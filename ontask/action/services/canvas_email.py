"""Views to run the personalized canvas email action."""
import datetime
import json
from time import sleep
from typing import Dict, Optional, Tuple
from zoneinfo import ZoneInfo

import requests
from celery.utils.log import get_task_logger
from django import http
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext, gettext_lazy as _
from rest_framework import status

from ontask import models
from ontask.action.evaluate import evaluate_action
from ontask.action.services.edit_factory import ActionOutEditProducerBase
from ontask.action.services.run_factory import ActionRunProducerBase
from ontask.core import is_instructor
from ontask.oauth import services

LOGGER = get_task_logger('celery_execution')


def _do_burst_pause(burst: int, burst_pause: int, idx: int):
    """Detect end of burst and pause if needed.

    :param burst: Burst length
    :param burst_pause: Pause after length is reached
    :param idx: Current index
    :return:
    """
    if burst and (idx % burst) == 0:
        # Burst exists and the limit has been reached
        LOGGER.info(
            'Burst (%s) reached. Waiting for %s secs',
            str(burst),
            str(burst_pause))
        sleep(burst_pause)


def _refresh_and_retry_send(
    oauth_info,
    conversation_url: str,
    canvas_email_payload: Dict,
):
    """Refresh OAuth token and retry send.

    :param oauth_info: Object with the oauth information
    :param conversation_url: URL to send the conversation
    :param canvas_email_payload: Dictionary with additional information
    :return:
    """
    # Request rejected due to token expiration. Refresh the token
    result_msg = gettext('OAuth token refreshed')
    response_status = None
    user_token = None
    try:
        user_token = services.refresh_token(user_token, oauth_info)

        if user_token := services.refresh_token(user_token, oauth_info):
            # Update the header with the new token
            headers = {
                'content-type':
                    'application/x-www-form-urlencoded; charset=UTF-8',
                'Authorization': 'Bearer {0}'.format(
                    user_token.access_token,
                ),
            }

            # Second attempt at executing the API call
            response = requests.post(
                url=conversation_url,
                data=canvas_email_payload,
                headers=headers)
            response_status = response.status_code
    except Exception as exc:
        result_msg = str(exc)

    return result_msg, response_status


@user_passes_test(is_instructor)
def _canvas_get_or_set_oauth_token(
    request: HttpRequest,
    oauth_instance_name: str,
    continue_url: str,
) -> http.HttpResponse:
    """Check for OAuth token, if not present, request a new one.

    Function that checks if the user has a Canvas OAuth token. If there is a
    token, the function goes straight to send the messages. If not, the OAuth
    process starts.

    :param request: Request object to process
    :param oauth_instance_name: Locator for the OAuth instance in OnTask
    :param continue_url: URL to continue if the token exists and is valid
    :return: Http response
    """
    # Get the information from the payload
    if not (oauth_info := settings.CANVAS_INFO_DICT.get(oauth_instance_name)):
        messages.error(
            request,
            _('Unable to obtain Canvas OAuth information'),
        )
        return redirect('action:index')

    # Check if we have the token
    if not (token := models.OAuthUserToken.objects.filter(
        user=request.user,
        instance_name=oauth_instance_name,
    ).first()):
        # There is no token, authentication has to take place for the first
        # time
        return services.get_initial_token_step1(
            request,
            oauth_info,
            reverse(continue_url))

    # Check if the token is valid
    now = datetime.datetime.now(ZoneInfo(settings.TIME_ZONE))
    if now > token.valid_until:
        try:
            services.refresh_token(token, oauth_info)
        except Exception as exc:
            # Something went wrong when refreshing the token
            messages.error(
                request,
                _('Error when invoking Canvas API: {0}.'.format(str(exc))),
            )
            return redirect('action:index')

    return redirect(continue_url)


def _send_single_canvas_message(
    conversation_url: str,
    canvas_email_payload,
    headers: Dict,
    oauth_info,
) -> Tuple[str, int]:
    """Send a single email to Canvas using the API.

    :param conversation_url: URL pointing to the conversation object
    :param canvas_email_payload: Email message
    :param headers: HTTP headers for the request
    :param oauth_info: Authentication info
    :return: response message, response status
    """
    result_msg = gettext('Message successfuly sent')

    # Send the email through the API call
    # First attempt
    response = requests.post(
        url=conversation_url,
        data=canvas_email_payload,
        headers=headers,
        verify=True)

    response_status = response.status_code
    if (
        response.status_code == status.HTTP_401_UNAUTHORIZED
        and response.headers.get('WWW-Authenticate')
    ):
        result_msg, response_status = _refresh_and_retry_send(
            oauth_info,
            conversation_url,
            canvas_email_payload,
        )
    elif response_status != status.HTTP_201_CREATED:
        result_msg = gettext(
            'Unable to deliver message (code {0})').format(
            response_status)

    return result_msg, response_status


class ActionEditProducerCanvasEmail(ActionOutEditProducerBase):
    """Class to serve running an email action."""

    def get_context_data(self, **kwargs) -> Dict:
        """Add conditions, conditions to clone and columns to show stats."""
        context = super().get_context_data(**kwargs)
        self.add_conditions(context)
        self.add_conditions_to_clone(context)
        self.add_columns_show_stats(context)
        return context


class ActionRunProducerCanvasEmail(ActionRunProducerBase):
    log_event = models.Log.ACTION_RUN_PERSONALIZED_CANVAS_EMAIL

    def form_valid(self, form) -> http.HttpResponse:
        """Process the VALID POST request."""
        if self.payload.get('confirm_items'):
            # Create a dictionary in the session to carry over all the
            # information to execute the next pages
            self.payload['button_label'] = gettext('Send')
            self.payload['value_range'] = 2
            self.payload['step'] = 2
            continue_url = 'action:item_filter'
        else:
            continue_url = 'action:run_done'

        self.payload.store_in_session(self.request.session)

        # Check for the CANVAS token and proceed to the continue_url
        return _canvas_get_or_set_oauth_token(
            self.request,
            self.payload['target_url'],
            continue_url)

    def execute_operation(
        self,
        user,
        workflow: Optional[models.Workflow] = None,
        action: Optional[models.Action] = None,
        payload: Optional[Dict] = None,
        log_item: Optional[models.Log] = None,
    ):
        """Send CANVAS emails with the action content evaluated for each row.

        Performs the submission of the emails for the given action and with the
        given subject. The subject will be evaluated also with respect to the
        rows, attributes, and conditions.
        :param user: User object that executed the action
        :param workflow: Workflow being processed
        :param action: Action from where to take the messages
        :param log_item: Log object to store results
        :param payload: Dictionary with all the parameters
        :return: Nothing
        """
        # Evaluate the action string, evaluate the subject, and get the value
        # of the email column.
        if log_item is None:
            log_item = action.log(user, self.log_event, **payload)

        item_column = action.workflow.columns.get(pk=payload['item_column'])
        action_evals = evaluate_action(
            action,
            extra_string=payload['subject'],
            column_name=item_column.name,
            exclude_values=payload.get('exclude_values', []))

        # Get the oauth info
        target_url = payload['target_url']
        if not (oauth_info := settings.CANVAS_INFO_DICT.get(target_url)):
            raise Exception(_('Unable to find OAuth Information Record'))

        # Get the token
        if not (user_token := models.OAuthUserToken.objects.filter(
            user=user,
            instance_name=target_url,
        ).first()):
            # There is no token, execution cannot proceed
            raise Exception(_('Incorrect execution due to absence of token'))

        # Create the headers to use for all requests
        headers = {
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Authorization': 'Bearer {0}'.format(user_token.access_token),
        }

        # Create the context for the log events
        context = {'action': action.id}

        # Send the objects to the given URL
        idx = 1
        burst = oauth_info['aux_params'].get('burst')
        burst_pause = oauth_info['aux_params'].get('pause', 0)
        domain = oauth_info['domain_port']
        conversation_url = oauth_info['conversation_url'].format(domain)
        to_emails = []
        for msg_body, msg_subject, msg_to in action_evals:
            # JSON object to send. Taken from method.conversations.create in
            # https://canvas.instructure.com/doc/api/conversations.html
            canvas_email_payload = {
                'recipients[]': int(msg_to),
                'body': msg_body,
                'subject': msg_subject,
                'force_new': True,
            }

            # Manage the bursts
            _do_burst_pause(burst, burst_pause, idx)
            # Index to detect bursts
            idx += 1

            # Send the email
            result_msg, response_status = _send_single_canvas_message(
                conversation_url,
                canvas_email_payload,
                headers,
                oauth_info,
            )
            if settings.ONTASK_TESTING:
                # Print the JSON object sent to the server
                LOGGER.info(
                    'SEND JSON(%s): %s',
                    target_url,
                    json.dumps(canvas_email_payload))
                result_msg = 'SENT TO LOGGER'
                response_status = 200

            # Log message sent
            context['subject'] = canvas_email_payload['subject']
            context['body'] = canvas_email_payload['body']
            context['from_email'] = user.email
            context['to_email'] = canvas_email_payload['recipients[]']
            context['email_sent_datetime'] = str(
                datetime.datetime.now(ZoneInfo(settings.TIME_ZONE)))
            context['response_status'] = response_status
            context['result_msg'] = result_msg
            action.log(
                user,
                models.Log.ACTION_CANVAS_EMAIL_SENT,
                **context)
            to_emails.append(msg_to)

        action.last_executed_log = log_item
        action.save(update_fields=['last_executed_log'])

        # Update excluded items in payload
        self._update_excluded_items(payload, to_emails)

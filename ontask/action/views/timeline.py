# -*- coding: utf-8 -*-

"""View to implement the timeline visualization."""
from typing import Optional

from django import http
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render

from ontask import models
from ontask.core import get_workflow, is_instructor


@user_passes_test(is_instructor)
@get_workflow(pf_related='logs')
def show_timeline(
    request: http.HttpRequest,
    pk: Optional[int] = None,
    workflow: Optional[models.Workflow] = None,
) -> http.HttpResponse:
    """Show a vertical timeline of action executions.

    :param request: HTTP request
    :param pk: Action PK. If none, all of them in workflow are considered
    :param workflow: Workflow being manipulated (set by the decorators)
    :return: HTTP response
    """
    action = None
    if pk:
        action = workflow.actions.filter(pk=pk).first()

        if not action:
            # The action is not part of the selected workflow
            return redirect('home')
        logs = workflow.logs.filter(payload__action_id=action.id)
    else:
        logs = workflow.logs

    logs = logs.order_by('created')
    event_names = [
        models.Log.ACTION_DOWNLOAD,
        models.Log.ACTION_RUN_PERSONALIZED_CANVAS_EMAIL,
        models.Log.ACTION_RUN_PERSONALIZED_EMAIL,
        models.Log.ACTION_RUN_PERSONALIZED_JSON,
        models.Log.ACTION_RUN_JSON_REPORT,
        models.Log.ACTION_RUN_EMAIL_REPORT,
        models.Log.ACTION_SURVEY_INPUT,
        models.Log.SCHEDULE_CREATE,
        models.Log.SCHEDULE_EDIT,
        models.Log.SCHEDULE_DELETE]

    # Filter the logs to display and transform into values (process the json
    # and the long value for the log name
    logs = logs.filter(name__in=event_names).exclude(payload__action=None)

    return render(
        request,
        'action/timeline.html',
        {'event_list': logs, 'action': action})

# -*- coding: utf-8 -*-

"""Module common operations."""
from typing import Optional, Tuple

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext

from ontask import models


def get_execution_items(
    user_id: int,
    workflow_id: Optional[int] = None,
    action_id: Optional[int] = None,
) -> Tuple:
    """Get the objects with the given ids.

    Given a set of ids, get the objects from the DB

    :param user_id: User id
    :param workflow_id: Workflow ID (being manipulated)
    :param action_id: Action id (to be executed)
    :return: (user, action, log)
    """
    # Get the user
    user = None
    if user_id:
        user = get_user_model().objects.filter(id=user_id).first()
        if not user:
            raise Exception(
                ugettext('Unable to find user with id {0}').format(user_id),
            )

    workflow = None
    if workflow_id:
        workflow = models.Workflow.objects.filter(
            user=user,
            pk=workflow_id).first()
        if not workflow:
            raise Exception(
                ugettext('Unable to find workflow with id {0}').format(
                    workflow_id))

    action = None
    if action_id:
        # Get the action
        action = models.Action.objects.filter(
            workflow__user=user,
            pk=action_id).first()
        if not action:
            raise Exception(
                ugettext('Unable to find action with id {0}').format(
                    action_id))

    return user, workflow, action

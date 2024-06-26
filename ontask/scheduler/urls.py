"""URLs for the scheduler package."""
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from ontask import models
from ontask.scheduler import api, services, views

app_name = 'scheduler'

urlpatterns = [

    # List all schedule actions
    path('', views.SchedulerIndex.as_view(), name='index'),

    # Select a SQL connection
    path(
        'select_sql/',
        views.SchedulerConnectionIndex.as_view(),
        name='select_sql'),

    # Create scheduled action
    path(
        '<int:pk>/create_action_run/',
        views.create_action_run,
        name='create_action_run'),

    # Create a SQL upload operation
    path('<int:pk>/sqlupload/', views.create_sql_upload, name='sqlupload'),

    # Edit scheduled operation
    path(
        '<int:pk>/edit_scheduled_operation/',
        views.edit_scheduled_operation,
        name='edit_scheduled_operation'),

    path(
        'finish_scheduling/',
        views.finish_scheduling,
        name='finish_scheduling'),

    # View the details of a scheduled operation
    path('<int:pk>/view/', views.SchedulerIndexView.as_view(), name='view'),

    # Delete scheduled action
    path(
        '<int:pk>/delete/',
        views.ScheduledItemDelete.as_view(),
        name='delete'),

    # Toggle scheduled enable
    path(
        '<int:pk>/schedule_toggle/',
        views.ActionToggleQuestionChangeView.as_view(),
        name='schedule_toggle'),

    # API
    path(
        'scheduled_email/',
        api.ScheduledOperationEmailAPIListCreate.as_view(),
        name='api_scheduled_email'),

    path(
        'scheduled_json/',
        api.ScheduledOperationJSONAPIListCreate.as_view(),
        name='api_scheduled_json'),

    # Get, update content or destroy scheduled actions
    path(
        '<int:pk>/rud_email/',
        api.ScheduledEmailAPIRetrieveUpdateDestroy.as_view(),
        name='api_rud_email'),
    path(
        '<int:pk>/rud_json/',
        api.ScheduledJSONAPIRetrieveUpdateDestroy.as_view(),
        name='api_rud_json'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

services.SCHEDULE_CRUD_FACTORY.register_producer(
    models.Action.PERSONALIZED_TEXT,
    services.ScheduledOperationEmailUpdateView)

services.SCHEDULE_CRUD_FACTORY.register_producer(
    models.Action.EMAIL_REPORT,
    services.ScheduledOperationEmailReportUpdateView)

services.SCHEDULE_CRUD_FACTORY.register_producer(
    models.Action.RUBRIC_TEXT,
    services.ScheduledOperationEmailUpdateView)

services.SCHEDULE_CRUD_FACTORY.register_producer(
    models.Action.PERSONALIZED_JSON,
    services.ScheduledOperationJSONUpdateView)

services.SCHEDULE_CRUD_FACTORY.register_producer(
    models.Action.JSON_REPORT,
    services.ScheduledOperationJSONReportUpdateView)

# services.SCHEDULE_CRUD_FACTORY.register_producer(
#     models.Action.PERSONALIZED_CANVAS_EMAIL,
#     services.ScheduleOperation???)

services.SCHEDULE_CRUD_FACTORY.register_producer(
    models.Log.WORKFLOW_DATA_SQL_UPLOAD,
    services.ScheduledOperationUpdateSQLUpload)

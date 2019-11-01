# -*- coding: utf-8 -*-

"""URL to manipulate actions."""

from django.urls import path, re_path

from ontask.action import views

app_name = 'action'

urlpatterns = [
    #
    # Action CRUD
    #
    # List them all
    path('', views.action_index, name='index'),
    path('<int:wid>/index/', views.action_index, name='index_set'),

    # Create an action
    path('create/', views.ActionCreateView.as_view(), name='create'),

    # Show timeline
    path('timeline/', views.show_timeline, name='timeline'),
    path('<int:pk>/timeline/', views.show_timeline, name='timeline'),

    # Edit action
    path('<int:pk>/edit/', views.edit_action, name='edit'),

    # Save action out content
    path(
        '<int:pk>/action_out_save_content/',
        views.action_out_save_content,
        name='action_out_save_content'),

    # Action export ask
    # path('<int:pk>/export_ask/', views.export_ask, name='export_ask'),

    # Action export the file
    re_path(
        r'(?P<pklist>\d+(,\d+)*)/export/',
        views.export,
        name='export'),

    # Action import
    path('import/', views.action_import, name='import'),

    # Update an action
    path('<int:pk>/update/', views.ActionUpdateView.as_view(), name='update'),

    # Clone the action
    path('<int:pk>/clone_action/', views.clone_action, name='clone_action'),

    # Nuke the action
    path('<int:pk>/delete/', views.delete_action, name='delete'),

    # Run ZIP action
    path('<int:pk>/zip/', views.zip_action, name='zip_action'),

    # Run action
    path('<int:pk>/run/', views.run_action, name='run'),

    #
    # Personalised text and JSON action steps
    #
    path('item_filter/', views.run_action_item_filter, name='item_filter'),

    #
    # URLs to use when action finishes run
    #
    path('email_done/', views.run_email_done, name='email_done'),
    path('zip_done/', views.run_zip_done, name='zip_done'),
    path('zip_export/', views.action_zip_export, name='zip_export'),
    path('json_done/', views.run_json_done, name='json_done'),
    path(
        'canvas_email_done/',
        views.run_canvas_email_done,
        name='canvas_email_done'),

    #
    # ACTION IN EDIT PAGE
    #
    # Manage columns for action in
    path(
        '<int:pk>/<int:cpk>/<int:key>/select_column_action/',
        views.select_column_action,
        name='select_key_column_action'),
    path(
        '<int:pk>/select_column_action/',
        views.select_column_action,
        name='unselect_key_column_action'),

    # Select column for action in
    path(
        '<int:pk>/<int:cpk>/select_column_action/',
        views.select_column_action,
        name='select_column_action'),

    # Unselect column for action in
    path(
        '<int:pk>/<int:cpk>/unselect_column_action/',
        views.unselect_column_action,
        name='unselect_column_action'),

    # Toggle shuffle action-in
    path(
        '<int:pk>/shuffle_questions/',
        views.shuffle_questions,
        name='shuffle_questions'),

    # Toggle question changes
    path(
        '<int:pk>/toggle_question_change/',
        views.toggle_question_change,
        name='toggle_question_change'),

    # Select condition for a column/question
    path(
        '<int:pk>/<int:condpk>/select_condition/',
        views.select_condition_for_question,
        name='edit_in_select_condition'),
    path(
        '<int:tpk>/select_condition/',
        views.select_condition_for_question,
        name='edit_in_select_condition'),

    # Rubric URLs
    path(
        '<int:pk>/<int:cid>/<int:loa_pos>/rubriccell_edit',
        views.edit_rubric_cell,
        name='rubriccell_edit'),
    path(
        '<int:pk>/rubric_loas_edit',
        views.edit_rubric_loas,
        name='rubric_loas_edit'),

    #
    # RUN SURVEY
    #
    # Server side update of the run survey page for action in
    path('<int:pk>/run_survey_ss/', views.run_survey_ss, name='run_survey_ss'),

    # Run action in a row. Can be executed by the instructor or the
    # learner!!
    path(
        '<int:pk>/run_survey_row/',
        views.run_survey_row,
        name='run_survey_row'),

    # Say thanks
    path('thanks/', views.survey_thanks, name='thanks'),

    #
    # Preview action out
    #
    path(
        '<int:pk>/<int:idx>/preview/',
        views.preview_response,
        name='preview'),
    path(
        '<int:pk>/<int:idx>/preview_next_all_false/',
        views.preview_next_all_false_response,
        name='preview_all_false'),

    # Allow url on/off toggle
    path('<int:pk>/showurl/', views.showurl, name='showurl'),

    #
    # Serve the personalised content
    #
    path('<int:action_id>/serve/', views.serve_action, name='serve'),
    path('serve/', views.serve_action_lti, name='serve_lti'),

    #
    # Edit action description and name
    #
    path(
        '<int:pk>/edit_description/',
        views.edit_description,
        name='edit_description'),

    #
    # FILTERS
    #
    path(
        '<int:pk>/create_filter/',
        views.FilterCreateView.as_view(),
        name='create_filter'),
    path('<int:pk>/edit_filter/', views.edit_filter, name='edit_filter'),
    path('<int:pk>/delete_filter/', views.delete_filter, name='delete_filter'),

    #
    # CONDITIONS
    #
    path(
        '<int:pk>/create_condition/',
        views.ConditionCreateView.as_view(),
        name='create_condition'),
    path(
        '<int:pk>/edit_condition/',
        views.edit_condition,
        name='edit_condition'),
    path(
        '<int:pk>/delete_condition/',
        views.delete_condition,
        name='delete_condition'),

    # Clone the condition
    path(
        '<int:pk>/clone_condition/',
        views.clone_condition,
        name='clone_condition'),
    path(
        '<int:pk>/<int:action_pk>/clone_condition/',
        views.clone_condition,
        name='clone_condition'),
]
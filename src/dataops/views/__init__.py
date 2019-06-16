# -*- coding: utf-8 -*-

"""Package with the dataops views."""

from dataops.views.csvupload import csvupload_start
from dataops.views.excelupload import excelupload_start
from dataops.views.googlesheetupload import googlesheetupload_start
from dataops.views.row import row_create, row_update
from dataops.views.s3upload import s3upload_start
from dataops.views.sqlconnection import (
    sqlconn_add, sqlconn_clone, sqlconn_delete, sqlconn_edit, sqlconn_view,
    sqlconnection_admin_index, sqlconnection_instructor_index,
)
from dataops.views.sqlupload import sqlupload_start
from dataops.views.transform import (
    plugin_invoke, transform_model
)
from dataops.views.plugin_admin import (
    plugin_admin, diagnose, moreinfo,
    plugin_toggle,
)
from dataops.views.upload import upload_s2, upload_s3, upload_s4, uploadmerge
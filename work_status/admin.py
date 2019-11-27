from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *

# Register your models here.


@admin.register(lte_integration, lte_validation, team, prs)

class ViewAdmin(ImportExportModelAdmin):
    pass
    exclude = ('id','completed' )


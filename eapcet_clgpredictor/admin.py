from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import ClgsCutoffs
# Register your models here.

class ClgsCutoffsAdmin (ImportExportModelAdmin):
    pass
admin.site.register(ClgsCutoffs,ClgsCutoffsAdmin)


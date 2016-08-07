from django.contrib import admin
from .models import ZoteroReference

@admin.register(ZoteroReference)
class ZoteroReference(admin.ModelAdmin):
    list_display = ['key']
    search_fields = ['key']

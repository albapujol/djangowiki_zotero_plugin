from django.contrib import admin
from .models import ZoteroReference, ZoteroAttachment

@admin.register(ZoteroReference)
class ZoteroReferenceAdmin(admin.ModelAdmin):
    list_display = ['key']
    search_fields = ['key']

@admin.register(ZoteroAttachment)
class ZoteroAttachmentAdmin(admin.ModelAdmin):
    list_display = ['key']
    search_fields = ['key']
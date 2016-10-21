from django.db import models

class ZoteroReference(models.Model):
    key = models.CharField(max_length=8, unique=True)
    bibtex_key = models.CharField(max_length=100)
    url = models.CharField(max_length=500)
    bibtex = models.TextField()
    citation = models.TextField()
    abstract = models.TextField()
    fetch_timestamp = models.DateTimeField(auto_now=True)
    # json = JSONField()

class ZoteroAttachment(models.Model):
    reference = models.ForeignKey(ZoteroReference)
    key = models.CharField(max_length=8, unique=True)
    attachment = models.FileField(upload_to='zotero/', blank=True)

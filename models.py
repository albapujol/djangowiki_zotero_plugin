from django.db import models
# from django.contrib.postgres.fields import JSONField

class ZoteroReference(models.Model):
    key = models.CharField(max_length=8)
    bibtex_key = models.CharField(max_length=100)
    url = models.CharField(max_length=500)
    bibtex = models.TextField()
    citation = models.TextField()
    abstract = models.TextField()
    # json = JSONField()


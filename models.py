from django.db import models

class ZoteroReference(models.Model):
    key = models.CharField(max_length=8)
    bibtex_key = models.CharField(max_length=100)
    url = models.CharField(max_length=500)
    citation_sidebar = models.TextField()
    bibtex = models.TextField()
    citation_text = models.TextField()
    abstract = models.TextField()


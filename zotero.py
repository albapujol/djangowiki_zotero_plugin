import re
from pyzotero import zotero as zotero_api
from . import settings
from . import models
import datetime
import django.utils.timezone

BIBTEX_REGEX = r'{(?P<backup>[^\]]*?),'

class ZoteroWrapper():
    def __init__(self):
        self.id = settings.ZOTERO_ID #if id is None else id
        self.key = settings.ZOTERO_KEY #if key is None else key
        self.id_type = settings.ZOTERO_ID_TYPE #if id_type is None else id_type
        self.refresh_rate = datetime.timedelta(**settings.ZOTERO_REFRESH_RATE)
        self.client = zotero_api.Zotero(self.id, self.id_type, self.key)
        self.style= settings.ZOTERO_BIB_STYLE

    def query_elements(self, query):
        res = self.client.top(q=query, format='json', include='bib', style=self.style)
        # res = self.client.top(q=query, format='json', include='bib,bibtex,data', style=self.style)
        # for r in res:
        #     _ = self.store_got_element(r)
        return [{'text': i['bib'], 'key': i['key']} for i in res]

    def get_element(self, key):
        try:
            obj = models.ZoteroReference.objects.filter(key=key)[0]
            if obj.fetch_timestamp + self.refresh_rate > django.utils.timezone.now():
                raise IndexError
        except IndexError:
            json = self.client.top(itemKey=key, format='json', include='bib,bibtex,data', style=self.style)[0]
            obj = self.store_got_element(json)
        return {
            'key': key,
            'bibtex_key': obj.bibtex_key,
            'url': obj.url,
            'bibtex': obj.bibtex,
            'citation': obj.citation,
            'abstract': obj.abstract
        }

    def store_got_element(self, json):
        key = json['key']
        bibtex = json['bibtex']
        citation = json['bib']
        url = json['links']["alternate"]['href']
        abstract = json['data']['abstractNote']
        bibtex_key = re.search(BIBTEX_REGEX, bibtex).group(1)
        try:
            obj = models.ZoteroReference.objects.filter(key=key)[0]
            obj.bibtex_key = bibtex_key
            obj.abstract = abstract
            obj.url = url
            obj.citation = citation
            obj.bibtex = bibtex
            obj.save()
            return obj
        except IndexError:
            return models.ZoteroReference.objects.create(
                key=key,
                bibtex_key=bibtex_key,
                url=url,
                bibtex=bibtex,
                citation=citation,
                abstract=abstract,
            )

zotero_port = ZoteroWrapper()
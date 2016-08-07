import re
from pyzotero import zotero as zotero_api
from . import settings
from . import models

BIBTEX_REGEX = r'{(?P<backup>[^\]]*?),'

class ZoteroWrapper():
    def __init__(self):
        self.id = settings.ZOTERO_ID #if id is None else id
        self.key = settings.ZOTERO_KEY #if key is None else key
        self.id_type = settings.ZOTERO_ID_TYPE #if id_type is None else id_type
        self.client = zotero_api.Zotero(self.id, self.id_type, self.key)

    def query_elements(self, query):
        res = self.client.top(q=query, format='json', include='citation')
        return [{'text':i['citation'], 'key':i['key']} for i in res]

    def get_elemment(self, key):
        try:
            obj = models.ZoteroReference.objects.filter(key=key)[0]
            return {
                'bibtex_key': obj.bibtex_key,
                'url': obj.url,
                'bibtex': obj.bibtex,
                'citation': obj.citation,
                'abstract': obj.abstract
            }
        except IndexError:
            citation = self.client.top(itemKey=key, format='json', include='bib', style="mla")[0]["bib"]
            bibtex = self.client.top(itemKey=key, format='json', include='bib', style="bibtex")[0]["bib"]
            json = self.client.top(itemKey=key)[0]
            url = json['links']["alternate"]['href']
            abstract= json['data']['abstractNote']
            bibtex_key = re.search(BIBTEX_REGEX, bibtex).group(1)
            models.ZoteroReference.objects.get_or_create(
                key=key,
                bibtex_key=bibtex_key,
                url=url,
                bibtex=bibtex,
                citation=citation,
                abstract=abstract
            )
            obj = models.ZoteroReference.objects.filter(key=key)[0]
            return {
                'bibtex_key': obj.bibtex_key,
                'url': obj.url,
                'bibtex': obj.bibtex,
                'citation': obj.citation,
                'abstract': obj.abstract
            }




zotero_port = ZoteroWrapper()
import re
from pyzotero import zotero as zotero_api
from . import settings
from . import models
import datetime
import django.utils.timezone
import easywebdav
import zipfile
from easywebdav.client import OperationFailed
import os
from django.core.files.base import ContentFile

BIBTEX_REGEX = r'{(?P<backup>[^\]]*?),'

class ZoteroWrapper():
    def __init__(self):
        self.id = settings.ZOTERO_ID
        self.key = settings.ZOTERO_KEY
        self.id_type = settings.ZOTERO_ID_TYPE
        self.refresh_rate = datetime.timedelta(**settings.ZOTERO_REFRESH_RATE)
        self.client = zotero_api.Zotero(self.id, self.id_type, self.key)
        self.webdav_client = easywebdav.connect(settings.WEBDAV_URL,
                                                path=settings.WEBDAV_PATH,
                                                username=settings.WEBDAV_USER,
                                                password=settings.WEBDAV_PASSWORD,
                                                protocol=settings.WEBDAV_PROTOCOL)
        self.style= settings.ZOTERO_BIB_STYLE

    def query_elements(self, query):
        res = self.client.top(q=query, format='json', include='bib', style=self.style)
        # res = self.client.top(q=query, format='json', include='bib,bibtex,data', style=self.style)
        # for r in res:
        #     _ = self.store_got_element(r)
        print res
        return [{'text': i['bib'], 'key': i['key']} for i in res]

    def get_element(self, key):
        print "getting element"
        try:
            obj = models.ZoteroReference.objects.filter(key=key)[0]
            print "element found"
            if obj.fetch_timestamp + self.refresh_rate < django.utils.timezone.now():
                print "element old"
                raise IndexError
        except IndexError:
            print "element not found or old"
            try:
                json = self.client.top(itemKey=key, format='json', include='bib,bibtex,data', style=self.style)[0]
                children = self.client.children(key)
                obj = self.store_got_element(json, children)
            except IndexError:
                return {
                    'key': '',
                    'bibtex_key': '%s -not found' % key,
                    'url': '',
                    'bibtex': '',
                    'citation': 'Element %s not found in Zotero database' % key,
                    'abstract': '',
                    'downloads': [],
                }
        return {
            'key': key,
            'bibtex_key': obj.bibtex_key,
            'url': obj.url,
            'bibtex': obj.bibtex,
            'citation': obj.citation,
            'abstract': obj.abstract,
            'downloads': obj.zoteroattachment_set.all(),
        }

    def store_got_element(self, json, children):
        print "storing element"
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
            obj.fetch_timestamp = datetime.datetime.now()
            obj.save()
        except IndexError:
            obj = models.ZoteroReference.objects.create(
                key=key,
                bibtex_key=bibtex_key,
                url=url,
                bibtex=bibtex,
                citation=citation,
                abstract=abstract,
                fetch_timestamp=datetime.datetime.now()
            )
        for el in children:
                if el['data']['contentType'] == 'application/pdf':
                    print "storing pdf"
                    self.store_pdf(obj, el['data']['key'])
        return obj


    def store_pdf(self, parent_obj, key):
        try:
            obj = models.ZoteroAttachment.objects.filter(key=key)[0]
            obj.reference = parent_obj
        except IndexError:
            obj = models.ZoteroAttachment.objects.create(
                key=key,
                reference=parent_obj,
            )
        try:
            self.webdav_client.download('zotero/%s.zip' % key, 'tmp.zip')
            z_file = zipfile.ZipFile('tmp.zip')
            pathfile = z_file.extract(z_file.namelist()[0])
            with open(pathfile) as f:
                data = f.read()
            import os, binascii
            print z_file.namelist()[0]
            obj.attachment.delete(save=False)
            obj.attachment.save(binascii.b2a_hex(os.urandom(4))+z_file.namelist()[0], ContentFile(data))
            obj.save()
            os.remove(pathfile)
        except OperationFailed:
            pass
        return obj


zotero_port = ZoteroWrapper()

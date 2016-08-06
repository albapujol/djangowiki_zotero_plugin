from pyzotero import zotero as zotero_api
from . import settings
from . import models

from pyzotero import zotero
# zotero_key = '1IIOOfDvfYEtDi3sDcBFPZx1'
# zotero_id = '1785240'
# zot = zotero.Zotero(zotero_id, 'user', zotero_key)

from pyzotero import zotero as zotero_api
from . import settings
from . import models
#
#
class ZoteroWrapper():
    def __init__(self):
        self.id = settings.ZOTERO_ID #if id is None else id
        self.key = settings.ZOTERO_KEY #if key is None else key
        self.id_type = settings.ZOTERO_ID_TYPE #if id_type is None else id_type
        self.client = zotero_api.Zotero(self.id, self.id_type, self.key)

    def query_elements(self, query):
        res = self.client.top(q=query, format='json', include='citation')
        return [{'text':i['citation'], 'key':i['key']} for i in res]

zotero_port = ZoteroWrapper()

# zot = zotero.Zotero(zotero_id, 'user', zotero_key)
#
zotero_port = ZoteroWrapper()
#
# # zot = zotero.Zotero(zotero_id, 'user', zotero_key)

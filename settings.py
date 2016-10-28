from django.conf import settings as django_settings

SLUG = 'zotero'

ZOTERO_KEY = getattr(django_settings, 'WIKI_ZOTERO_KEY', 'your_zotero_key')
ZOTERO_ID = getattr(django_settings, 'WIKI_ZOTERO_ID', 'your_zotero_id')
ZOTERO_ID_TYPE = getattr(django_settings, 'WIKI_ZOTERO_ID_TYPE', 'user')

ZOTERO_BIB_STYLE = getattr(django_settings, 'WIKI_ZOTERO_BIB_STYLE', 'mla')

ZOTERO_REFRESH_RATE = getattr(django_settings, 'WIKI_ZOTERO_REFRESH_RATE',
                              {
                                  'seconds': 0,
                                  'minutes': 0,
                                  'hours': 0,
                                  'days': 0,
                                  'weeks': 4,
                              })

WEBDAV_URL = getattr(django_settings, 'WIKI_ZOTERO_WEBDAV_URL', 'your_webdav_url')
WEBDAV_PATH = getattr(django_settings, 'WIKI_ZOTERO_WEBDAV_PATH','your_webdav_password')
WEBDAV_PROTOCOL = getattr(django_settings, 'WIKI_ZOTERO_WEBDAV_PROTOCOL','https')
WEBDAV_USER = getattr(django_settings, 'WIKI_ZOTERO_WEBDAV_USER','your_webdav_user')
WEBDAV_PASSWORD = getattr(django_settings, 'WIKI_ZOTERO_WEBDAV_PASSWORD','your_webdav_password')

from .zotero import zotero_port

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def available_zotero_resources(request, path):
    """
    The description goes there?!
    """
    try:
        return Response(zotero_port.query_elements(request.query_params["pattern"]))
    except KeyError:
        return Response([])

@api_view(['GET'])
def bibtex_file(request, path):
    """
    API to call to retrieve the bibtex fille of the keys referred in the request
    """
    pass
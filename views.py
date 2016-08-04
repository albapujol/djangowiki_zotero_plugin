from .zotero import zot
from pprint import pprint

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def available_zotero_resources(request, path):
    """
    The description goes there?!
    """
    try:
        items = zot.top(q=request.query_params['pattern'], format='json', include='citation')
        print items
        return Response([i['citation'] for i in items])
    except KeyError:
        return Response({})
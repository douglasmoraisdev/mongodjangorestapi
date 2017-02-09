from django.contrib.auth.models import User, Group

from apigateway.services import *

from cell.serializers import CellSerializer
from cell.models import *

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_mongoengine.viewsets import ModelViewSet		

from oauth2_provider.views.generic import ProtectedResourceView
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope


class ApiGatewayViewSet(ProtectedResourceView, ModelViewSet):
    """
    API endpoint that allows cells to be viewed or edited.
    """
    queryset = Cells.objects.all()
    serializer_class = CellSerializer
    depth = 5

    # OAuth
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    required_scopes = ['cells']

    def list(self, request):
        
        cell_m_data = get_books('', '', request)
        
        return Response(cell_m_data)

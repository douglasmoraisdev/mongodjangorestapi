from django.contrib.auth.models import User, Group

from cell.serializers import CellSerializer
from cell.models import *

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_mongoengine.viewsets import ModelViewSet		

from oauth2_provider.views.generic import ProtectedResourceView
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope


class CellsViewSet(ProtectedResourceView, ModelViewSet):
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
        queryset = self.queryset
        serializer = CellSerializer(queryset, many=True)
        return Response(serializer.data)

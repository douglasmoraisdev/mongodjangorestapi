from django.contrib.auth.models import User, Group

from cell.serializers import CellSerializer
from cell.models import *

from rest_framework.response import Response

from rest_framework_mongoengine.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet		

from bethel_core.decorators import *




class CellsViewSet(ModelViewSet):
    """
    API endpoint that allows cells to be viewed or edited.
    """
    queryset = Cells.objects.all()
    serializer_class = CellSerializer    


    #Override
    def list(self, request):
        queryset = Cells.objects()
        serializer = CellSerializer(queryset, many=True)
        return Response(serializer.data)
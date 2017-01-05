from django.contrib.auth.models import User, Group
from cell.serializers import CellSerializer

from cell.models import *


from rest_framework_mongoengine.viewsets import GenericViewSet


class CellsViewSet(GenericViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Cells.objects.all()
    serializer_class = CellSerializer

from django.contrib.auth.models import User, Group
from cell.serializers import CellSerializer

from cell_metting.models import *


from rest_framework_mongoengine.viewsets import GenericViewSet, ModelViewSet


class CellMettingsViewSet(ModelViewSet):
    """
    API endpoint that allows cells to be viewed or edited.
    """
    queryset = Cell_mettings.objects.all()
    serializer_class = CellSerializer

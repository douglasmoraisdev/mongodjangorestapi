from .models import Cell_mettings

from rest_framework_mongoengine.serializers import DocumentSerializer


class CellMettingSerializer(DocumentSerializer):
    class Meta:
        model = Cell_mettings
        fields = ('name')
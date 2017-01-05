from .models import Cells

#from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer


class CellSerializer(DocumentSerializer):
    class Meta:
        model = Cells
        fields = ('name', 'street')
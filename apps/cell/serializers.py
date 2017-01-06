from .models import Cells

from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer


class CellSerializer(DocumentSerializer):

    class Meta:
        model = Cells
        fields = ('name', 'street', 'street_number', 'user_roles')
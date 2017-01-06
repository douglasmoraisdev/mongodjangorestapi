from .models import Users

from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer


class BethelCoreSerializer(DocumentSerializer):

    class Meta:
        model = Users
        fields = ('__all__')
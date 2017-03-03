from .models import Users, Roles

from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer


class BethelCoreSerializer(DocumentSerializer):

    class Meta:
        model = Users
        fields = ('__all__')


class RoleSerializer(DocumentSerializer):

    class Meta:
        model = Roles
        fields = ('id', 'name', 'code',)
from .models import Users

from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer


class UsersSerializer(DocumentSerializer):

    class Meta:
        model = Users
        fields = ('user_name', 'first_name')
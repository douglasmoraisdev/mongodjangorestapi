from .models import Users, User_roles

from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer

class UserroleSerializer(EmbeddedDocumentSerializer):

	class Meta:
		model = User_roles
		depth = 2
		fields = '__all__'


class UsersSerializer(DocumentSerializer):

    class Meta:
        model = Users
        fields = ('user_name', 'first_name')
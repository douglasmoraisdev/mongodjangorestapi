from .models import *

from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer

from core.serializers import RoleSerializer

class UsersSerializer(DocumentSerializer):

    class Meta:
        model = BUsers
        fields = ('user_name', 'first_name', 'city', 'phones')

class UserroleSerializer(EmbeddedDocumentSerializer):

	user = UsersSerializer()
	role = RoleSerializer(many = True)

	class Meta:
		model = BUser_roles
		depth = 2
		fields = ('role','user')

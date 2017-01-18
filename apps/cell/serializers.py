from .models import Cells

from user.models import User_roles
from user.serializers import UserroleSerializer

from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer
from rest_framework.serializers import SerializerMethodField

import bethel_core.utils as utils


class CellSerializer(DocumentSerializer):

	#user_roles = UserroleSerializer(User_roles, many=True)
	members_count = SerializerMethodField()
	members_geolocation = SerializerMethodField()


	class Meta:
		model = Cells
		depth = 2
		#fields = '__all__'
		fields = ('id', 'name', 'members_count', 'members_geolocation')


	def get_members_count(self, obj):
		return obj.user_roles.count();


	def get_members_geolocation(self, obj):
		return utils.get_users_geo(obj.user_roles)
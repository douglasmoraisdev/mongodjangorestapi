from .models import Cell_mettings

from core.models import Events, Users, User_roles
from user.serializers import UserroleSerializer

from rest_framework_mongoengine.serializers import *
from rest_framework_mongoengine.fields import *

from rest_framework.fields import CharField

from rest_framework.serializers import SerializerMethodField

from cell.models import *
from cell.serializers import CellSerializer, CellofMettingSerializer


import cell as cls

class CellMettingSerializer(DocumentSerializer):
	'''
		Cell metting main data
	'''
	
	user_roles = UserroleSerializer(User_roles, many=True, read_only=True)
	cell = SerializerMethodField(read_only=True)
	host = CellSerializer(Cells,many=False, read_only=True)
	field_info = ''


	class Meta:
		model = Events
		fields = ('id', 'name', 'host','user_roles', 'start_date', 'end_date', 'txt_obs', 'event_income', 'status_acomplished', 'cell')
		depth = 2
		

	def to_internal_value(self, data):
		
		data['host'] = Cells.objects.get(id=ObjectId(data['host']))

		return data

	
	def update(self, instance, validated_data, data=None):

		#Alternative method
		#Cell_mettings.objects.filter(id=instance.id).update(**validated_data)
		#return Cell_mettings.objects.get(id=instance.id)
		
		instance.modify(**validated_data)
		
		return self.data
		
	def create(self, validated_data):

		instance = Cell_mettings.objects.create(**validated_data)
		
		#return instance		
		return instance

		
	def get_cell(self, obj):
		
		if obj.host:
			queryset = Cells.objects(id=obj.host.id)
			serializer = CellofMettingSerializer(queryset, many=True)
			return serializer.data


class MettingsofCellSerializer(DocumentSerializer):
	'''
		Used to display data on cells page
	'''
	
	user_roles = UserroleSerializer(User_roles, many=True)


	class Meta:
		model = Events
		fields = ('id', 'name', 'user_roles', 'start_date', 'end_date', 'status_acomplished')
		depth = 2

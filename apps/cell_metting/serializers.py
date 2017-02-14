from .models import Cell_mettings

from bethel_core.models import Events, Users, User_roles
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

		#host = Cells.objects.get(id=ObjectId(validated_data.get('host')))
		
		#instance.name = validated_data.get('name', instance.name)
		#instance.event_income = validated_data.get('event_income', instance.event_income)
		#instance.txt_obs = validated_data.get('txt_obs', instance.txt_obs)
		#instance.host = validated_data.get('host', instance.host)
		
		#from pudb import set_trace; set_trace()
		
		#instance.name = validated_data.get('name', instance.name)		
		#instance.save()
		
		Cell_mettings.objects.filter(id=instance.id).update(**validated_data)
		#return instance
		return Cell_mettings.objects.get(id=instance.id)
		
	def create(self, validated_data):
	
		#from pudb import set_trace; set_trace()
		
		
	
		instance = Cell_mettings.objects.create(**validated_data)
		
		#instance.name = validated_data.get('name', instance.name)

		#instance.save()
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

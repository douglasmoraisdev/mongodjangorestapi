from .models import Cell_mettings

from bethel_core.models import Events, Users, User_roles
from user.serializers import UserroleSerializer

from rest_framework_mongoengine.serializers import *
from rest_framework_mongoengine.fields import *

from rest_framework.fields import CharField

from rest_framework.serializers import SerializerMethodField

from cell.models import *

import cell as cls

class CellMettingSerializer(DocumentSerializer):
	'''
		Cell metting main data
	'''
	
	user_roles = UserroleSerializer(User_roles, many=True)
	cell = SerializerMethodField(read_only=True)


	class Meta:
		model = Events
		fields = ('id', 'name', 'user_roles', 'start_date', 'end_date', 'txt_obs', 'event_income', 'status_acomplished', 'cell')
		depth = 2


	def get_cell(self, obj):
		
		queryset = Cells.objects(id=obj.host.id)
		serializer = cls.serializers.CellofMettingSerializer(queryset, many=True)
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

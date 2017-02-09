from .models import Cell_mettings

from bethel_core.models import Events, Users, User_roles
from user.serializers import UserroleSerializer

from rest_framework_mongoengine.serializers import *
from rest_framework_mongoengine.fields import *

from rest_framework.fields import CharField




class CellMettingSerializer(DocumentSerializer):
	
	user_roles = UserroleSerializer(User_roles, many=True)


	class Meta:
		model = Events
		fields = ('id', 'host', 'name', 'user_roles', 'start_date', 'end_date', 'txt_obs', 'event_income', 'status_acomplished')
		depth = 2

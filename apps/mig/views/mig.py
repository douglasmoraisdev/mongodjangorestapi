from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import HttpResponseForbidden
from bson.objectid import ObjectId
from django.urls import reverse
from bethel_core import utils

from django.utils.translation import *


from mig.models import *

import uuid
import googlemaps


from bethel_core.decorators import *

import logging

logger = logging.getLogger(__name__)


def prover(request,  user_apps=''):


	#Usuarios
	res_mig_user = Mig().mig_users()

	result_msg_user = res_mig_user['result_msg']
	result_count_user = res_mig_user['result_count']
	
	#Celulas
	#res_mig_cell = Mig().mig_groups()

	#result_msg_cells = res_mig_cell['result_msg']
	#result_count_cells = res_mig_cell['result_count']


	#Celulas x Funcoes
	#res_mig_roles = Mig().mig_groups_roles()

	#result_msg_roles = res_mig_roles['result_msg']
	#result_count_roles = res_mig_roles['result_count']
	

	#Encontros
	#res_mig_meeting = Mig().mig_metting()

	#result_msg_mettings = res_mig_meeting['result_msg']
	#result_count_mettings = res_mig_meeting['result_count']	


	#Encontros x Presença
	#res_mig_meeting_presence = Mig().mig_metting_presence()

	#result_msg_mettings_presence = res_mig_meeting_presence['result_msg']
	#result_count_mettings_presence = res_mig_meeting_presence['result_count']	
	

	template = loader.get_template('prover.html')

	result_count = 'to model all'
	csv_data = 'to model all'

	
	content = {
		'result_msg_user' : result_msg_user,
		'result_count_user' : result_count_user,
		#'result_msg_cells' : result_msg_cells,
		#'result_count_cells' : result_count_cells,
		#'result_msg_roles' : result_msg_roles,
		#'result_count_roles' : result_count_roles,
		#'result_msg_mettings' : result_msg_mettings,
		#'result_count_mettings' : result_count_mettings,
		#'result_msg_mettings_presence' : result_msg_mettings_presence,
		#'result_count_mettings_presence' : result_count_mettings_presence,			
		'csv_data': csv_data

	}
	
	return HttpResponse(template.render(content, request))

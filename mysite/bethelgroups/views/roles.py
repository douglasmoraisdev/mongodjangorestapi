from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import HttpResponseForbidden
from bson.objectid import ObjectId
from django.urls import reverse

import uuid

from bethelgroups.models import *


def role_new(request):

	template = loader.get_template('home/role/role_new.html')

	content = {
		'Users': Users.objects,
		'Groups': Groups.objects,
		'Groups_types': Groups_types.objects,
		'Roles': Roles.objects,
		'Events': Events.objects,        
	}


	if request.method == 'POST':

		role_name = request.POST.get('nome_funcao')
		role_code = request.POST.get('codigo_funcao')		

		role = Roles()

		role.add_role(role_name, role_code)

		return HttpResponse(template.render(content, request))

	else:

		return HttpResponse(template.render(content, request))
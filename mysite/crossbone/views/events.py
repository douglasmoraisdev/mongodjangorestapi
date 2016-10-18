from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import HttpResponseForbidden
from bson.objectid import ObjectId
from django.urls import reverse

import uuid

from crossbone.models import *


def event(request):

    template = loader.get_template('home/event/event.html')


    content = {
        'Users': Users.objects,
        'Groups': Groups.objects,
        'Groups_types': Groups_types.objects,
        'Roles': Roles.objects,
        'Events': Events.objects,        
    }

    return HttpResponse(template.render(content, request))

def event_new(request):

	template = loader.get_template('home/event/event_new.html')

	content = {
		'Users': Users.objects,
		'Groups': Groups.objects,
		'Groups_types': Groups_types.objects,
		'Roles': Roles.objects,
		'Events': Events.objects,        
	}

	if request.method == 'POST':

		document_group_origin, document_group_acima, document_group_abaixo = None, [], []
		document_group_roles, document_group_users, document_group_users_roles = [], [], []
		group_users = []
		group_users_hashs = []
		group_roles = []
		user_roles = []
		event_name = request.POST.get('nome-evento')
		group_origin = request.POST.get('grupo-origem-evento')

		
		users_group_input_names = [name for name in request.POST.keys() if name.startswith('user-group')]
		for input_name in users_group_input_names:
			group_users.append(request.POST.get(input_name))
			group_users_hashs = input_name.replace('user-group','')
			group_roles.append(request.POST.getlist('group-role'+group_users_hashs+'-multiple'))

		if group_origin:
			document_group_origin = Groups.objects.get(id=ObjectId(group_origin))

		if group_users:
			for key, users in enumerate(group_users):
				if users != '':
					document_group_users.append(Users.objects.get(id=ObjectId(group_users[key])))					


					for roles in group_roles[key]:
						document_group_roles.append(Roles.objects.get(id=ObjectId(roles)))

					document_group_users_roles.append(document_group_roles)
					document_group_roles = []		

		for key, user in enumerate(document_group_users):

			for role in document_group_users_roles[key]:
				user_roles.append(User_roles(user=user, role=role))

		evento = Events()
		evento.add_event(document_group_origin, user_roles, {'name':event_name})

		return HttpResponse('evento ok')    

	else:

		return HttpResponse(template.render(content, request))        

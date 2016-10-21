from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import HttpResponseForbidden
from bson.objectid import ObjectId
from django.urls import reverse

import uuid

from crossbone.models import *


def event(request, event_id):

	template = loader.get_template('home/event/event.html')

	events = Events()
	events = events.get_event_by_id(event_id)

	group_id = ObjectId(events.host.id)
	
	group = Groups()
	group = group.get_group_by_id(group_id)

	group_type_id = group.group_type.id
	group_type = Groups_types()
	group_type = group_type.get_grouptype_by_id(ObjectId(group_type_id))

	users = events.get_event_users(event_id)

	users_count = len(users)
	content = {
		'group_name':group.extra_data['name']['value'],
		'group_type':group_type.name,
		'users_list':users,
		'users_count': users_count,
		'event_date':events.extra_data['name']['value'],
		'event_name': events.extra_data['name']['value'],
		'event_data': events.extra_data

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
		document_group_tasks = []
		document_group_users_tasks = []		
		group_users = []
		user_hash = []
		ut = []
		group_tasks = []
		group_roles = []
		user_roles = []
		event_name = request.POST.get('nome-evento')
		group_origin = request.POST.get('grupo-origem-evento')

		
		users_group_input_names = [name for name in request.POST.keys() if name.startswith('user-group')]
		for input_name in users_group_input_names:
			group_users.append(request.POST.get(input_name))
			user_hash = input_name.replace('user-group','')
			group_roles.append(request.POST.getlist('group-role'+user_hash+'-multiple'))

			#Tasks per user
			tasks_input_names = [name for name in request.POST.keys() if name.startswith('user-task'+user_hash)]
			for task_input_name in tasks_input_names:
				task_hash = task_input_name.replace('user-task'+user_hash,'')
				ut.append(request.POST.get('user-task'+user_hash+task_hash))

			group_tasks.append(ut)
			ut = []			

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

					for tasks in group_tasks[key]:
						document_group_tasks.append(Tasks.objects.get(id=ObjectId(tasks)))

					document_group_users_tasks.append(document_group_tasks)
					document_group_tasks = []
															

		for key, user in enumerate(document_group_users):
			user_roles.append(User_roles(user=user, role=document_group_users_roles[key], task=document_group_users_tasks[key]))


		extra_data = dict({
			'name': event_name,
		})

		evento = Events()
		evento.add_event(document_group_origin, user_roles, 'start', 'end', {'name':event_name})

		return HttpResponse('evento ok')    

	else:

		return HttpResponse(template.render(content, request))        

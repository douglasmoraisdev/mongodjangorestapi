from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import HttpResponseForbidden
from bson.objectid import ObjectId
from django.urls import reverse

import uuid

from bethelgroups.models import *


def event(request, event_id):

	template = loader.get_template('home/event/event.html')

	group_name = ''
		
	events = Events()
	events = events.get_event_by_id(event_id)

	if events.host:
		group_id = ObjectId(events.host.id)
	else:
		group_id = None
	
	if group_id:
		group = Groups()
		group = group.get_group_by_id(group_id)
		group_name = group.name

	users = events.get_event_users(event_id)
	users_count = len(users)
	

	content = {
		'event_name': events.name,
		'group_origin_name': group_name,
		'users_list': users,
		'users_count': users_count,
		'start_date': events.start_date,
		'end_date': events.end_date,
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
		'Events_types': Events_types.objects,
	}

	if request.method == 'POST':

		document_group_origin = None
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
		event_type = request.POST.get('tipo-evento')

		
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
		evento.add_event(name=event_name, 
				  host=document_group_origin,
				  parent_event='',
				  groups_in=[],
				  event_type=event_type,
				  user_roles=user_roles,
				  start_date='date_start', 
				  end_date='date_end',
				  recorrent='S',
				  extra_data={})		

		return HttpResponse('evento ok')    

	else:

		return HttpResponse(template.render(content, request))        



def new_course(request):

	template = loader.get_template('home/event/course/event_new_course.html')

	content = {
		'Users': Users.objects,
		'Groups': Groups.objects,
		'Groups_types': Groups_types.objects,
		'Roles': Roles.objects,
		'Events': Events.objects,        
	}

	if request.method == 'POST':

		document_group_origin = None
		document_group_roles, document_group_users, document_group_users_roles = [], [], []
		document_group_tasks = []
		document_group_users_tasks = []		
		group_users = []
		user_hash = []
		ut = []
		group_tasks = []
		group_roles = []
		user_roles = []


		course_name = request.POST.get('nome-curso')
		course_origin = request.POST.get('curso-origem')		
		group_origin = request.POST.get('grupo-origem')		
		groups_included =  request.POST.getlist('grupos-incluidos-multiple')
		date_start = request.POST.get('data-inicio')
		date_end = request.POST.get('data-fim')
		recorrent = request.POST.get('curso-recorrente')
		course_value = request.POST.get('curso-valor')
		course_tax_period = request.POST.get('curso-cobranca')

		extra_data = {'value':course_value, 'tax_period':course_tax_period}
		
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


		course_type_id = Events_types.objects(code='course')[0].id


		evento = Events()
		evento.add_event(name=course_name, 
				  host=document_group_origin,
				  parent_event=course_origin,
				  groups_in=groups_included,
				  event_type=course_type_id,
				  user_roles=user_roles,
				  start_date=date_start, 
				  end_date=date_end,
				  recorrent=recorrent,
				  extra_data=extra_data)

		return HttpResponse('evento ok')    

	else:

		return HttpResponse(template.render(content, request))        


def course(request, event_id):

	template = loader.get_template('home/event/course/event_course.html')
	
	
	events = Events()
	events = events.get_event_by_id(event_id)

	group_id = ObjectId(events.host.id)
	
	group = Groups()
	group = group.get_group_by_id(group_id)

	users = events.get_event_users(event_id)
	users_count = len(users)
	

	content = {
		'course_name': events.name,
		'group_origin_name': group.name,
		'users_list': users,
		'users_count': users_count,
		'start_date': events.start_date,
		'end_date': events.end_date,
		'event_data': events.extra_data
	}

	return HttpResponse(template.render(content, request))


def new_subject(request):

	template = loader.get_template('home/event/course/event_new_course_subject.html')

	content = {
		'Users': Users.objects,
		'Groups': Groups.objects,
		'Groups_types': Groups_types.objects,
		'Roles': Roles.objects,
		'Events': Events.objects,        
	}

	if request.method == 'POST':

		document_group_origin = None
		document_group_roles, document_group_users, document_group_users_roles = [], [], []
		document_group_tasks = []
		document_group_users_tasks = []		
		group_users = []
		user_hash = []
		ut = []
		group_tasks = []
		group_roles = []
		user_roles = []

		subject_name = request.POST.get('disciplina-nome')
		course_origin = request.POST.get('curso-origem-disciplina')
		date_start = request.POST.get('data-inicio')
		date_end = request.POST.get('data-fim')
		classes_day = request.POST.getlist('disciplina-dias-multiple')
		subject_value = request.POST.get('disciplina-valor')

		extra_data = {'value':subject_value, 'classes_day':classes_day}
		
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


		subject_name = request.POST.get('disciplina-nome')
		course_origin = request.POST.get('curso-origem-disciplina')
		date_start = request.POST.get('data-inicio')
		date_end = request.POST.get('data-fim')

		evento = Events()
		evento.add_event(name=subject_name, 
				  parent_event=course_origin,
				  event_type='',
				  user_roles=user_roles,
				  start_date=date_start, 
				  end_date=date_end,
				  extra_data=extra_data)

		return HttpResponse('evento ok')    

	else:

		return HttpResponse(template.render(content, request))        

def subject(request, event_id):

	template = loader.get_template('home/event/course/event_course_subject.html')
	
	
	subject = Events()
	subject = subject.get_event_by_id(event_id)

	course = Events()
	course = course.get_event_by_id(subject.parent_event.id)	

	users = subject.get_event_users(event_id)
	users_count = len(users)
	

	content = {
		'subject_name': subject.name,
		'course_name': course.name,
		'users_list': users,
		'users_count': users_count,
		'start_date': subject.start_date,
		'end_date': subject.end_date,
		'event_data': subject.extra_data
	}

	return HttpResponse(template.render(content, request))

def stepper(request):

	template = loader.get_template('home/tests/stepper.html')

	content = {
		'dale': 'nosmeio'
	}

	return HttpResponse(template.render(content, request))
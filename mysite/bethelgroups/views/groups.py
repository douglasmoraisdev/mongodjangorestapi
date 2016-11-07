from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import HttpResponseForbidden
from bson.objectid import ObjectId
from django.urls import reverse

import uuid

from bethelgroups.models import *

import logging

logger = logging.getLogger(__name__)



def group(request, group_id):

	template = loader.get_template('home/group/group.html')

	leader_users = []
	host_users = []
	member_users = []
	visitor_users = []
	user_already_listed = []

	group_id = ObjectId(group_id)
	
	group = Groups()
	group = group.get_group_by_id(group_id)

	group_type_id = group.group_type.id
	group_type = Groups_types()
	group_type = group_type.get_grouptype_by_id(ObjectId(group_type_id))

	users = group.get_group_users(group_id)

	for key, user_list in enumerate(users):
		for role in user_list.role:

			if user_list.user.id not in user_already_listed:
				if role.code == 'leader':
					leader_users.append(user_list)
					user_already_listed.append(user_list.user.id)

				if role.code == 'host':
					host_users.append(user_list)
					user_already_listed.append(user_list.user.id)

				if role.code == 'cell_member':
					member_users.append(user_list)
					user_already_listed.append(user_list.user.id)

				if role.code == 'visitor':
					visitor_users.append(user_list)
					user_already_listed.append(user_list.user.id)


	events = Events()
	events = events.get_events_by_group_id(group_id)

	meetings = Events()
	meetings = meetings.get_meetings_by_group_id(group_id)

	generated_groups = Groups()
	generated_groups = generated_groups.get_groups_generetad(group_id)

	users_count = len(users)
	content = {
		'group_name':group.name,
		'group_type':group_type.name,
		'groups_over':group.groups_over,
		'groups_under':group.groups_under,
		'group_origin':group.origin,
		'generated_groups': generated_groups,
		'leader_users' : leader_users,
		'host_users' : host_users,
		'member_users' : member_users,
		'visitor_users' : visitor_users,
		'meetings' : meetings,
		'users_count': users_count,
		'group_data':group.extra_data,
		'events':events
	}


	
	return HttpResponse(template.render(content, request))



def group_new(request):

	template = loader.get_template('home/group/group_new.html')


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
		group_roles = []
		ut = []
		group_tasks = []
		user_roles = []
		group_name = request.POST.get('nome-grupo')
		group_date = request.POST.get('group-date')
		group_type = request.POST.get('tipo-grupo')
		group_origin = request.POST.get('grupo-origem')
		groups_over = request.POST.getlist('grupos-acima-multiple')
		groups_under = request.POST.getlist('grupos-abaixo-multiple')
		
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

		if groups_over:
			for gruposa in groups_over:
				document_group_acima.append(Groups.objects.get(id=ObjectId(gruposa)))

		if groups_under:
			for gruposb in groups_under:
				document_group_abaixo.append(Groups.objects.get(id=ObjectId(gruposb)))

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
			'created_on_date': group_date
		})

		group = Groups()
		group.add_group(group_name, group_type, document_group_origin, document_group_acima, document_group_abaixo, user_roles, extra_data)


		return HttpResponse('ok')

	else:

		return HttpResponse(template.render(content, request))




def cell_new(request):

	template = loader.get_template('home/group/cells/cell_new.html')


	content = {
		'Users': Users.objects,
		'Groups': Groups.objects,
		'Groups_types': Groups_types.objects,
		'Roles': Roles.objects,
		'Events': Events.objects,
	}


	if request.method == 'POST':

		group_origin = None
		groups_over = None
		groups_under = None
		servant_roles = []
		members_roles = []
		user_roles = []
		days_list = []
		hours_list = []
		#user_obj
		#roles_add 		
		roles_obj = []

		cell_name = request.POST.get('cell-name')
		cell_date = request.POST.get('cell-date')
		cell_zip = request.POST.get('cell-zip')
		cell_state = request.POST.get('cell-state')
		cell_city = request.POST.get('cell-city')
		cell_neigh = request.POST.get('cell-neigh')
		cell_street = request.POST.get('cell-street')
		cell_street_number = request.POST.get('cell-street-number')
		cell_days = request.POST.getlist('cell-days-multiple[]')
		cell_hours = request.POST.getlist('cell-hours[]')
		user_added = request.POST.getlist('user-added[]')
		roles_added = request.POST.getlist('roles-added[]')
		member_added = request.POST.getlist('member-added[]')
		group_origin = request.POST.get('group-origin')
		groups_up_multiple = request.POST.getlist('groups-up-multiple')
		groups_down_multiple = request.POST.getlist('groups-down-multiple')
		

		days_input_names = [name for name in request.POST.keys() if name.startswith('cell-days-multiple-')]
		for input_name in days_input_names:
			days_list.append(request.POST.getlist(input_name))
			seq_hash = input_name.replace('cell-days-multiple-','')
			hours_list.append(request.POST.get('cell-hours-'+seq_hash))


		#servants added get list
		for key, users in enumerate(user_added):
			user_obj =	Users.objects.get(id=ObjectId(users))

			for roles in roles_added[key].split(","):

				roles_add = Roles.objects.get(id=ObjectId(roles))
				roles_obj.append(roles_add)

			servant_roles.append(User_roles(user=user_obj, role=roles_obj))

			roles_obj = []


		#members added get list
		member_role = Roles.objects.get(code="cell_member")
		for key, users in enumerate(member_added):
			user_obj =	Users.objects.get(id=ObjectId(users))

			members_roles.append(User_roles(user=user_obj, role=[member_role]))


		#join servants and users
		for servants in servant_roles:
			user_roles.append(servants)

		for members in members_roles:
			user_roles.append(members)


		#extra data formater
		extra_data = dict({
			'created_on_date': cell_date,
			'addr_zip' : cell_zip,
			'addr_state': cell_state,
			'addr_city': cell_city,
			'addr_neigh' : cell_neigh,
			'addr_street' : cell_street,
			'addr_street_number' : cell_street_number,
			'meet_day':days_list,
			'meet_hour':hours_list
		})		


		cell = Groups()
		cell.add_cell(
			name=cell_name,
			group_origin=group_origin,
			groups_over=groups_over,
			groups_under=groups_under,
			user_roles=user_roles,
			extra_data=extra_data
			)
		

		return HttpResponse('ok')

	else:

		return HttpResponse(template.render(content, request))


def grouptype_new(request):

	template = loader.get_template('home/group/grouptype_new.html')

	content = {
		'Users': Users.objects,
		'Groups': Groups.objects,
		'Groups_types': Groups_types.objects,
		'Roles': Roles.objects,
		'Events': Events.objects,        
	}

	if request.method == 'POST':
		
		type_group_code = request.POST.get('codigo_tipo_grupo')
		type_group_name = request.POST.get('nome_tipo_grupo')		

		group_type = Groups_types()

		group_type.add_group_type(type_group_code, type_group_name)

	else:

		return HttpResponse(template.render(content, request))

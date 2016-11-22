from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import HttpResponseForbidden
from bson.objectid import ObjectId
from django.urls import reverse

import uuid

from bethelgroups.models import *

import logging

logger = logging.getLogger(__name__)



def cell(request, group_id):

	template = loader.get_template('home/group/cells/cell.html')

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
		'group_id':group.id,
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
		'cell_id':group_id,
		'events':events
	}


	
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


def cell_edit(request, group_id):

	template = loader.get_template('home/group/cells/cell_edit.html')

	cell_members = []
	cell_leaders = []

	group = Groups()
	group_users = group.get_group_users(group_id)	

	for user in group_users:
		for codes in user.role:
			if 'cell_member' == codes.code:
				cell_members.append(user)
			elif codes.code in ['leader', 'host']:
				cell_leaders.append(user)

	content = {
		'Users': Users.objects,
		'cell_members': cell_members,
		'cell_leaders': cell_leaders,		
		'Groups': Groups.objects,
		'Groups_types': Groups_types.objects,
		'Roles': Roles.objects,
		'Events': Events.objects,
		'cell_data': Groups.objects.get(id=group_id)
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
		cell.edit_cell(
			cell_id=group_id,
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

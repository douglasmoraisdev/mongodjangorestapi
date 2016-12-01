from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import HttpResponseForbidden
from django.urls import reverse
from bson.objectid import ObjectId

import uuid

from bethelgroups.models import *


def cell_metting(request, event_id):

	template = loader.get_template('app/event/cell_metting/cell_metting.html')

	group_name = ''
	member_maps = []
		
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
	

	# Members data for maps
	tested_user_id = []
	for usersA in users:

		#Verify same address users
		for usersB in users:

			if (usersA.user.id != usersB.user.id):
				if (usersB.user.id not in tested_user_id):				
					if (usersA.user.extra_data['addr_lat'] == usersB.user.extra_data['addr_lat']) and (usersA.user.extra_data['addr_lng'] == usersB.user.extra_data['addr_lng']):

						tested_user_id.append(usersA.user.id)
						tested_user_id.append(usersB.user.id)
						logger.error('Mesmo endereço: %s e %s' % (usersA.user.extra_data['first_name'], usersB.user.extra_data['first_name']))

						addr_maps_info = {
							'users' : [usersA, usersB]
						}

						member_maps.append(addr_maps_info)

		#Add other members no duplied
		if (usersA.user.id not in tested_user_id):

			addr_maps_info = {
				'users' : [usersA]
			}

			member_maps.append(addr_maps_info)	

	content = {
		'event_name': events.name,
		'group_origin_name': group_name,
		'group_origin_id': group_id,
		'users_list': users,
		'users_count': users_count,
		'start_date': events.start_date,
		'end_date': events.end_date,
		'event_data': events.extra_data,
		'event_id':events.id,
		'member_maps' : member_maps
	}

	return HttpResponse(template.render(content, request))


def cell_metting_new(request, group_id):

	template = loader.get_template('app/event/cell_metting/cell_metting_new.html')

	group_metting_name = ''
	group_metting_id = ''

	group = Groups()
	group = group.get_group_by_id(group_id)

	if group.id:
		group_metting_name = group.name
		group_metting_id = group.id

	content = {
		'Users': Users.objects,
		'Groups': Groups.objects,
		'Groups_types': Groups_types.objects,
		'Roles': Roles.objects,
		'Events': Events.objects,
		'cell_members': Users.objects,
		'group_metting_name' : group_metting_name,
		'group_id':group_metting_id
	}


	if request.method == 'POST':


		document_group_origin = None
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

		group_origin = request.POST.get('group-origin')

		metting_cell_name = request.POST.get('metting-cell-name')
		metting_cell_date = request.POST.get('metting-cell-date')
		metting_cell_start_hour = request.POST.get('metting-cell-start-hour')
		metting_cell_end_hour = request.POST.get('metting-cell-end-hour')
		metting_has_offer = request.POST.get('metting-has-offer')
		metting_offer_value = request.POST.get('offer-value')
		metting_has_children = request.POST.get('metting-has-children')
		metting_children_qtd = request.POST.get('metting-children-qtd')
		metting_resume = request.POST.get('metting-resume')

		user_added = request.POST.getlist('user-added[]')
		roles_added = request.POST.getlist('roles-added[]')
		member_added = request.POST.getlist('member_presence[]')
		

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


		if group_origin:
			document_group_origin = Groups.objects.get(id=ObjectId(group_origin))

		#join servants and users
		for servants in servant_roles:
			user_roles.append(servants)

		for members in members_roles:
			user_roles.append(members)


		#extra data formater
		extra_data = dict({
			'start_hour': metting_cell_start_hour,
			'end_hour' : metting_cell_end_hour,
			'has_offer': metting_has_offer,
			'offer_value': metting_offer_value,
			'has_children' : metting_has_children,
			'children_qtd' : metting_children_qtd,
			'resume' : metting_resume
		})

		id_cell_metting_type = Events_types.objects(code='meeting')[0].id

		evento = Events()
		evento.add_event(name=metting_cell_name, 
				  parent_event='',
				  host=document_group_origin,
				  event_type=id_cell_metting_type,
				  user_roles=user_roles,
				  start_date=metting_cell_date, 
				  end_date=metting_cell_date,
				  extra_data=extra_data)

		return HttpResponse('ok')

	else:

		return HttpResponse(template.render(content, request))


def cell_metting_edit(request, group_id, event_id):

	template = loader.get_template('app/event/cell_metting/cell_metting_edit.html')

	group_metting_name = ''
	group_metting_id = ''

	group = Groups()
	group = group.get_group_by_id(group_id)

	events = Events()
	events = events.get_event_by_id(event_id)

	event_users = events.get_event_users(event_id)

	if group.id:
		group_metting_name = group.name
		group_metting_id = group.id
		group_users = group.get_group_users(group_id)	


	event_leaders = []
	event_members = []

	for user in event_users:
		for codes in user.role:
			if 'cell_member' == codes.code:
				event_members.append(user)
			elif codes.code in ['leader', 'host']:
				event_leaders.append(user)		

	content = {
		'Users': Users.objects,
		'Groups': Groups.objects,
		'Groups_types': Groups_types.objects,
		'Roles': Roles.objects,
		'Events': Events.objects,
		'event_members': event_members,
		'event_leaders': event_leaders,		
		'group_metting_name' : group_metting_name,
		'event' : events,
		'event_id':group_metting_id
	}


	if request.method == 'POST':


		document_group_origin = None
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

		group_origin = request.POST.get('group-origin')

		metting_cell_name = request.POST.get('metting-cell-name')
		metting_cell_date = request.POST.get('metting-cell-date')
		metting_cell_start_hour = request.POST.get('metting-cell-start-hour')
		metting_cell_end_hour = request.POST.get('metting-cell-end-hour')
		metting_has_offer = request.POST.get('metting-has-offer')
		metting_offer_value = request.POST.get('offer-value')
		metting_has_children = request.POST.get('metting-has-children')
		metting_children_qtd = request.POST.get('metting-children-qtd')
		metting_resume = request.POST.get('metting-resume')

		user_added = request.POST.getlist('user-added[]')
		roles_added = request.POST.getlist('roles-added[]')
		member_added = request.POST.getlist('member_presence[]')
		

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


		if group_origin:
			document_group_origin = Groups.objects.get(id=ObjectId(group_origin))

		#join servants and users
		for servants in servant_roles:
			user_roles.append(servants)

		for members in members_roles:
			user_roles.append(members)


		#extra data formater
		extra_data = dict({
			'start_hour': metting_cell_start_hour,
			'end_hour' : metting_cell_end_hour,
			'has_offer': metting_has_offer,
			'offer_value': metting_offer_value,
			'has_children' : metting_has_children,
			'children_qtd' : metting_children_qtd,
			'resume' : metting_resume
		})

		id_cell_metting_type = Events_types.objects(code='meeting')[0].id

		evento = Events()
		evento.edit_event(
				  name=metting_cell_name, 
				  event_id=event_id,
				  parent_event='',
				  host=document_group_origin,
				  event_type=id_cell_metting_type,
				  user_roles=user_roles,
				  start_date=metting_cell_date, 
				  end_date=metting_cell_date,
				  extra_data=extra_data)

		return HttpResponse('ok')

	else:

		return HttpResponse(template.render(content, request))

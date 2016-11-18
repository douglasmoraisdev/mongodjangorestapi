from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import HttpResponseForbidden
from bson.objectid import ObjectId
from django.urls import reverse

import uuid

from bethelgroups.models import *


def cell_metting(request, event_id):

	template = loader.get_template('home/event/cell_metting/cell_metting.html')

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


def cell_metting_new(request):

	template = loader.get_template('home/event/cell_metting/cell_metting_new.html')


	content = {
		'Users': Users.objects,
		'Groups': Groups.objects,
		'Groups_types': Groups_types.objects,
		'Roles': Roles.objects,
		'Events': Events.objects,
		'cell_members': Users.objects
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

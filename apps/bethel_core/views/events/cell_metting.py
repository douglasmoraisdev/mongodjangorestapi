from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import HttpResponseForbidden
from django.urls import reverse
from bson.objectid import ObjectId
from bethel_core import utils

from bethel_core.decorators import *


import uuid

from bethel_core.models import *

@bethel_auth_required
def cell_metting(request, event_id, user_apps):

	template = loader.get_template('app/event/cell_metting/cell_metting.html')

	group_name = ''
	member_maps = []
		
	events = Events().get_event_by_id(event_id)

	user = Users().get_user_by_id(request.session['user_id'])

	if events.host:
		group_id = ObjectId(events.host.id)
	else:
		group_id = None
	
	if group_id:
		group = Groups().get_group_by_id(group_id)
		group_name = group.name

	users = events.get_event_users(event_id)
	users_count = len(users)
	
	member_maps = utils.get_users_geo(users)

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
		'member_maps' : member_maps,
		'User' : user,
		'Groups_perm' : user_apps['groups_perm'],
		'Events_perm' : user_apps['events_perm']		
	}

	return HttpResponse(template.render(content, request))

@bethel_auth_required
def cell_metting_new(request, group_id, user_apps):

	template = loader.get_template('app/event/cell_metting/cell_metting_new.html')

	group = Groups().get_group_by_id(group_id)

	servant = Groups().get_group_users(group_id, ['leader', 'host'])
	cell_members = Groups().get_group_users(group_id, ['cell_member'])

	content = {
		'Users': Users.objects,
		'Groups': Groups.objects,
		'Groups_types': Groups_types.objects,
		'Roles': Roles.objects(app_scope__in=["cell_metting"]),
		'Events': Events.objects,
		'cell_members': cell_members,
		'servant': servant,
		'group' : group,
	}


	if request.method == 'POST':

		document_group_origin = None
		group_origin = None
		servant_roles = []
		members_roles = []
		user_roles = []
		#user_obj
		#roles_add 		

		group_origin = group_id

		metting_cell_name = request.POST.get('metting-cell-name')
		metting_cell_date = request.POST.get('metting-cell-date')
		metting_cell_start_hour = request.POST.get('metting-cell-start-hour')
		metting_cell_end_hour = request.POST.get('metting-cell-end-hour')
		metting_has_offer = request.POST.get('metting-has-offer')
		metting_offer_value = request.POST.get('offer-value')
		metting_has_children = request.POST.get('metting-has-children')
		metting_children_qtd = request.POST.get('metting-children-qtd')
		metting_resume = request.POST.get('metting-resume')

		user_added = request.POST.getlist('servant_presence[]')
		roles_added = request.POST.getlist('roles-added[]')
		member_added = request.POST.getlist('member_presence[]')
		
		print(user_added)
		print(roles_added)

		servant_roles = utils.parse_users_multi_role(user_added, roles_added)
		members_roles = utils.parse_users_fixed_role(member_added, "cell_member")


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

		return HttpResponseRedirect(reverse('cell', args=(group_id,)))


	else:

		return HttpResponse(template.render(content, request))

@bethel_auth_required
def cell_metting_edit(request, group_id, event_id, user_apps):

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


	group_servant = Groups().get_group_users(group_id, ['leader', 'host'])
	group_members = Groups().get_group_users(group_id, ['cell_member'])
	
	present_servant = Events().get_event_users(event_id, ['leader', 'host'])
	present_members = Events().get_event_users(event_id, ['cell_member'])


	not_present_servant = [x for x in group_servant if x not in present_servant]
	not_present_members = [x for x in group_members if x not in present_members]

	content = {
		'Users': Users.objects,
		'Groups': Groups.objects,
		'Groups_types': Groups_types.objects,
		'Roles': Roles.objects(app_scope__in=["cell_metting"]),
		'Events': Events.objects,
		'group_metting_name' : group_metting_name,
		'event' : events,
		'event_id':group_metting_id,
		'present_servant' : present_servant,
		'not_present_servant' : not_present_servant,		
		'present_members' : present_members,
		'not_present_members' : not_present_members
	}


	if request.method == 'POST':


		document_group_origin = None
		group_origin = None
		servant_roles = []
		members_roles = []
		user_roles = []
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

		user_added = request.POST.getlist('servant_presence[]')
		roles_added = request.POST.getlist('roles-added[]')
		member_added = request.POST.getlist('member_presence[]')
		

		servant_roles = utils.parse_users_multi_role(user_added, roles_added)
		members_roles = utils.parse_users_fixed_role(member_added, "cell_member")

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

		return HttpResponseRedirect(reverse('cell_metting', args=(event_id,)))

	else:

		return HttpResponse(template.render(content, request))

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.utils.translation import *

from bethel_core import utils
from bethel_core.decorators import *

from cell.models import *

from bson.objectid import ObjectId

import uuid
import googlemaps



import logging

logger = logging.getLogger(__name__)


@bethel_auth_required
def cell(request, group_id, user_apps=''):

	# Google Maps Client
	#gmaps = googlemaps.Client(key='AIzaSyD1FfhbFJv88cNCVu5xcHBt0rw4eeJYQOk')

	#geocode_result = gmaps.geocode('2345 Avenida Adão Foques, Florida, Guaíba, Rio grande do Sul, Brasil')

	template = loader.get_template('cell.html')

	leader_users = []
	host_users = []
	member_users = []
	member_maps = []
	addr_maps_info = dict()
	visitor_users = []
	user_already_listed = []	

	user = Users().get_user_by_id(request.session['user_id'])

	group_id = ObjectId(group_id)
	
	group = Cells().get_group_by_id(group_id)

	group_type = group._cls

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

	member_maps = utils.get_users_geo(users)	

	events = Events().get_events_by_group_id(group_id)

	meetings = Events().get_meetings_by_group_id(group_id)

	generated_groups = Cells().get_groups_generetad(group_id)

	users_count = len(users)
	content = {
		'group_id':group.id,
		'group_name':group.name,
		'group_type':group_type,
		'groups_over':group.groups_over,
		'groups_under':group.groups_under,
		#'group_origin':group.origin,
		'generated_groups': generated_groups,
		'leader_users' : leader_users,
		'host_users' : host_users,
		'member_users' : member_users,
		'visitor_users' : visitor_users,
		'meetings' : meetings,
		'users_count': users_count,
		'group_data':group.extra_data,
		'cell_id':group_id,
		'events':events,
		'User' : user,		
		'member_maps' : member_maps,
		'Groups_perm' : user_apps['groups_perm'],
		'Events_perm' : user_apps['events_perm'],
		'System_perm' : user_apps['system_perm'],
	}
	
	return HttpResponse(template.render(content, request))


@bethel_auth_required
def cell_detail(request, group_id, user_apps=''):

	template = loader.get_template('cell_detail.html')

	leader_users = []
	host_users = []
	member_users = []
	member_maps = []
	addr_maps_info = dict()
	visitor_users = []
	user_already_listed = []	

	user = Users().get_user_by_id(request.session['user_id'])

	group_id = ObjectId(group_id)
	
	group = Cells().get_group_by_id(group_id)

	group_type = group._cls

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

	member_maps = utils.get_users_geo(users)	

	events = Events().get_events_by_group_id(group_id)

	meetings = Events().get_meetings_by_group_id(group_id)

	generated_groups = Cells().get_groups_generetad(group_id)

	#For report
	mettings_presence = Cells().get_cell_presence_graph(group_id)

	total_roles = Cells().get_total_roles(group_id)


	users_count = len(users)
	content = {
		'group_id':group.id,
		'group_name':group.name,
		'group_type':group_type,
		'groups_over':group.groups_over,
		'groups_under':group.groups_under,
		#'group_origin':group.origin,
		'generated_groups': generated_groups,
		'leader_users' : leader_users,
		'host_users' : host_users,
		'member_users' : member_users,
		'visitor_users' : visitor_users,
		'meetings' : meetings,
		'users_count': users_count,
		'group_data':group.extra_data,
		'cell_id':group_id,
		'events':events,
		'User' : user,		
		'member_maps' : member_maps,
		'Groups_perm' : user_apps['groups_perm'],
		'Events_perm' : user_apps['events_perm'],
		'System_perm' : user_apps['system_perm'],

		'presence_days' : mettings_presence['presence_days'],
		'presence_evolution' : mettings_presence['presence_evolution'],
		'roles_presence' : mettings_presence['roles_presence'],

		'total_roles' : total_roles
	}
	
	return HttpResponse(template.render(content, request))


#@bethel_auth_required(min_perm=[{'groups':'c'}, {'system':'c'}])
@bethel_auth_required
def cell_new(request, user_apps):

	template = loader.get_template('cell_new.html')


	content = {
		'Users': Users.objects,
		'Groups': Groups.objects,
		'Roles': Roles.objects(app_scope__in=["cell", "cell_metting"]),
		'Events': Events.objects,
	}


	if request.method == 'POST':

		group_origin = None
		groups_over = []
		groups_under = []
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
		meet_freq = request.POST.get('group-meeting-freq')
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

		servant_roles = utils.parse_users_multi_role(user_added, roles_added)
		members_roles = utils.parse_users_fixed_role(member_added, "cell_member")


		#join servants and users
		for servants in servant_roles:
			user_roles.append(servants)

		for members in members_roles:
			user_roles.append(members)

		for gu in groups_down_multiple:			
			groups_under.append(Groups.objects.get(id=gu))

		for go in groups_up_multiple:			
			groups_over.append(Groups.objects.get(id=go))	


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
			'meet_hour':hours_list,
			'meet_freq' : meet_freq

		})		


		cell = Cells()
		cell.add_group(
			name=cell_name,
			group_origin=group_origin,
			groups_over=groups_over,
			groups_under=groups_under,
			user_roles=user_roles,
			extra_data=extra_data
			)
		

		return HttpResponseRedirect(reverse('home'))

	else:

		return HttpResponse(template.render(content, request))


#@bethel_auth_required(min_perm=[{'groups':'w'}, {'system':'w'}])
@bethel_auth_required
def cell_edit(request, group_id, user_apps):

	template = loader.get_template('cell_edit.html')

	cell_members = []
	cell_leaders = []

	group = Cells()
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
		'Groups': Groups.objects(id__nin=[group_id]),
		'Roles': Roles.objects(app_scope__in=["cell", "cell_metting"]),
		'Events': Events.objects,
		'cell_data': Groups.objects.get(id=group_id),
		'group_id': group_id
	}

	if request.method == 'POST':

		group_origin = None
		groups_over = []
		groups_under = []
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
		meet_freq = request.POST.get('group-meeting-freq')
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


		servant_roles = utils.parse_users_multi_role(user_added, roles_added)
		members_roles = utils.parse_users_fixed_role(member_added, "cell_member")


		#join servants and users
		for servants in servant_roles:
			user_roles.append(servants)

		for members in members_roles:
			user_roles.append(members)


		for gu in groups_down_multiple:			
			groups_under.append(Groups.objects.get(id=gu))

		for go in groups_up_multiple:			
			groups_over.append(Groups.objects.get(id=go))			

		#extra data formater
		extra_data = dict({
			'created_on_date': cell_date,
			'addr_zip' : cell_zip,
			'addr_state': cell_state,
			'addr_city': cell_city,
			'addr_neigh' : cell_neigh,
			'addr_street' : cell_street,
			'addr_street_number' : cell_street_number,
			'meet_day' : days_list,
			'meet_hour' : hours_list,
			'meet_freq' : meet_freq
		})		


		cell = Cells()
		cell.edit_cell(
			cell_id=group_id,
			name=cell_name,
			group_origin=group_origin,
			groups_over=groups_over,
			groups_under=groups_under,
			user_roles=user_roles,
			extra_data=extra_data
			)
		
		return HttpResponseRedirect(reverse('cell', args=(group_id,)))

	else:

		return HttpResponse(template.render(content, request))

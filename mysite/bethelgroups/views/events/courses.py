from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import HttpResponseForbidden
from django.urls import reverse
from bson.objectid import ObjectId
from bethelgroups import utils

from bethelgroups.decorators import *


import uuid

from bethelgroups.models import *

@bethel_auth_required
def course(request, event_id, user_apps):

	template = loader.get_template('app/event/course/course.html')

	member_maps = []

	user = Users().get_user_by_id(request.session['user_id'])	
	
	subjects = Events()
	subjects = subjects.get_event_childs(event_id)
	
	events = Events()
	events = events.get_event_by_id(event_id)

	group_origin_name = ''
	if (events.host):
		group_id = ObjectId(events.host.id)
	
		group = Groups()
		group = group.get_group_by_id(group_id)
		group_origin_name = group.name

	users = events.get_event_users(event_id)
	users_count = len(users)	

	member_maps = utils.get_users_geo(users)

	content = {
		'Subjects': subjects,
		'event_id': event_id,
		'course_name': events.name,
		'group_origin_name': group_origin_name,
		'users_list': users,
		'users_count': users_count,
		'start_date': events.start_date,
		'end_date': events.end_date,
		'event_data': events.extra_data,
		'member_maps' : member_maps,
		'Users' : user,
		'Groups_perm' : user_apps['groups_perm'],
		'Events_perm' : user_apps['events_perm']		

	}

	return HttpResponse(template.render(content, request))

@bethel_auth_required
def course_new(request, user_apps):

	template = loader.get_template('app/event/course/course_new.html')

	content = {
		'Users': Users.objects,
		'Groups': Groups.objects,
		'Groups_types': Groups_types.objects,
		'Roles': Roles.objects(app_scope__in=["course"]),
		'Events': Events.objects,
	}


	if request.method == 'POST':

		group_origin = None
		document_group_origin = None
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

		course_name = request.POST.get('course-name')
		course_date_start = request.POST.get('course-date-start')
		course_date_end = request.POST.get('course-date-end')
		course_recorrent = request.POST.get('course-recorrent')
		course_days = request.POST.getlist('cell-days-multiple[]')
		course_hours = request.POST.getlist('cell-hours[]')
		user_added = request.POST.getlist('user-added[]')
		roles_added = request.POST.getlist('roles-added[]')
		member_added = request.POST.getlist('member-added[]')
		group_origin = request.POST.get('group-origin')		

		days_input_names = [name for name in request.POST.keys() if name.startswith('cell-days-multiple-')]
		for input_name in days_input_names:
			days_list.append(request.POST.getlist(input_name))
			seq_hash = input_name.replace('cell-days-multiple-','')
			hours_list.append(request.POST.get('cell-hours-'+seq_hash))


		servant_roles = utils.parse_users_multi_role(user_added, roles_added)
		members_roles = utils.parse_users_fixed_role(member_added, "student")


		#join servants and users
		for servants in servant_roles:
			user_roles.append(servants)

		for members in members_roles:
			user_roles.append(members)


		#extra data formater
		extra_data = dict({
			'created_on_date': course_date_start,
			'meet_day':days_list,
			'meet_hour':hours_list
		})		

		course_type_id = Events_types.objects(code='course')[0].id

		course = Events()
		course.add_event(
				  name=course_name, 
				  host=document_group_origin,
				  parent_event=None,
				  groups_in=None,
				  event_type=course_type_id,
				  user_roles=user_roles,
				  start_date=course_date_start, 
				  end_date=course_date_end,
				  recorrent=course_recorrent,
				  extra_data=extra_data)
		

		return HttpResponseRedirect(reverse('home'))


	else:

		return HttpResponse(template.render(content, request))

@bethel_auth_required     
def course_edit(request, course_id, user_apps):

	template = loader.get_template('app/event/course/course_edit.html')

	events = Events()
	events = events.get_event_by_id(course_id)

	event_users = events.get_event_users(course_id)

	event_leaders = []
	event_members = []

	for user in event_users:
		for codes in user.role:
			if 'cell_member' == codes.code:
				event_members.append(user)
			elif codes.code in ['leader', 'host', 'teacher']:
				event_leaders.append(user)	

	content = {
		'Users': Users.objects,
		'Groups': Groups.objects,
		'Groups_types': Groups_types.objects,
		'Roles': Roles.objects(app_scope__in=["course"]),
		'event': events,
		'event_id': course_id,
		'event_users' : event_users,
		'event_members': event_members,
		'event_leaders': event_leaders		
	}

	if request.method == 'POST':

		group_origin = None
		document_group_origin = None
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

		course_name = request.POST.get('course-name')
		course_date_start = request.POST.get('course-date-start')
		course_date_end = request.POST.get('course-date-end')
		course_recorrent = request.POST.get('course-recorrent')
		course_days = request.POST.getlist('cell-days-multiple[]')
		course_hours = request.POST.getlist('cell-hours[]')
		user_added = request.POST.getlist('user-added[]')
		roles_added = request.POST.getlist('roles-added[]')
		member_added = request.POST.getlist('member-added[]')
		group_origin = request.POST.get('group-origin')		

		days_input_names = [name for name in request.POST.keys() if name.startswith('cell-days-multiple-')]
		for input_name in days_input_names:
			days_list.append(request.POST.getlist(input_name))
			seq_hash = input_name.replace('cell-days-multiple-','')
			hours_list.append(request.POST.get('cell-hours-'+seq_hash))


		servant_roles = utils.parse_users_multi_role(user_added, roles_added)
		members_roles = utils.parse_users_fixed_role(member_added, "student")


		#join servants and users
		for servants in servant_roles:
			user_roles.append(servants)

		for members in members_roles:
			user_roles.append(members)


		#extra data formater
		extra_data = dict({
			'created_on_date': course_date_start,
			'meet_day':days_list,
			'meet_hour':hours_list
		})		

		course_type_id = Events_types.objects(code='course')[0].id

		course = Events()
		course.edit_event(
				  event_id=course_id,
				  name=course_name, 
				  host=document_group_origin,
				  parent_event=None,
				  event_type=course_type_id,
				  user_roles=user_roles,
				  start_date=course_date_start, 
				  end_date=course_date_end,
				  recorrent=course_recorrent,
				  extra_data=extra_data)
		

		return HttpResponseRedirect(reverse('course', args=(course_id,)))


	else:

		return HttpResponse(template.render(content, request))
     
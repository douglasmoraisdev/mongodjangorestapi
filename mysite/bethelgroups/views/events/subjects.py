from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import HttpResponseForbidden
from django.urls import reverse
from bson.objectid import ObjectId
from bethelgroups import utils


import uuid

from bethelgroups.models import *


def subject(request, event_id):

	template = loader.get_template('app/event/subject/subject.html')
	
	member_maps = []	

	subject = Events()
	subject = subject.get_event_by_id(event_id)

	course = Events()
	course = course.get_event_by_id(subject.parent_event.id)	

	users = subject.get_event_users(event_id)
	users_count = len(users)
	
	member_maps = utils.get_users_geo(users)

	content = {
		'subject': subject,
		'course': course,
		'users_list': users,
		'users_count': users_count,
		'start_date': subject.start_date,
		'end_date': subject.end_date,
		'event_data': subject.extra_data,
		'member_maps' : member_maps
	}

	return HttpResponse(template.render(content, request))


def subject_new(request, course_id):

	template = loader.get_template('app/event/subject/subject_new.html')

	course = Events.objects.get(id=course_id)

	content = {
		'Users': Users.objects,
		'Groups': Groups.objects,
		'Groups_types': Groups_types.objects,
		'Roles': Roles.objects,
		'course' : course
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

		subject_name = request.POST.get('subject-name')
		subject_date_start = request.POST.get('subject-date-start')
		subject_date_end = request.POST.get('subject-date-end')
		subject_days = request.POST.getlist('cell-days-multiple[]')
		subject_hours = request.POST.getlist('cell-hours[]')
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
		members_roles = utils.parse_users_fixed_role(member_added, "cell_member")


		#join servants and users
		for servants in servant_roles:
			user_roles.append(servants)

		for members in members_roles:
			user_roles.append(members)


		#extra data formater
		extra_data = dict({
			'created_on_date': subject_date_start,
			'meet_day':days_list,
			'meet_hour':hours_list
		})		

		subject_type_id = Events_types.objects(code='subject')[0].id

		course = Events()
		course.add_event(
				  name=subject_name, 
				  host=document_group_origin,
				  parent_event=course_id,
				  groups_in=None,
				  event_type=subject_type_id,
				  user_roles=user_roles,
				  start_date=subject_date_start, 
				  end_date=subject_date_end,
				  recorrent='N',
				  extra_data=extra_data)
		

		return HttpResponse('ok')

	else:

		return HttpResponse(template.render(content, request))
     


def subject_edit(request, course_id, subject_id):

	template = loader.get_template('app/event/subject/subject_edit.html')

	subject = Events.objects.get(id=subject_id)

	course = Events.objects.get(id=course_id)


	events = Events()
	events = events.get_event_by_id(subject_id)	

	event_users = events.get_event_users(subject_id)

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
		'Roles': Roles.objects,
		'subject' : subject,
		'course' : course,
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

		subject_name = request.POST.get('subject-name')
		subject_date_start = request.POST.get('subject-date-start')
		subject_date_end = request.POST.get('subject-date-end')
		subject_days = request.POST.getlist('cell-days-multiple[]')
		subject_hours = request.POST.getlist('cell-hours[]')
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
		members_roles = utils.parse_users_fixed_role(member_added, "cell_member")


		#join servants and users
		for servants in servant_roles:
			user_roles.append(servants)

		for members in members_roles:
			user_roles.append(members)


		#extra data formater
		extra_data = dict({
			'created_on_date': subject_date_start,
			'meet_day':days_list,
			'meet_hour':hours_list
		})		

		subject_type_id = Events_types.objects(code='subject')[0].id

		course = Events()
		course.edit_event(
				  event_id=subject_id,
				  parent_event=course_id,
				  name=subject_name, 
				  host=document_group_origin,
				  groups_in=None,
				  event_type=subject_type_id,
				  user_roles=user_roles,
				  start_date=subject_date_start, 
				  end_date=subject_date_end,
				  recorrent='N',
				  extra_data=extra_data)
		

		return HttpResponse('ok')

	else:

		return HttpResponse(template.render(content, request))

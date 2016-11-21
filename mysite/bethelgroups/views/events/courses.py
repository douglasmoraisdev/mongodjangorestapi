from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import HttpResponseForbidden
from bson.objectid import ObjectId
from django.urls import reverse

import uuid

from bethelgroups.models import *


def course(request, event_id):

	template = loader.get_template('home/event/course/course.html')
	
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
	

	content = {
		'Subjects': subjects,
		'course_name': events.name,
		'group_origin_name': group_origin_name,
		'users_list': users,
		'users_count': users_count,
		'start_date': events.start_date,
		'end_date': events.end_date,
		'event_data': events.extra_data
	}

	return HttpResponse(template.render(content, request))



def course_new(request):

	template = loader.get_template('home/event/course/course_new.html')

	content = {
		'Users': Users.objects,
		'Groups': Groups.objects,
		'Groups_types': Groups_types.objects,
		'Roles': Roles.objects,
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
		

		return HttpResponse('ok')

	else:

		return HttpResponse(template.render(content, request))
     


def subject(request, event_id):

	template = loader.get_template('home/event/subject/subject.html')
	
	
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


def subject_new(request, course_id):

	template = loader.get_template('home/event/subject/subject_new.html')

	content = {
		'Users': Users.objects,
		'Groups': Groups.objects,
		'Groups_types': Groups_types.objects,
		'Roles': Roles.objects,
		'Events': Events.objects.get(id=course_id),
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
			'created_on_date': course_date_start,
			'meet_day':days_list,
			'meet_hour':hours_list
		})		

		course_type_id = Events_types.objects(code='course')[0].id

		course = Events()
		course.add_event(
				  name=course_name, 
				  host=document_group_origin,
				  parent_event=course_id,
				  groups_in=None,
				  event_type=course_type_id,
				  user_roles=user_roles,
				  start_date=course_date_start, 
				  end_date=course_date_end,
				  recorrent='N',
				  extra_data=extra_data)
		

		return HttpResponse('ok')

	else:

		return HttpResponse(template.render(content, request))
     
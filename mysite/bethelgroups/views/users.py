from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import HttpResponseForbidden
from bson.objectid import ObjectId
from django.urls import reverse

import json
import time

import os
import binascii

from bethelgroups.models import *


def user(request, user_id):

	template = loader.get_template('home/user/user.html') 

	user_id = ObjectId(user_id)
	
	user = Users()
	user = user.get_user_by_id(user_id)

	groups = Groups()
	groups = groups.get_user_groups(user_id)

	events = Events()
	events = events.get_user_events(user_id)

	courses = Events()
	courses = courses.get_user_courses(user_id)

	content = {
		'User':user,
		'Groups':groups,
		'Events':events,
		'Courses':courses
	}
	
	return HttpResponse(template.render(content, request))


def user_new(request):

	template = loader.get_template('home/user/user_new.html')

	content = {
		'Users': Users.objects,
		'Groups': Groups.objects,
		'Groups_types': Groups_types.objects,
		'Roles': Roles.objects,
		'Events': Events.objects,
	}	

	if request.method == 'POST':

		first_name = request.POST.get('nome_usuario')

		user_name = request.POST.get('user-name')
		user_pass = request.POST.get('user-pass')
	
		auth_type = 'password'
		auth_token = user_pass

		user = Users()
		user.add_user(
				user_name = user_name,
				auth_type = auth_type,
				auth_token = auth_token,
				extra_data={'first_name':first_name}
			)

		return HttpResponse(template.render(content, request))

	else:

		return HttpResponse(template.render(content, request))

#ajax
def usuarios_roles_list(request):

	content = {
		'Users': Users.objects,
		'Roles': Roles.objects,
		'fields_seq' : binascii.hexlify(os.urandom(4))
	}	

	template = loader.get_template('default/usuarios_roles_list.html')

	return HttpResponse(template.render(content,request))	


#ajax
def usuarios_tasks_list(request, fields_seq):

	content = {
		'Users': Users.objects,
		'Tasks': Tasks.objects,
		'fields_seq' : fields_seq,
		'task_seq' : binascii.hexlify(os.urandom(4))

	}	

	template = loader.get_template('default/usuarios_tasks_list.html')

	return HttpResponse(template.render(content,request))



#ajax
def get_servant_autocomplete(request):

	user_list = dict()

	search = request.GET.get('send')

	content = {
		'users_result': Users.objects(extra_data__first_name__icontains=search) #TODO mover como função do Model
	}	

	template = loader.get_template('home/group/cells/modals/servant_item_list_search.html')

	return HttpResponse(template.render(content,request))	

#ajax
def add_servant_list(request):

	user_list = dict()

	user_id = request.GET.get('userid');
	roles_ids = request.GET.getlist('rolesid[]');

	user_selected = Users.objects(id=user_id)[0] #TODO mover como função nos Models
	roles_selected = Roles.objects(id__in=roles_ids)

	content = {
		'user_name': user_selected,
		'user_roles' : roles_selected,
		'user_id': user_id,
		'roles_ids': roles_ids,
	}	

	template = loader.get_template('home/group/cells/modals/servant_item_list_add.html')

	return HttpResponse(template.render(content,request))

#ajax
def get_member_autocomplete(request):

	user_list = dict()

	search = request.GET.get('send')

	content = {
		'users_result': Users.objects(extra_data__first_name__icontains=search) #TODO mover como função do Model
	}	

	template = loader.get_template('home/group/cells/modals/member_item_list_search.html')

	return HttpResponse(template.render(content,request))	

#ajax
def add_member_list(request):


	user_list = dict()

	user_id = request.GET.get('userid');
	roles_ids = request.GET.getlist('rolesid[]');

	user_selected = Users.objects(id=user_id)[0] #TODO mover como função nos Models
	roles_selected = Roles.objects(id__in=roles_ids)

	content = {
		'user_name': user_selected,
		'user_roles' : roles_selected,
		'user_id': user_id,
		'roles_ids': roles_ids,
	}	

	template = loader.get_template('home/group/cells/modals/member_item_list_add.html')

	return HttpResponse(template.render(content,request))	


#ajax
def day_group_hmtl_frag(request):

	content = {
		'day_seq' : binascii.hexlify(os.urandom(4))
	}	

	template = loader.get_template('default/add_group_day_frag.html')

	return HttpResponse(template.render(content,request))		

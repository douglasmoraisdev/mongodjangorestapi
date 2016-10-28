from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import HttpResponseForbidden
from bson.objectid import ObjectId
from django.urls import reverse

import os
import binascii

from crossbone.models import *


def user(request, user_id):

	template = loader.get_template('home/user/user.html') 

	user_id = ObjectId(user_id)
	
	user = Users()
	user = user.get_user_by_id(user_id)

	content = {
		'user':user
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

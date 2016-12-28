from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import HttpResponseForbidden
from bson.objectid import ObjectId
from django.urls import reverse
from django.contrib import messages
from django.conf import settings

from bethel_core.decorators import *


from bethel_core.models import *

import logging
import uuid


logger = logging.getLogger(__name__)

@bethel_auth_required
def index(request, user_apps):


	template = loader.get_template('index.html')

	user_id = request.session['user_id']

	user = Users().get_user_by_id(user_id)

	user_courses = Events().get_user_courses(user_id)

	#update user perms
	user_perms = Permissions().get_user_perms(ObjectId(user_id))
	request.session['user_perms'] = user_perms


	content = {
		'user_name': user.user_name,
		'User' : user,
		'Roles': Roles.objects,        
		'Groups': user_apps['groups_obj'],
		'Events': user_apps['events_obj'],
		'Groups_perm' : user_apps['groups_perm'],
		'Events_perm' : user_apps['events_perm'],
		'Courses': user_courses,
	}
	return HttpResponse(template.render(content, request))


def loginLogout(request):

	template = loader.get_template('login.html')

	if (request.method == 'POST') and (request.POST.get('action') != 'logout'):

		user_name = request.POST.get('user-name')
		password = request.POST.get('user-pass')
		user_perms = dict()

		user = Users()

		user_id = user.is_auth(user_name, password)

		if user_id == False:

			messages.error(request, u'Usuário e/ou senha inválidos')
			return HttpResponse(template.render('', request))
			
		else:

			user_perms = Permissions().get_user_perms(user_id)

			request.session['user_id'] = str(user_id)
			request.session['user_perms'] = user_perms
			return HttpResponseRedirect('/bethel_core/')
		
	else:

		try:
			del request.session['user_id']
			messages.error(request, u'Efetue login novamente para entrar')
		except:
			pass

		return HttpResponse(template.render('', request))


@bethel_auth_required(min_perm=[{'system':'+'}])
def global_search(request, searchquery, user_apps):

	content = {
		'result': 'resultados',
	}


	template = loader.get_template('globalsearch_results.html')

	return HttpResponse(template.render(content, request))

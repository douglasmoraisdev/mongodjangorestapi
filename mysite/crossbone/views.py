from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseForbidden
from bson.objectid import ObjectId
import uuid

from crossbone.models import *

import logging


logger = logging.getLogger(__name__)


def index(request):

    logger.error('debug Something went wrong!')

    template = loader.get_template('home/index.html')


    content = {
        'Users': Users.objects,
        'Groups': Groups.objects,
        'Groups_types': Groups_types.objects,
        'Roles': Roles.objects,
        'Events': Events.objects,        
    }
    return HttpResponse(template.render(content, request))


def loginLogout(request):

    template = loader.get_template('home/login.html')


    content = {
        'Users': Users.objects,
        'Groups': Groups.objects,
        'Groups_types': Groups_types.objects,
        'Roles': Roles.objects,
        'Events': Events.objects,        
    }

    return HttpResponse(template.render(content, request))


def group(request):

    template = loader.get_template('home/group.html')


    content = {
        'Users': Users.objects,
        'Groups': Groups.objects,
        'Groups_types': Groups_types.objects,
        'Roles': Roles.objects,
        'Events': Events.objects,        
    }

    return HttpResponse(template.render(content, request))


def group_new(request):

    template = loader.get_template('home/group_new.html')


    content = {
        'Users': Users.objects,
        'Groups': Groups.objects,
        'Groups_types': Groups_types.objects,
        'Roles': Roles.objects,
        'Events': Events.objects,        
    }

    return HttpResponse(template.render(content, request))

def user_new(request):

    template = loader.get_template('home/user_new.html')


    content = {
        'Users': Users.objects,
        'Groups': Groups.objects,
        'Groups_types': Groups_types.objects,
        'Roles': Roles.objects,
        'Events': Events.objects,        
    }

    return HttpResponse(template.render(content, request))


def role_new(request):

    template = loader.get_template('home/role_new.html')


    content = {
        'Users': Users.objects,
        'Groups': Groups.objects,
        'Groups_types': Groups_types.objects,
        'Roles': Roles.objects,
        'Events': Events.objects,        
    }

    return HttpResponse(template.render(content, request))


def grouptype_new(request):

    template = loader.get_template('home/grouptype_new.html')


    content = {
        'Users': Users.objects,
        'Groups': Groups.objects,
        'Groups_types': Groups_types.objects,
        'Roles': Roles.objects,
        'Events': Events.objects,        
    }

    return HttpResponse(template.render(content, request))    


def event(request):

    template = loader.get_template('home/event.html')


    content = {
        'Users': Users.objects,
        'Groups': Groups.objects,
        'Groups_types': Groups_types.objects,
        'Roles': Roles.objects,
        'Events': Events.objects,        
    }

    return HttpResponse(template.render(content, request))    


    
def novogrupo(request):

	if request.method == 'POST':


		document_group_origin, document_group_acima, document_group_abaixo = None, [], []
		document_group_roles, document_group_users, document_group_users_roles = [], [], []
		group_users = []
		group_users_hashs = []
		group_roles = []
		user_roles = []
		group_name = request.POST.get('nome-grupo')
		group_type = request.POST.get('tipo-grupo')
		group_origin = request.POST.get('grupo-origem')
		groups_over = request.POST.getlist('grupos-acima-multiple')
		groups_under = request.POST.getlist('grupos-abaixo-multiple')
		
		users_group_input_names = [name for name in request.POST.keys() if name.startswith('user-group')]
		for input_name in users_group_input_names:
			group_users.append(request.POST.get(input_name))
			group_users_hashs = input_name.replace('user-group','')
			group_roles.append(request.POST.getlist('user-role'+group_users_hashs+'-multiple'))

		if group_origin:
			document_group_origin = Groups.objects.get(id=ObjectId(group_origin))

		if groups_over:
			for gruposa in groups_over:
				document_group_acima.append(Groups.objects.get(id=ObjectId(gruposa)))

		if groups_under:
			for gruposb in groups_under:			
				document_group_abaixo.append(Groups.objects.get(id=ObjectId(gruposb)))

		if group_users:
			for key, users in enumerate(group_users):
				if users != '':
					document_group_users.append(Users.objects.get(id=ObjectId(group_users[key])))					


					for roles in group_roles[key]:
						document_group_roles.append(Roles.objects.get(id=ObjectId(roles)))

					document_group_users_roles.append(document_group_roles)
					document_group_roles = []		

		for key, user in enumerate(document_group_users):


			for role in document_group_users_roles[key]:
				user_roles.append(User_roles(user=user, role=role))

		group = Groups.objects.create(
			group_type=[group_type],
			origin=document_group_origin,
			groups_over=document_group_acima,
			groups_under=document_group_abaixo,
			user_roles = user_roles,			
			data={'name':group_name}
		)

		return HttpResponse('abc')


	else:
		return HttpResponseForbidden()

def novouser(request):

	if request.method == 'POST':

		user_name = request.POST.get('nome_usuario')

		user = Users()

		user.add_user(user_name)

		return HttpResponse('Feito!')

	else:
		return HttpResponseForbidden()

def novorole(request):

	if request.method == 'POST':

		role_name = request.POST.get('nome_funcao')

		role = Roles()

		role.add_role(role_name)

		return HttpResponse('Feito!')

	else:
		return HttpResponseForbidden()	

def novogrouptype(request):

	if request.method == 'POST':

		type_group_code = request.POST.get('codigo_tipo_grupo')
		type_group_name = request.POST.get('nome_tipo_grupo')		

		group_type = Groups_types()

		group_type.add_group_type(type_group_code, type_group_name)

		return HttpResponse('Feito!')

	else:
		return HttpResponseForbidden()

def newevent(request):

	if request.method == 'POST':

		document_group_origin, document_group_acima, document_group_abaixo = None, [], []
		document_group_roles, document_group_users, document_group_users_roles = [], [], []
		group_users = []
		group_users_hashs = []
		group_roles = []
		user_roles = []
		event_name = request.POST.get('nome-grupo-evento')
		group_origin = request.POST.get('grupo-origem-evento')

		
		users_group_input_names = [name for name in request.POST.keys() if name.startswith('user-group')]
		for input_name in users_group_input_names:
			group_users.append(request.POST.get(input_name))
			group_users_hashs = input_name.replace('user-group','')
			group_roles.append(request.POST.getlist('user-role'+group_users_hashs+'-multiple'))

		if group_origin:
			document_group_origin = Groups.objects.get(id=ObjectId(group_origin))

		if group_users:
			for key, users in enumerate(group_users):
				if users != '':
					document_group_users.append(Users.objects.get(id=ObjectId(group_users[key])))					


					for roles in group_roles[key]:
						document_group_roles.append(Roles.objects.get(id=ObjectId(roles)))

					document_group_users_roles.append(document_group_roles)
					document_group_roles = []		

		for key, user in enumerate(document_group_users):

			for role in document_group_users_roles[key]:
				user_roles.append(User_roles(user=user, role=role))

		evento = Events()

		evento.add_event(document_group_origin, user_roles, {'name':event_name})

		return HttpResponse(request)


	else:
		return HttpResponseForbidden()		

#ajax
def usuarios_roles_list(request):

	content = {
		'Users': Users.objects,
		'Roles': Roles.objects,
		'fields_seq' : uuid.uuid1()
	}	

	template = loader.get_template('default/usuarios_roles_list.html')

	return HttpResponse(template.render(content,request))
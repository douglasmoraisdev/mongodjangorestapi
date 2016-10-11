from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseForbidden

from crossbone.models import *

def index(request):
    template = loader.get_template('home/index.html')


    content = {
        'Users': Users.objects,
        'Groups': Groups.objects,
        'Groups_types': Groups_types.objects,
        'Roles': Roles.objects,
        'Events': Events.objects,        
    }
    return HttpResponse(template.render(content, request))
    
    
def contact(request):
    
    template = loader.get_template('contact/contact.html')
    
    return HttpResponse(template.render('',request))


def novogrupo(request):

	if request.method == 'POST':
		nome_grupo = request.POST.get('nome_grupo')

		userrole1 = User_roles(user=Users.objects[0], role=Roles.objects[0])
		userrole2 = User_roles(user=Users.objects[1], role=Roles.objects[1])
		#group_child = Groups.objects[0]

		#grupo = Groups.objects.create(
		#	group_type=['Celula', 'Rede'],
		#	user_roles= [userrole1, userrole2],
		#	data={'nome':nome_grupo}
		#)

		#grupo = Groups.objects.create(
		#		group_type=['Celula', 'Rede'],
		#		user_roles= [userrole1],
		#		group_roles= group_child
		#	)



		#grupo.save()

		return HttpResponse('Feito!')

	else:
		return HttpResponseForbidden()

def novouser(request):

	if request.method == 'POST':

		nome_usuario = request.POST.get('nome_usuario')

		user = Users.objects.create(
			name = nome_usuario
		)

		user.save()

		return HttpResponse('Feito!')

	else:
		return HttpResponseForbidden()	

def novorole(request):

	if request.method == 'POST':

		nome_funcao = request.POST.get('nome_funcao')

		role = Roles.objects.create(
			name = nome_funcao
		)

		role.save()

		return HttpResponse('Feito!')

	else:
		return HttpResponseForbidden()	

def novogrouptype(request):

	if request.method == 'POST':

		codigo_tipo_grupo = request.POST.get('codigo_tipo_grupo')
		nome_tipo_grupo = request.POST.get('nome_tipo_grupo')		

		group_type = Groups_types.objects.create(
			code = codigo_tipo_grupo,
			name = nome_tipo_grupo
		)

		group_type.save()

		return HttpResponse('Feito!')

	else:
		return HttpResponseForbidden()	
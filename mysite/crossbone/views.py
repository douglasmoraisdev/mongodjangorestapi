from django.http import HttpResponse
from django.template import loader

from crossbone.models import *

def index(request):
    template = loader.get_template('home/index.html')
    context = {
        'item': 'dale',
    }
    return HttpResponse(template.render(context, request))
    
    
def contact(request):
    
    template = loader.get_template('contact/contact.html')
    
    return HttpResponse(template.render('',request))


def novogrupo(request):

	userrole1 = User_roles(user=Users.objects[0], role=Roles.objects[0])
	userrole2 = User_roles(user=Users.objects[1], role=Roles.objects[1])
	group_child = Groups.objects[0]

	#grupo = Groups.objects.create(
	#	group_type=['Celula', 'Rede'],
	#	user_roles= [userrole1, userrole2]
	#)

	grupo = Groups.objects.create(
			group_type=['Celula', 'Rede'],
			user_roles= [userrole1],
			group_roles= group_child
		)



	grupo.save()

	return HttpResponse('Criado com sucesso!')

def novouser(request):
	user = Users.objects.create(
		name = 'Altair'
	)

	user.save()

	return HttpResponse('Criado com sucesso!')	

def novorole(request):

	roles = Roles.objects.create(
		name = 'Anfitriao'
	)

	roles.save()

	return HttpResponse('Criado com sucesso!')

def userrole(request):	

	userroles = User_roles.objects.create(
		user = Users.objects[1],
		role = Roles.objects[1]
	)

	userroles.save()

	return HttpResponse('Criado com sucesso!')			

def visualizar(request):

	employee_list = Groups.objects.all()

	group_name = []

	for a in employee_list:
		group_name.append(a.name)

	return HttpResponse('lista de grupos %s' % group_name)


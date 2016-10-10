from django.http import HttpResponse
from django.template import loader

from crossbone.models import Groups

def index(request):
    template = loader.get_template('home/index.html')
    context = {
        'item': 'dale',
    }
    return HttpResponse(template.render(context, request))
    
    
def contact(request):
    
    template = loader.get_template('contact/contact.html')
    
    return HttpResponse(template.render('',request))


def novo(request):
	#employee = Employee.objects.create(
	#		email='teste@email.com',
	#		first_name='Joao',
	#		last_name='Morais'
	#	)

	#employee.save()

	grupo = Groups.objects.create(
		email='contact@gmail.com',
		name='Celula da Alvorada',
		tipo='Celula'
	)

	grupo.save()

	return HttpResponse('Criado com sucesso!')


def empregados(request):

	employee_list = Groups.objects.all()

	group_name = []

	for a in employee_list:
		group_name.append(a.email)

	return HttpResponse('lista de empregados %s' % group_name)


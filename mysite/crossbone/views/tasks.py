from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import HttpResponseForbidden
from bson.objectid import ObjectId
from django.urls import reverse

from crossbone.models import *


def task_new(request):

	template = loader.get_template('home/task/task_new.html')

	content = {
		'Users': Users.objects,
		'Groups': Groups.objects,
		'Groups_types': Groups_types.objects,
		'Roles': Roles.objects,
		'Events': Events.objects,        
	}


	if request.method == 'POST':

		task_name = request.POST.get('task_name')

		task = Tasks()

		task.add_task(task_name)

		return HttpResponse(template.render(content, request))

	else:

		return HttpResponse(template.render(content, request))
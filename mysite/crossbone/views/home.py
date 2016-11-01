from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import HttpResponseForbidden
from bson.objectid import ObjectId
from django.urls import reverse
from django.contrib import messages

import uuid

from crossbone.models import *

import logging


logger = logging.getLogger(__name__)


def index(request):

    if ('user_id' in request.session):
        if (request.session['user_id'] != ''):

            template = loader.get_template('home/index.html')

            user_id = request.session['user_id']

            user = Users().get_user_by_id(user_id)

            user_groups = Groups().get_user_groups_by_type(user_id)
            user_events = Events().get_user_events_by_type(user_id)
            user_courses = Events().get_user_courses(user_id)


            content = {
                'user_name': user.user_name,
                'Groups': user_groups,
                'Roles': Roles.objects,
                'Events': user_events,
                'Courses': user_courses,
                'baseurl': request.get_full_path
            }
            return HttpResponse(template.render(content, request))

        else:
            return HttpResponseRedirect('/crossbone/login')
    else:
        return HttpResponseRedirect('/crossbone/login')

def loginLogout(request):

    template = loader.get_template('home/login.html')

    if (request.method == 'POST') and (request.POST.get('action') != 'logout'):

        user_name = request.POST.get('user-name')
        password = request.POST.get('user-pass')

        user = Users()

        user_id = user.is_auth(user_name, password)

        if user_id == False:

            messages.error(request, u'Usuário e/ou senha inválidos')

            return HttpResponse(template.render('', request))
            
        else:
            request.session['user_id'] = str(user_id)
            return HttpResponseRedirect('/crossbone/')
        
    else:

        try:
            del request.session['user_id']
            messages.error(request, u'Efetue login novamente para entrar')
        except:
            pass

        return HttpResponse(template.render('', request))


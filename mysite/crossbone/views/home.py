from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import HttpResponseForbidden
from bson.objectid import ObjectId
from django.urls import reverse

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



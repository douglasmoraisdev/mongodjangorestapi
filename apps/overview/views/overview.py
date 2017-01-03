from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import HttpResponseForbidden
from bson.objectid import ObjectId
from django.urls import reverse
from bethel_core import utils


import uuid
import googlemaps

from cell.models import *
from bethel_core.decorators import *

import logging

logger = logging.getLogger(__name__)

#@bethel_auth_required(min_perm=[{'system':'+'}])
bethel_auth_required
def home(request, user_apps=''):


	template = loader.get_template('overview.html')

	return HttpResponse(template.render([], request))

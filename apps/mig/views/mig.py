from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import HttpResponseForbidden
from bson.objectid import ObjectId
from django.urls import reverse
from bethel_core import utils

from django.utils.translation import *

import csv


import uuid
import googlemaps

from cell.models import *
from user.models import *

from bethel_core.decorators import *

import logging

logger = logging.getLogger(__name__)


def prover(request,  user_apps=''):


	result_msg = ''
	result_count = 0

	csv_data = []

	cvs_path = 'mig/static/upload/pessoas.csv'

	with open(cvs_path) as f:
		reader = csv.reader(f)

		for row in reader:

			csv_data.append([{
				'first_name' : row[4].replace(row[4].split(" ")[0],"", 1),
				'last_name' : row[4].replace(row[4].split(" ")[0],"", 1), #retira o primeiro nome do nom
				'user_name' : row[15]
			}])

	#Add to the Users Model

	for item in csv_data:

		name = '"'+item[0]['first_name']+'"'

		extra = dict()
		extra['last_name'] = item[0]['last_name']		
		extra['first_name'] = item[0]['first_name'],
		extra['other_key'] = name.replace(" ", "",1),
		extra['other_key2'] = 'banana'


		try:
			Users().add_user(
				user_name=item[0]['user_name'],

				auth_type='password',
				auth_token='abacate',
				extra_data = extra,
			)

			result_msg = 'Sucesso'
			result_count += 1
		except Exception as err:
			result_msg = format(err)


	template = loader.get_template('prover.html')



	
	content = {
		'result_msg' : result_msg,
		'result_count' : result_count,
		'csv_data': csv_data

	}
	
	return HttpResponse(template.render(content, request))

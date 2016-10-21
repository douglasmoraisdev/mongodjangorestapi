from django.db import models
from mongoengine import *
# Create your models here.

class Events_types(Document):
	code = StringField(max_length=50)
	name = StringField(max_length=50)
	extra_data = DictField()

	def add_event_type(self, code, name, extra_data=None):

		ex_data = dict()

		if extra_data:

			#empty 
			extra_data['description'] = extra_data['description'] if ('description' in extra_data) else ''

			ex_data = dict( 
				{'description':
					{'name':'Descrição','value': extra_data.description}

				}
			)			

		Events_types.objects.create(
			code=code,
			name=name,
			extra_data=ex_data
		)

	def get_eventtype_by_id(self, eventtype_id):

		return Events_types.objects.get(id=eventtype_id)
from django.db import models
from mongoengine import *
from crossbone.models.groups import *
# Create your models here.

class Events(Document):
	host = ReferenceField(Groups)
	event_roles = EmbeddedDocumentListField(User_roles)
	start_date = StringField(max_length=50)
	end_date = StringField(max_length=50)	
	extra_data = DictField()

	def add_event(self, host, event_roles, start_date, end_date, extra_data):

		ex_data = dict()

		if extra_data:

			#empty 
			extra_data['description'] = extra_data['description'] if ('description' in extra_data) else ''

			ex_data = dict( 
				{'description':
					{'name':'Descrição','value': extra_data.description}

				}
			)			

		Events.objects.create(
			host=host,
			start_date=start_date,
			end_date=end_date,
			event_roles = event_roles,			
			extra_data=ex_data
		)


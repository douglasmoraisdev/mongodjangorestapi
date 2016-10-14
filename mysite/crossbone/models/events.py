from django.db import models
from mongoengine import *
from crossbone.models.groups import *
# Create your models here.

class Events(Document):
	host = ReferenceField(Groups)
	event_roles = EmbeddedDocumentListField(User_roles)
	data = DictField()

	def add_event(self, host, event_roles, data):

		Events.objects.create(
			host=host,
			event_roles = event_roles,			
			data=data
		)


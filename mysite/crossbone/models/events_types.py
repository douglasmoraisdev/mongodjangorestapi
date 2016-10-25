from django.db import models
from mongoengine import *
# Create your models here.

class Events_types(Document):
	code = StringField(max_length=50)
	name = StringField(max_length=50)
	extra_data = DictField()

	def add_event_type(self, code, name, extra_data=None):

		Events_types.objects.create(
			code=code,
			name=name,
			extra_data=extra_data
		)

	def get_eventtype_by_id(self, eventtype_id):

		return Events_types.objects.get(id=eventtype_id)
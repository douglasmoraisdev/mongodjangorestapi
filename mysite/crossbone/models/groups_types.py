from django.db import models
from mongoengine import *
# Create your models here.


class Groups_types(Document):
	code = StringField(max_length=50)
	name = StringField(max_length=50)

	def add_group_type(self, code, name):
		Groups_types.objects.create(
			code=code,
			name=name
		)
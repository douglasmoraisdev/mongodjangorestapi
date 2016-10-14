from django.db import models
from mongoengine import *
# Create your models here.

class Roles(Document):
	name = StringField(max_length=50)
	data = DictField()

	def add_role(self, role_name):
		Roles.objects.create(
			name = role_name
		)	

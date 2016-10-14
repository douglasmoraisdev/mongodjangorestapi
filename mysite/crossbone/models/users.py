from django.db import models
from mongoengine import *
from crossbone.models.roles import *

# Create your models here.

class Users(Document):
	name = StringField(max_length=50)
	data = DictField()

	def add_user(self, user_name):
		Users.objects.create(
			name = user_name
		)	

class User_roles(EmbeddedDocument):
	user = ReferenceField(Users)
	role = ReferenceField(Roles)		
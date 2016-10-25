from django.db import models
from mongoengine import *
from crossbone.models.roles import *
from crossbone.models.tasks import *


# Create your models here.

class Users(Document):

	name = StringField(max_length=50)
	auth = StringField(max_length=255)
	extra_data = DictField()

	def add_user(self, user_name, extra_data=None):

		Users.objects.create(
			name = user_name,
			extra_data = extra_data
			)

	def get_user_by_id(self, user_id):

		return Users.objects.get(id=user_id)


class User_roles(EmbeddedDocument):
	user = ReferenceField(Users)
	role = ListField(ReferenceField(Roles))
	task = ListField(ReferenceField(Tasks))
	extra_data = DictField()

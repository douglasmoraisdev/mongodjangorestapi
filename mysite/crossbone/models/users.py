from django.db import models
from mongoengine import *
from crossbone.models.roles import *
from crossbone.models.tasks import *


import logging

logger = logging.getLogger(__name__)

class Users(Document):

	user_name = StringField(max_length=50)
	auth_type = StringField(max_length=10) #facebook #google #password
	auth_token = StringField(max_length=255) #token or password
	extra_data = DictField()

	def add_user(self, user_name, auth_type, auth_token, extra_data=None):

		Users.objects.create(
			user_name = user_name,
			auth_type = auth_type,
			auth_token = auth_token,
			extra_data = extra_data
			)

	def get_user_by_id(self, user_id):

		return Users.objects.get(id=user_id)

	def is_auth(self, user_name, auth_token):

		user = Users.objects(user_name=user_name)


		if (user):
			if (user[0].auth_token == auth_token):
				return user[0].id

		return False



class User_roles(EmbeddedDocument):
	user = ReferenceField(Users)
	role = ListField(ReferenceField(Roles))
	task = ListField(ReferenceField(Tasks))
	extra_data = DictField()

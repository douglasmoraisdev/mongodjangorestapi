from django.db import models
from mongoengine import *
from bethel_core.models.roles import *
from bethel_core.models.tasks import *
from bethel_core.models.users import *


import logging

logger = logging.getLogger(__name__)

class Users(Users):

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

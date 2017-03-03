from django.db import models
from mongoengine import *
from core.models.roles import *
from core.models.tasks import *
from core.models.users import *


import logging

logger = logging.getLogger(__name__)

class BUsers(Users):

	def get_user_by_id(self, user_id):

		return Users.objects.get(id=user_id)

	def is_auth(self, user_name, auth_token):

		user = Users.objects(user_name=user_name)


		if (user):
			if (user[0].auth_token == auth_token):
				return user[0].id

		return False



class BUser_roles(EmbeddedDocument):
	user = ReferenceField(Users)
	role = ListField(ReferenceField(Roles))
	task = ListField(ReferenceField(Tasks))
	extra_data = DictField()

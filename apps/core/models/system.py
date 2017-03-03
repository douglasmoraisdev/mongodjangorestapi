from django.db import models
from mongoengine import *
from core.models.users import *


import logging

logger = logging.getLogger(__name__)


class System(Document):
	user_roles = EmbeddedDocumentListField(User_roles)


	def get_user_system_perms(self, user_id=''):

		# Get user system perms
		system = System.objects(user_roles__user=user_id)

		return system
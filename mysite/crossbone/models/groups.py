from django.db import models
from mongoengine import *
from crossbone.models.groups_types import *
from crossbone.models.users import *


import logging

logger = logging.getLogger(__name__)


class Groups(Document):
	group_type = ReferenceField(Groups_types)
	user_roles = EmbeddedDocumentListField(User_roles)
	data = DictField()
	origin = ReferenceField("self", reverse_delete_rule = NULLIFY)
	groups_over = ListField(ReferenceField("self", reverse_delete_rule = NULLIFY))
	groups_under = ListField(ReferenceField("self", reverse_delete_rule = NULLIFY))


	def add_group(self, data, group_type, group_origin, groups_over, groups_under, user_roles):

		Groups.objects.create(
			group_type=group_type,
			origin=group_origin,
			groups_over=groups_over,
			groups_under=groups_under,
			user_roles = user_roles,			
			data=data
		)

	def get_group_by_id(self, group_id):

		return Groups.objects.get(id=group_id)


	def get_group_users(self, group_id):

		user_roles = []

		group = Groups.objects.get(id=group_id)

		for users in group.user_roles:
			user_roles.append(users.user.name)

		return user_roles


		#query to get and separe users on group

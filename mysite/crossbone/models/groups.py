from django.db import models
from mongoengine import *
from crossbone.models.groups_types import *
from crossbone.models.users import *


import logging

logger = logging.getLogger(__name__)


class Groups(Document):
	name = StringField(max_length=50)
	group_type = ReferenceField(Groups_types)
	user_roles = EmbeddedDocumentListField(User_roles)
	origin = ReferenceField("self", reverse_delete_rule = NULLIFY)
	groups_over = ListField(ReferenceField("self", reverse_delete_rule = NULLIFY))
	groups_under = ListField(ReferenceField("self", reverse_delete_rule = NULLIFY))
	extra_data = DictField()


	def add_group(self, name, group_type, group_origin, groups_over, groups_under, user_roles, extra_data=None):

		Groups.objects.create(
			name=name,
			group_type=group_type,
			origin=group_origin,
			groups_over=groups_over,
			groups_under=groups_under,
			user_roles = user_roles,
			extra_data=extra_data
		)

	def get_group_by_id(self, group_id):

		return Groups.objects.get(id=group_id)


	def get_group_users(self, group_id):

		group = Groups.objects.get(id=group_id)

		return group.user_roles


	def get_user_groups(self, user_id):

		group = Groups.objects(user_roles__user=user_id)

		return group

from django.db import models
from mongoengine import *
from bethelgroups.models.groups_types import *
from bethelgroups.models.users import *


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

	def add_cell(self, name, group_origin, groups_over, groups_under, user_roles, extra_data=None):

		cell_type_id = Groups_types.objects(code='cell')[0]

		Groups.objects.create(
			name=name,
			group_type=cell_type_id,
			origin=group_origin,
			groups_over=groups_over,
			groups_under=groups_under,
			user_roles = user_roles,
			extra_data=extra_data
		)	


	def get_group_by_id(self, group_id):

		return Groups.objects.get(id=group_id)


	def get_groups_over_by_id(self, group_id):

		return Groups.objects.get(id=group_id)


	def get_groups_under_by_id(self, group_id):

		return Groups.objects.get(id=group_id)			


	def get_group_users(self, group_id, role=''):
		'''
		returns the user_roles of the groups by id
		params:
		role(optional): get by user role, eg: 'leaders or hosts'
		'''

		group = Groups.objects.get(id=group_id)

		return group.user_roles


	def get_user_groups(self, user_id):

		group = Groups.objects(user_roles__user=user_id)

		return group

	def get_user_groups_by_type(self, user_id):

		group = Groups.objects(user_roles__user=user_id)

		user_groups = dict()

		for key, gtype in enumerate(group):

			if gtype.group_type.code in user_groups:
				user_groups[gtype.group_type.code].append(group[key])
			else:
				user_groups[gtype.group_type.code] = [group[key]]



		return user_groups

	def get_groups_generetad(self, group_id):

		groups = Groups.objects(origin=group_id)

		return groups

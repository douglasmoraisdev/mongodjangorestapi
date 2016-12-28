from django.db import models
from mongoengine import *
from bethel_core.models.users import *


import logging

logger = logging.getLogger(__name__)


class Groups(Document):
	meta = {'allow_inheritance': True}
	name = StringField(max_length=50)
	user_roles = EmbeddedDocumentListField(User_roles)
	origin = ReferenceField("self", reverse_delete_rule = NULLIFY)
	groups_over = ListField(ReferenceField("self", reverse_delete_rule = NULLIFY))
	groups_under = ListField(ReferenceField("self", reverse_delete_rule = NULLIFY))
	extra_data = DictField()


	def add_user_group(self, user_roles, group_id):

		Groups.objects.filter(id=group_id).update(
			add_to_set__user_roles = user_roles
		)

	'''
		REMOVE DATA METHODS
	'''
	def remove_user_group(self, user, group_id):

		Groups.objects.filter(id=group_id).update(pull__user_roles__user=user[0].user)

	'''
		EDIT DATA METHODS		
	'''

	def edit_cell(self, cell_id, name, group_origin, groups_over, groups_under, user_roles=None, extra_data=None):


		Groups.objects.filter(id=cell_id).update(
			name=name,
			origin=group_origin,
			groups_over=groups_over,
			groups_under=groups_under,
			user_roles = user_roles,
			extra_data=extra_data
		)	

	'''
		GET DATA METHODS		
	'''

	def get_all(self, search):
		
		return Groups.objects(name__icontains=search)


	def get_group_by_id(self, group_id):

		return Groups.objects.get(id=group_id)


	def get_groups_over_by_id(self, group_id):

		return Groups.objects.get(id=group_id)


	def get_groups_under_by_id(self, group_id):

		return Groups.objects.get(id=group_id)			


	def get_group_users(self, group_id, role=None):
		'''
		returns the user_roles of the groups by id
		params:
		role(optional): get by user role, eg: 'leaders or hosts'
		'''
		user_list = []
		group = Groups.objects.get(id=group_id)

		if (role != None):
			for us in group.user_roles:
				for rl in us.role:
					if rl.code in role:
						user_list.append(us)

			return user_list


		return group.user_roles


	def get_user_groups(self, user_id):

		group = Groups.objects(user_roles__user=user_id)

		return group

	def get_user_groups_by_type(self, user_id='', get_childs=False):
		'''
			return a list of groups-type separated
		'''

		groups_under = []

		# Get user groups
		groups = Groups.objects(user_roles__user=user_id)

		user_groups = dict()

		for key, gtype in enumerate(groups):

			if gtype._cls in user_groups:
				user_groups[gtype._cls].append(groups[key])
			else:
				user_groups[gtype._cls] = [groups[key]]


		# Get groups under (all groups that this group is over) IF get_childs == True
		if get_childs:
			groups_under = Groups.objects(groups_over__in=groups)

			for key, gtype in enumerate(groups_under):

				if gtype._cls in user_groups:
					user_groups[gtype._cls].append(groups_under[key])
				else:
					user_groups[gtype._cls] = [groups_under[key]]				

		return user_groups

	def get_user_groups_by_role(self, user_id, role_code):

		group = Groups.objects(user_roles__user=user_id)

		user_groups = dict()

		for key, gtype in enumerate(group):

			if gtype._cls in user_groups:
				user_groups[gtype._cls].append(group[key])
			else:
				user_groups[gtype._cls] = [group[key]]



		return user_groups		

	def get_groups_generetad(self, group_id):

		groups = Groups.objects(origin=group_id)

		return groups

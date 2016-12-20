from django.db import models
from mongoengine import *

from bethel_core.models.groups import *
from bethel_core.models.users import *
from bethel_core.models.roles import *
from cell_metting.models import *

import logging

logger = logging.getLogger(__name__)


class Cells(Groups):

	def add_group(self, name, group_origin, groups_over, groups_under, user_roles, extra_data=None):

		Cells.objects.create(
			name=name,
			origin=group_origin,
			groups_over=groups_over,
			groups_under=groups_under,
			user_roles = user_roles,
			extra_data=extra_data
		)

	def add_cell(self, name, group_origin, groups_over, groups_under, user_roles, extra_data=None):

		cell_type_id = Groups_types.objects(code='cell')[0]

		Cells.objects.create(
			name=name,
			#group_type=cell_type_id,
			origin=group_origin,
			groups_over=groups_over,
			groups_under=groups_under,
			user_roles = user_roles,
			extra_data=extra_data
		)

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

			if gtype.group_type.code in user_groups:
				user_groups[gtype.group_type.code].append(groups[key])
			else:
				user_groups[gtype.group_type.code] = [groups[key]]


		# Get groups under (all groups that this group is over) IF get_childs == True
		if get_childs:
			groups_under = Groups.objects(groups_over__in=groups)

			for key, gtype in enumerate(groups_under):

				if gtype.group_type.code in user_groups:
					user_groups[gtype.group_type.code].append(groups_under[key])
				else:
					user_groups[gtype.group_type.code] = [groups_under[key]]				

		return user_groups

	def get_user_groups_by_role(self, user_id, role_code):

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



	'''
		REPORT LEVEL DATA
	'''

	def get_cell_presence(self, group_id):

		report = dict()

		servants_count = dict()
		members_count = dict()

		presence = []

		leader_id = Roles.objects(code='leader')[0].id
		host_id = Roles.objects(code='host')[0].id

		member_id = Roles.objects(code='cell_member')[0].id

		metting = Cell_mettings.objects(host=group_id)
	
		for item in metting:
			for rl in item.user_roles:
				for cd in rl.role:
					presence.append({item.start_date:cd.code})
				


		print(presence)	

		report['servants'] = servants_count
		report['members'] = members_count		


		return report


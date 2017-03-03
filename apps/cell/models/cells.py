from django.db import models
from mongoengine import *
from collections import Counter


from core.models.groups import *
from core.models.users import *
from core.models.roles import *
from cell_metting.models import *

import logging

logger = logging.getLogger(__name__)


class Cells(Groups):

	def add_cell(self, name, cell_origin, cells_over, cells_under, user_roles, extra_data=None):

		Cells.objects.create(
			name=name,
			origin=cell_origin,
			cells_over=cells_over,
			cells_under=cells_under,
			user_roles = user_roles,
			extra_data=extra_data
		)



	def add_cell(self, mig_id, name, cell_origin, cells_over, cells_under, 
		user_roles, zipcode,  street,  street_number,  addr_obs,  neigh,  city,  state, 
	 	extra_data=None):

		#cell_type_id = Groups_types.objects(code='cell')[0]

		Cells.objects.create(
			mig_id = mig_id,
			name=name,
			#cell_type=cell_type_id,
			origin=cell_origin,
			cells_over=cells_over,
			cells_under=cells_under,
			user_roles = user_roles,
			
			zipcode = zipcode,
			street = street,
			street_number = street_number,
			addr_obs = addr_obs,
			neigh = neigh,
			city = city,
			state = state,

			extra_data=extra_data

		)

	'''
		REMOVE DATA METHODS
	'''
	def remove_user_cell(self, user, cell_id):

		Groups.objects.filter(id=cell_id).update(pull__user_roles__user=user[0].user)

	'''
		EDIT DATA METHODS		
	'''

	def edit_cell(self, cell_id, name, cell_origin, cells_over, cells_under, user_roles=None, extra_data=None):


		Groups.objects.filter(id=cell_id).update(
			name=name,
			origin=cell_origin,
			cells_over=cells_over,
			cells_under=cells_under,
			user_roles = user_roles,
			extra_data=extra_data
		)



	def get_cells_over_by_id(self, cell_id):

		return Groups.objects.get(id=cell_id)


	def get_cells_under_by_id(self, cell_id):

		return Groups.objects.get(id=cell_id)			


	def get_cell_users(self, cell_id, role=None):
		'''
		returns the user_roles of the cells by id
		params:
		role(optional): get by user role, eg: 'leaders or hosts'
		'''
		user_list = []
		cell = Groups.objects.get(id=cell_id)

		if (role != None):
			for us in cell.user_roles:
				for rl in us.role:
					if rl.code in role:
						user_list.append(us)

			return user_list


		return cell.user_roles


	def get_user_cells(self, user_id):

		cell = Groups.objects(user_roles__user=user_id)

		return cell

	def get_user_cells_by_type(self, user_id='', get_childs=False):
		'''
			return a list of cells-type separated
		'''

		cells_under = []

		# Get user cells
		cells = Groups.objects(user_roles__user=user_id)

		user_cells = dict()

		for key, gtype in enumerate(cells):

			if gtype.cell_type.code in user_cells:
				user_cells[gtype.cell_type.code].append(cells[key])
			else:
				user_cells[gtype.cell_type.code] = [cells[key]]


		# Get cells under (all cells that this cell is over) IF get_childs == True
		if get_childs:
			cells_under = Groups.objects(cells_over__in=cells)

			for key, gtype in enumerate(cells_under):

				if gtype.cell_type.code in user_cells:
					user_cells[gtype.cell_type.code].append(cells_under[key])
				else:
					user_cells[gtype.cell_type.code] = [cells_under[key]]				

		return user_cells

	def get_user_cells_by_role(self, user_id, role_code):

		cell = Groups.objects(user_roles__user=user_id)

		user_cells = dict()

		for key, gtype in enumerate(cell):

			if gtype.cell_type.code in user_cells:
				user_cells[gtype.cell_type.code].append(cell[key])
			else:
				user_cells[gtype.cell_type.code] = [cell[key]]



		return user_cells		

	def get_cells_generetad(self, cell_id):

		cells = Groups.objects(origin=cell_id)

		return cells



	'''
		REPORT LEVEL DATA
	'''

	def get_cell_presence_graph(self, cell_id):

		presence_evolution = []
		key_presence = []

		leader_presence = []
		member_presence = []
		visitor_presence = []

		report = dict()

		metting = Cell_mettings.objects(host=cell_id).order_by('start_date')

		#presence labels by day	
		for item in metting:
			servants_count = 0
			members_count = 0
			visitor_count = 0
			for rl in item.user_roles:
				for cd in rl.role:
					if cd.code == 'leader':
						servants_count += 1
					if cd.code == 'cell_member':
						members_count += 1
					if cd.code == 'visitor':
						visitor_count += 1


			presence_evolution.append({item.start_date : {'leader' : servants_count, 
														  'member' : members_count, 
														  'visitor' : visitor_count
														  }})

		for node in presence_evolution:

			#labels
			for key, value in enumerate(node):
				key_presence.append(value)

			# presence by role
			for item in node[value]:
				
				if 'leader' == item:
					leader_presence.append(node[value]['leader'])

				if 'member' == item:
					member_presence.append(node[value]['member'])

				if 'visitor' == item:
					visitor_presence.append(node[value]['visitor'])
								


		report['presence_days'] = key_presence
		report['presence_evolution'] = presence_evolution

		report['roles_presence'] = {'leader':leader_presence, 
									'member': member_presence,
									'visitor':visitor_presence
									}

		return report

	def get_total_roles(self, cell_id):

		cell = Cells.objects.get(id=cell_id)

		report = dict()
		
		servants_count = 0
		members_count = 0
		visitor_count = 0

		for roles in cell.user_roles:

			for rl in roles.role:
				if rl.code == 'leader':
					servants_count += 1

				if rl.code == 'cell_member':
					members_count += 1

				if rl.code == 'visitor':
					visitor_count += 1			


		report['leader'] = servants_count
		report['member'] = members_count
		report['visitor'] = visitor_count
		report['total_persons'] = cell.user_roles.count()

		return report
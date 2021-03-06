from django.db import models
from mongoengine import *
from core.models.roles import *
from core.models.tasks import *
from core.models.users import *
from core.models.roles import *



from cell.models import *

import logging

import csv

logger = logging.getLogger(__name__)

class Mig(models.Model):

	def mig_users(self):

		result_msg = ''
		result_count = 0

		csv_data = []

		cvs_path = 'mig/static/upload/pessoas.csv'

		with open(cvs_path) as f:
			reader = csv.reader(f, delimiter=',')

			iters = 0
			for row in reader:

				if iters > 0:				
					csv_data.append([{
						'mig_id' : row[0],

						'first_name' : row[4].split(" ")[0],
						'last_name' : row[4].replace(row[4].split(" ")[0],"", 1).strip(), #retira o primeiro nome do nom
						'user_name' : row[15],
						'cpf' : row[3],
						'birthday' : row[5],

						'zipcode' : row[16],
						'street' : row[17],
						'street_number' : row[18],
						'addr_obs' : row[19],
						'neigh' : row[20],
						'city' : row[21],
						'state' : row[22],

						'profession' : row[29]

					}])
				else:
					iters += 1


		#Add to the Users Model

		for item in csv_data:

			iters -= 1
			print(iters)

			extra = dict()

			try:
				Users().add_user(
					mig_id=item[0]['mig_id'],

					user_name=item[0]['user_name'],
					auth_type='password',
					auth_token='abacate',

					first_name = item[0]['first_name'],
					last_name = item[0]['last_name'],
					cpf = item[0]['cpf'],
					birthday = item[0]['birthday'],

					zipcode = item[0]['zipcode'],
					street = item[0]['street'],
					street_number = item[0]['street_number'],
					addr_obs = item[0]['addr_obs'],
					neigh = item[0]['neigh'],
					city = item[0]['city'],
					state = item[0]['state'],

					profession = item[0]['profession'],

					extra_data = extra,
				)

				result_msg = 'Sucesso'
				result_count += 1

			except Exception as err:
				result_msg = format(err)+' '+item[0]['mig_id']
				return {'result_msg': result_msg, 'result_count' : result_count}

		return {'result_msg': result_msg, 'result_count' : result_count}


	def mig_cells(self):

		result_msg = ''
		result_count = 0
		ids_added = []

		csv_data = []

		cvs_path_cells = 'mig/static/upload/grupos.csv'

		with open(cvs_path_cells) as f:
			reader = csv.reader(f, delimiter=';')

			for row in reader:

				if row[0] not in ids_added:

					csv_data.append([{
						'id_cell' : row[0],
						'cell_name' : row[1].strip(),

						'zipcode' : row[16],
						'street' : row[17],	
						'street_number' : row[18],
						'addr_obs' : row[19],
						'neigh' : row[20],
						'city' : row[21],
						'state' : row[22]

					}])

					ids_added.append(row[0])					

		#Add to the Group/Cells Model
		iters = 0
		for item in csv_data:

			if iters > 0:
				extra = dict()

				try:
					Cells().add_cell(
						mig_id = item[0]['id_cell'],
						name = item[0]['cell_name'],

						cell_origin = None,
						cells_over = [],
						cells_under = [],
						user_roles = [],

						zipcode = item[0]['zipcode'],
						street = item[0]['street'],
						street_number = item[0]['street_number'],
						addr_obs = item[0]['addr_obs'],
						neigh = item[0]['neigh'],
						city = item[0]['city'],
						state = item[0]['state'],

						extra_data = extra,
					)

					result_msg = 'Sucesso'
					result_count += 1
				except Exception as err:
					result_msg = format(err)
			else:
				iters += 1


		return {'result_msg': result_msg, 'result_count' : result_count}


	def mig_cells_roles(self):

		result_msg = ''
		result_count = 0

		csv_data = []

		cvs_path_cells = 'mig/static/upload/grupos_x_participantes.csv'

		with open(cvs_path_cells) as f:
			reader = csv.reader(f, delimiter=';')

			for row in reader:

				csv_data.append([{
					'id_cell' : row[0],
					'id_user' : row[2],
					'role' : row[4]
				}])

		#Add to the Group/Cells Model
		iters = 0
		for item in csv_data:

			if iters > 0:
				user_rls = []

				id_user = item[0]['id_user']
				id_cell = item[0]['id_cell']
				role = item[0]['role']

				user_obj = Users.objects.get(mig_id=id_user)

				if role == 'LÍDER':
					roles_obj = Roles.objects.get(code="leader")
				elif role == 'ANFITRIÃO':
					roles_obj = Roles.objects.get(code="host")				
				else:
					roles_obj = Roles.objects.get(code="cell_member")				

				user_rls.append(User_roles(user=user_obj, role=[roles_obj]))

				try:

					Cells.objects.filter(mig_id = id_cell).update(
						add_to_set__user_roles = user_rls
					)

					result_msg = 'Sucesso'
					result_count += 1

				except Exception as err:
					result_msg = format(err)

			iters += 1


		return {'result_msg': result_msg, 'result_count' : result_count}


	def mig_metting(self):

		result_msg = ''
		result_count = 0
		ids_added = []

		csv_data = []

		cvs_path_cells = 'mig/static/upload/grupos_x_encontro_precenca_participantes.csv'

		with open(cvs_path_cells) as f:
			reader = csv.reader(f, delimiter=',')

			for row in reader:

				if row[2] not in ids_added:

					csv_data.append([{
						'id_cell' : row[0],
						'id_metting' : row[2],
						'name' : row[3],
						'data' : row[4],
						'id_user' : row[5],
						'role' : row[7],
						'presence' : row[8]
					}])

					ids_added.append(row[2])

		#Add to the Events/Cell_metting Model
		iters = 0
		for item in csv_data:

			if iters > 0:
				user_rls = []

				extra = dict()

				id_cell = item[0]['id_cell']
				id_metting = item[0]['id_metting']
				name = item[0]['name']
				data = item[0]['data']
				id_user = item[0]['id_user']
				role = item[0]['role']
				presence = item[0]['presence']

				cell_obj = Cells.objects.get(mig_id=id_cell)

				try:
					Cell_mettings().add_event(
						mig_id = id_metting,
						name = name,
						parent_event = None,
						start_date = data,
						end_date = '',
						cells_in = [],
						host = cell_obj,
						recorrent = '',
						user_roles = [],
						extra_data = extra,
					)

					result_msg = 'Sucesso'
					result_count += 1
				except Exception as err:
					result_msg = format(err)

			iters += 1


		return {'result_msg': result_msg, 'result_count' : result_count}


	def mig_metting_presence(self):

		result_msg = ''
		result_count = 0
		ids_added = []

		csv_data = []

		cvs_path_cells = 'mig/static/upload/grupos_x_encontro_precenca_participantes.csv'

		with open(cvs_path_cells) as f:
			reader = csv.reader(f, delimiter=',')

			for row in reader:

				csv_data.append([{
					'id_cell' : row[0],
					'id_metting' : row[2],
					'id_user' : row[5],
					'role' : row[7],
					'presence' : row[8]
				}])


		#Add to the Events/Cell_metting Model
		iters = 0
		for item in csv_data:

			if iters > 0:
				user_rls = []

				extra = dict()

				id_cell = item[0]['id_cell']
				id_metting = item[0]['id_metting']
				id_user = item[0]['id_user']
				role = item[0]['role']
				presence = item[0]['presence']

				if presence == '1':

					user_obj = Users.objects.get(mig_id=id_user)

					if role == 'LÍDER':
						roles_obj = Roles.objects.get(code="leader")
					elif role == 'ANFITRIÃO':
						roles_obj = Roles.objects.get(code="host")				
					else:
						roles_obj = Roles.objects.get(code="cell_member")				

					user_rls.append(User_roles(user=user_obj, role=[roles_obj]))

					try:

						Cell_mettings.objects.filter(mig_id = id_metting).update(
							add_to_set__user_roles = user_rls
						)

						result_msg = 'Sucesso'
						result_count += 1

					except Exception as err:
						result_msg = format(err)


			iters += 1


		return {'result_msg': result_msg, 'result_count' : result_count}


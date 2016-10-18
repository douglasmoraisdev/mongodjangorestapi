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

		users_list = []
		roles_list = []
		users_count = 0
		users_formated = []
		user_role = []
		user_added = []

		group = Groups.objects.get(id=group_id)

		#algoritimo que faz um distict entre os usuarios e suas funções
		#retorna uma lista de dicts ex.: UsuarioA:['funcao1'], UsuarioB: ['funcao1','funcao2']
		for u in group.user_roles:
			users_list.append(u.user)
			roles_list.append(u.role)

		users_count = len(users_list)
		for key, user in enumerate(users_list):

			if (users_list[key].id not in user_added):
				for x in range(0,users_count):
					if (users_list[x].id == users_list[key].id):
						user_role.append(roles_list[x].name)
						user_added.append(users_list[key].id)

				users_formated.append({'name':user.name,'role':user_role})
				user_role = []

		return users_formated


		#query to get and separe users on group

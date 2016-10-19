from django.db import models
from mongoengine import *
from crossbone.models.groups import *
# Create your models here.

class Events(Document):
	host = ReferenceField(Groups)
	event_roles = EmbeddedDocumentListField(User_roles)
	data = DictField()

	def add_event(self, host, event_roles, data):

		Events.objects.create(
			host=host,
			event_roles = event_roles,
			data=data
		)

	def get_events_by_group_id(self, group_id):

		return Events.objects(host=group_id)

	def get_event_by_id(self, event_id):

		return Events.objects.get(id=event_id)

	def get_event_users(self, event_id):

		users_list = []
		roles_list = []
		users_count = 0
		users_formated = []
		user_role = []
		user_added = []

		event = Events.objects.get(id=event_id)

		#algoritimo que faz um distict entre os usuarios e suas funções
		#retorna uma lista de dicts ex.: UsuarioA:['funcao1'], UsuarioB: ['funcao1','funcao2']
		for u in event.event_roles:
			users_list.append(u.user)
			roles_list.append(u.role)

		users_count = len(users_list)
		for key, user in enumerate(users_list):

			if (users_list[key].id not in user_added):
				for x in range(0,users_count):
					if (users_list[x].id == users_list[key].id):
						user_role.append(roles_list[x].name)
						user_added.append(users_list[key].id)

				users_formated.append({'name':user.name,'user_id':user.id,'role':user_role})
				user_role = []

		return users_formated
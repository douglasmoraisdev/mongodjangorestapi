from django.db import models
from mongoengine import *
from crossbone.models.groups_types import *
from crossbone.models.users import *


import logging

logger = logging.getLogger(__name__)


class Groups(Document):
	group_type = ReferenceField(Groups_types)
	user_roles = EmbeddedDocumentListField(User_roles)
	origin = ReferenceField("self", reverse_delete_rule = NULLIFY)
	groups_over = ListField(ReferenceField("self", reverse_delete_rule = NULLIFY))
	groups_under = ListField(ReferenceField("self", reverse_delete_rule = NULLIFY))
	extra_data = DictField()


	def add_group(self, group_type, group_origin, groups_over, groups_under, user_roles, extra_data=None):

		ex_data = dict()

		if extra_data:

			#empty 
			extra_data['name'] = extra_data['name'] if ('name' in extra_data) else ''
			extra_data['description'] = extra_data['description'] if ('description' in extra_data) else ''
			extra_data['created_on_date'] = extra_data['created_on_date'] if ('created_on_date' in extra_data) else ''
			extra_data['status'] = extra_data['status'] if ('status' in extra_data) else ''
			extra_data['obs'] = extra_data['obs'] if ('obs' in extra_data) else ''			

			ex_data = dict(
				{'name':
					{'name':'Nome','value': extra_data['name']},
				 'description':
					{'name':'Descrição','value': extra_data['description']},
				 'created_on_date':
					{'name':'Criado em','value': extra_data['created_on_date']},
				 'status':
					{'name':'Situação','value': extra_data['status']},
				 'obs':
					{'name':'Observações','value': extra_data['obs']},
				}
			)

		Groups.objects.create(
			group_type=group_type,
			origin=group_origin,
			groups_over=groups_over,
			groups_under=groups_under,
			user_roles = user_roles,
			extra_data=ex_data
		)

	def get_group_by_id(self, group_id):

		return Groups.objects.get(id=group_id)


	def get_group_users(self, group_id):

		users_list = []
		roles_list = []
		tasks_list = []
		users_formated = []

		group = Groups.objects.get(id=group_id)

		return group.user_roles

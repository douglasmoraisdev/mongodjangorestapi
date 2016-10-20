from django.db import models
from mongoengine import *
# Create your models here.

class Roles(Document):
	name = StringField(max_length=50)
	roles_over = ListField(ReferenceField("self", reverse_delete_rule = NULLIFY))
	roles_under = ListField(ReferenceField("self", reverse_delete_rule = NULLIFY))
	view_order = IntField(max_length=5)
	permissions = StringField(max_length=3) # r = read - rw = readwrite - rwc = readwritecreate
	presence = StringField(max_length=1)
	extra_data = DictField()


	def add_role(self, role_name='', roles_over=[], roles_under=[], view_order=0, extra_data=None):
		
		ex_data = dict()

		if extra_data:

			#empty 
			extra_data['description'] = extra_data['description'] if ('description' in extra_data) else ''
			
			ex_data = dict( 
				{'description':
					{'name':'Descrição','value': extra_data.description}

				}
			)

		Roles.objects.create(
			name = role_name,
			roles_over = roles_over,
			roles_under = roles_under,
			view_order=view_order,
			extra_data = ex_data
		)

from django.db import models
from mongoengine import *
from bethelgroups.models.events import *
from bethelgroups.models.groups import *

# Create your models here.

class Roles(Document):
	name = StringField(max_length=50)
	code = StringField(max_length=50)
	roles_over = ListField(ReferenceField("self", reverse_delete_rule = NULLIFY))
	roles_under = ListField(ReferenceField("self", reverse_delete_rule = NULLIFY))
	#role_groups_scope = ListField(ReferenceField(Groups)) #scope = para ser exibido atribuido a 1-n grupos
	#role_events_scope = ListField(ReferenceField(Events))	
	view_order = IntField(max_length=5)
	permissions = StringField(max_length=3) # r = read - rw = readwrite - rwc = readwritecreate
	presence = StringField(max_length=1)# y or n
	extra_data = DictField()


	def add_role(self, role_name, code, permissions='r', presence='y', roles_over=[], roles_under=[], view_order=0, extra_data=None):
		
		Roles.objects.create(
			name = role_name,
			code = code,
			roles_over = roles_over,
			roles_under = roles_under,
			view_order=view_order,
			permissions=permissions,
			presence=presence,
			extra_data = extra_data
		)


	def edit_role(self, role_name, code, permissions='r', presence='y', roles_over=[], roles_under=[], view_order=0, extra_data=None):
		
		Roles.objects.create(
			name = role_name,
			code = code,
			roles_over = roles_over,
			roles_under = roles_under,
			view_order=view_order,
			permissions=permissions,
			presence=presence,
			extra_data = extra_data
		)
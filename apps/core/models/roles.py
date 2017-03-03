from django.db import models
from mongoengine import *
from core.models.events import *
from core.models.groups import *

# Create your models here.

class Roles(Document):
	name = StringField(max_length=50)
	code = StringField(max_length=50)
	roles_over = ListField(ReferenceField("self", reverse_delete_rule = NULLIFY))
	roles_under = ListField(ReferenceField("self", reverse_delete_rule = NULLIFY))
	#role_groups_scope = ListField(ReferenceField(Groups)) #scope = para ser exibido atribuido a 1-n grupos
	#role_events_scope = ListField(ReferenceField(Events)) #scope = para ser exibido atribuido a 1-n eventos
	view_order = IntField(max_length=5)
	permissions = StringField(max_length=3) # r = read - rw = readwrite - rwc = readwritecreate
	presence = StringField(max_length=1)# y or n
	extra_data = DictField()
	app_scope = ListField(StringField(max_length=50)) #list with apps that a role is related to apper eg. group, course, subject


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
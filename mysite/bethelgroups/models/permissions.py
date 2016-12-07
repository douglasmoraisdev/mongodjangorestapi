from django.db import models
from mongoengine import *
from bethelgroups.models.roles import *
from bethelgroups.models.groups import *
from bethelgroups.models.events import *
from bethelgroups.models.system import *


class Permissions(Document):
	target_obj = StringField(max_length=15) # sistem, groups, event, task, financial_account
	perms = StringField(max_length=4) # r = read - rw = readwrite - rwc = readwritecreate - + = see childs
	role = ReferenceField(Roles) # id of leader, host, member
	extra_data = DictField()

	def get_user_perms(self, user_id):
		'''
			Retrive from DB the roles perms
		'''

		#Get perms for Events
		event_roles_user = dict()
		event_perms = None
		all_user_roles = []
		user_events = Events().get_user_events(user_id)
		for ur in user_events:
			for us in ur.user_roles:
				if us.user.id == user_id:
					for rls in us.role:
						all_user_roles.append(rls)
			event_roles_user = {'type': 'events', 'roles': all_user_roles}

		if event_roles_user:
			event_perms = Permissions().get_app_perms(event_roles_user['type'], event_roles_user['roles'])
		

		#Get perms for Groups
		group_roles_user = dict()
		group_perms = None	
		all_user_roles = []
		user_groups = Groups().get_user_groups(user_id)
		for ur in user_groups:
			for us in ur.user_roles:
				if us.user.id == user_id:
					for rls in us.role:
						all_user_roles.append(rls)
			group_roles_user  = {'type': 'groups', 'roles': all_user_roles}

		if group_roles_user:
			group_perms = Permissions().get_app_perms(group_roles_user['type'], group_roles_user['roles'])


		#Get perms for System
		system_roles_user = dict()
		system_perms = None	
		all_user_roles = []
		user_systems = System().get_user_system_perms(user_id)
		for ur in user_systems:
			for us in ur.user_roles:
				if us.user.id == user_id:
					for rls in us.role:
						all_user_roles.append(rls)
			system_roles_user  = {'type': 'system', 'roles': all_user_roles}

		if system_roles_user:
			system_perms = Permissions().get_app_perms(system_roles_user['type'], system_roles_user['roles'])			


		return {"events":event_perms, "groups":group_perms, "system":system_perms}

		

	def get_app_perms(self, app_code, roles):

		app_perms = dict()
		list_perms = []

		for rl in roles:
			perm = Permissions.objects(target_obj=app_code, role=rl)
			
			for p in perm:
				list_perms.append(p.perms)

		app_perms = {'app':app_code, 'perm_codes': list_perms}

		return app_perms
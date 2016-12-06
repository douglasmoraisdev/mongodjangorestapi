from django.db import models
from mongoengine import *
from bethelgroups.models.roles import *
from bethelgroups.models.groups import *
from bethelgroups.models.events import *


class Permissions(Document):
	target_obj = StringField(max_length=15) # groups, event, task, financial_account
	perms = StringField(max_length=4) # r = read - rw = readwrite - rwc = readwritecreate - + = see childs
	role = ReferenceField(Roles) # id of leader, host, member
	extra_data = DictField()

	def get_user_perms(self, user_id):

		event_roles_user = dict()		
		group_roles_user = dict()


		#Get perms for Events
		all_user_roles = []		
		user_events = Events().get_user_events(user_id)
		for ur in user_events:
			for rls in ur.user_roles[0].role:
				all_user_roles.append(rls)			
			event_roles_user = {'type': 'events', 'roles': all_user_roles}			

		event_perms = Permissions().get_app_perms(event_roles_user['type'], event_roles_user['roles'])


		#Get perms for Groups
		all_user_roles = []		
		user_groups = Groups().get_user_groups(user_id)			
		for ur in user_groups:
			for rls in ur.user_roles[0].role:
				all_user_roles.append(rls)				
			group_roles_user  = {'type': 'groups', 'roles': all_user_roles}

		group_perms = Permissions().get_app_perms(group_roles_user['type'], group_roles_user['roles'])


		return [event_perms, group_perms]

		

	def get_app_perms(self, app_code, roles):

		app_perms = dict()
		list_perms = []

		for rl in roles:
			perm = Permissions.objects(target_obj=app_code, role=rl)
			
			for p in perm:
				list_perms.append(p.perms)

		app_perms = {'app':app_code, 'perm_codes': list_perms}

		return app_perms
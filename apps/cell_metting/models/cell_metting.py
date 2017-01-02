from django.db import models
from mongoengine import *
from bethel_core.models.groups import *
from bethel_core.models.events import *
# Create your models here.

class Cell_mettings(Events):


	def add_event(self, name,parent_event, user_roles, start_date, end_date, groups_in=[], host='', recorrent='', extra_data=None,  mig_id=''):

		Cell_mettings.objects.create(
			name=name,
			mig_id = mig_id,
			parent_event=parent_event,
			host=host,
			groups_in=groups_in,
			user_roles = user_roles,
			start_date=start_date,
			end_date=end_date,
			recorrent=recorrent,
			extra_data=extra_data
		)

	def add_user_event(self, user_roles, event_id):

		Events.objects.filter(id=event_id).update(
			add_to_set__user_roles = user_roles
		)	

	def remove_user_event(self, user, event_id):

		Events.objects.filter(id=event_id).update(pull__user_roles__user=user[0].user)			


	def get_events_by_group_id(self, group_id):
		
		course_id = Events_types.objects(code='course')[0].id
		meeting_id = Events_types.objects(code='meeting')[0].id	

		events = Events.objects(host=group_id, event_type__nin=[course_id, meeting_id])

		return events


	def get_courses_by_group_id(self, group_id):

		course_id = Events_types.objects(code='course')[0].id

		courses = Events.objects(host=group_id, event_type=course_id)		

		return courses


	def get_meetings_by_group_id(self, group_id):

		meeting_id = Events_types.objects(code='meeting')[0].id

		meetings = Events.objects(host=group_id, event_type=meeting_id)		

		return meetings			


	def get_event_by_id(self, event_id):

		return Events.objects.get(id=event_id)


	def get_event_childs(self, event_id):

		return Events.objects(parent_event=event_id)


	def get_event_users(self, event_id, role=None):
		'''
		returns the user_roles of the groups by id
		params:
		role(optional): get by user role, eg: 'leaders or hosts'
		'''
		user_list = []
		event = Events.objects.get(id=event_id)

		if (role != None):
			for us in event.user_roles:
				for rl in us.role:
					if rl.code in role:
						user_list.append(us)

			return user_list		


		return event.user_roles


	def get_user_events(self, user_id):

		course_id = Events_types.objects(code='course')[0].id

		event = Events.objects(user_roles__user=user_id, event_type__ne=course_id)

		return event


	def get_user_courses(self, user_id):

		type_course_id = Events_types.objects(code='course')[0].id
		
		event = Events.objects(user_roles__user=user_id, event_type=type_course_id)

		return event


	def get_user_events_by_type(self, user_id = '', get_childs=False):

		events_under = []

		events = Events.objects(user_roles__user=user_id)

		user_events = dict()

		for key, etype in enumerate(events):

			if etype.event_type.code not in ['course']: #retorna tudos menos os cursos TODO: criar um list na conf
				if etype.event_type.code in user_events:
					user_events[etype.event_type.code].append(events[key])
				else:
					user_events[etype.event_type.code] = [events[key]]


		# Get events under (all events that this event is over) IF get_childs == True
		# TODO get groups over
		'''
		if get_childs:
			events_under = Events.objects(groups_over__in=groups)

			for key, etype in enumerate(events):

				if etype.event_type.code not in ['course']: #retorna tudos menos os cursos TODO: criar um list na conf
					if etype.event_type.code in user_events:
						user_events[etype.event_type.code].append(events[key])
					else:
						user_events[etype.event_type.code] = [events[key]]
		'''



		return user_events

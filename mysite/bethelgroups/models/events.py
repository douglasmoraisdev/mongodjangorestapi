from django.db import models
from mongoengine import *
from bethelgroups.models.groups import *
from bethelgroups.models.events_types import *
# Create your models here.

class Events(Document):

	parent_event = ReferenceField("self", reverse_delete_rule = NULLIFY)
	name = StringField(max_length=50)	
	host = ReferenceField(Groups)
	groups_in = ListField(ReferenceField(Groups))
	event_type = ReferenceField(Events_types)
	user_roles = EmbeddedDocumentListField(User_roles)
	start_date = StringField(max_length=50)
	end_date = StringField(max_length=50)
	recorrent = StringField(max_length=1)
	extra_data = DictField()


	def add_event(self, name,  parent_event, event_type, user_roles, start_date, end_date, groups_in=[], host='', recorrent='', extra_data=None):

		Events.objects.create(
			name=name,
			parent_event=parent_event,
			host=host,
			groups_in=groups_in,
			event_type=event_type,
			user_roles = user_roles,
			start_date=start_date,
			end_date=end_date,
			recorrent=recorrent,
			extra_data=extra_data
		)

	def edit_event(self, event_id, name, parent_event, event_type, user_roles, start_date, end_date, groups_in=[], host='', recorrent='', extra_data=None):

		Events.objects.filter(id=event_id).update(
			name=name,
			user_roles = user_roles,
			start_date=start_date,
			end_date=end_date,
			recorrent=recorrent,
			extra_data=extra_data
		)


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


	def get_event_users(self, event_id):

		event = Events.objects.get(id=event_id)

		return event.user_roles


	def get_user_events(self, user_id):

		course_id = Events_types.objects(code='course')[0].id

		event = Events.objects(user_roles__user=user_id, event_type__ne=course_id)

		return event


	def get_user_courses(self, user_id):

		type_course_id = Events_types.objects(code='course')[0].id
		
		event = Events.objects(user_roles__user=user_id, event_type=type_course_id)

		return event


	def get_user_events_by_type(self, user_id):

		events = Events.objects(user_roles__user=user_id)

		user_events = dict()

		for key, etype in enumerate(events):


			if etype.event_type.code not in ['course']: #retorna tudos menos os cursos TODO: criar um list na conf
				if etype.event_type.code in user_events:
					user_events[etype.event_type.code].append(events[key])
				else:
					user_events[etype.event_type.code] = [events[key]]


		return user_events

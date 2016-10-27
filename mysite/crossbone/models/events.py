from django.db import models
from mongoengine import *
from crossbone.models.groups import *
from crossbone.models.events_types import *
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


	def get_events_by_group_id(self, group_id):

		return Events.objects(host=group_id)


	def get_event_by_id(self, event_id):

		return Events.objects.get(id=event_id)



	def get_event_users(self, event_id):

		event = Events.objects.get(id=event_id)

		return event.user_roles

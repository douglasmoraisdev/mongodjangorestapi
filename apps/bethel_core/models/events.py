from django.db import models
from mongoengine import *
from bethel_core.models.groups import *
# Create your models here.

class Events(Document):	

	meta = {'allow_inheritance': True,  'indexes':['mig_id','name']}

	mig_id = StringField(max_length=50)
	parent_event = ReferenceField("self", reverse_delete_rule = NULLIFY)
	name = StringField(max_length=50)
	host = ReferenceField(Groups, dbref=True)
	groups_in = ListField(ReferenceField(Groups, dbref=True))
	user_roles = ListField(EmbeddedDocumentField(User_roles))
	#user_roles = EmbeddedDocumentListField(User_roles)
	start_date = StringField(max_length=50)
	end_date = StringField(max_length=50)
	recorrent = StringField(max_length=1)
	extra_data = DictField()




	def add_event(self, name,parent_event, user_roles, start_date, end_date, groups_in=[], host='', recorrent='', extra_data=None,  mig_id=''):

		Events.objects.create(
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

	def edit_event(self, event_id, name, parent_event,  user_roles, start_date, end_date, groups_in=[], host='', recorrent='', extra_data=None):

		Events.objects.filter(id=event_id).update(
			name=name,
			user_roles = user_roles,
			start_date=start_date,
			end_date=end_date,
			recorrent=recorrent,
			extra_data=extra_data
		)


	def get_all(self, search):
		
		return Events.objects(name__icontains=search)

	def get_events_by_group_id(self, group_id):
		#TODO usar o _cls para separar por tipos de eventos		

		#course_id = Events_types.objects(code='course')[0].id
		#meeting_id = Events_types.objects(code='meeting')[0].id	

		#events = Events.objects(host=group_id, event_type__nin=[course_id, meeting_id])

		#temp
		events = Events.objects(host=group_id)

		return events


	def get_courses_by_group_id(self, group_id):

		course_id = Events_types.objects(code='course')[0].id

		courses = Events.objects(host=group_id, event_type=course_id)		

		return courses


	def get_meetings_by_group_id(self, group_id):
		#TODO usar _cls para separa por tipos de eventos


		#meeting_id = Events_types.objects(code='meeting')[0].id

		#meetings = Events.objects(host=group_id, event_type=meeting_id)		

		#temp
		meetings = Events.objects(host=group_id)

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

		event = Events.objects(user_roles__user=user_id, _cls__ne='Events.Course')

		return event


	def get_user_courses(self, user_id):

	
		event = Events.objects(user_roles__user=user_id, _cls='Events.Course')

		return event


	def get_user_events_by_type(self, user_id = '', get_childs=False):

		events_under = []

		events = Events.objects(user_roles__user=user_id)

		user_events = dict()

		for key, etype in enumerate(events):

			if etype._cls not in ['Events.Courses']: #retorna tudos menos os cursos TODO: criar um list na conf
				if etype._cls in user_events:
					user_events[etype._cls].append(events[key])
				else:
					user_events[etype._cls] = [events[key]]


		# Get events under (all events that this event is over) IF get_childs == True
		# TODO get groups over
		'''
		if get_childs:
			events_under = Events.objects(groups_over__in=groups)

			for key, etype in enumerate(events):

				if etype._cls not in ['course']: #retorna tudos menos os cursos TODO: criar um list na conf
					if etype._cls in user_events:
						user_events[etype._cls].append(events[key])
					else:
						user_events[etype._cls] = [events[key]]
		'''



		return user_events

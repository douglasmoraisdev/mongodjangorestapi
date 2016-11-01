from django.db import models
from mongoengine import *

from crossbone.models.groups import *
from crossbone.models.events import *
from crossbone.models.users import *
from crossbone.models.financial_account import *


class Financial_movement(Document):

	release_date = StringField(max_length=20)
	due_date = StringField(max_length=20)	
	value = StringField(max_length=30)
	amount_paid	= StringField(max_length=30)
	description = StringField(max_length=30)
	groups_origin = ListField(ReferenceField(Groups))
	users_origin = ListField(ReferenceField(Users))
	events_origin = ListField(ReferenceField(Events))
	account_origin = ReferenceField(Financial_account)
	account_destiny = ReferenceField(Financial_account)
	recorrent = ListField(StringField(max_length=1))
	recurrence_period = StringField(max_length=30)
	extra_data = DictField()


	def add_financial_movement(self, movement_date, description, value, group_origin, user_origin, event_origin, recorrent, extra_data):

		Financial_movement.objects.create(
			movement_date = movement_date,
			description = description,
			value = value,
			group_origin = group_origin,
			user_origin = user_origin,
			event_origin = event_origin,
			recorrent = recorrent,
			extra_data = extra_data
		)

	def get_financial_movement_by_group_id(self, group_id):

		return Financial_movement.objects(host=group_id)

	def get_financial_movement_by_id(self, financial_movement_id):

		return Financial_movement.objects.get(id=financial_movement)


	def get_financial_movement_users(self, financial_movement):

		f_mov = Financial_movement.objects.get(id=financial_movement)

		return f_mov.user_origin
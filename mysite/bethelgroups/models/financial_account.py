from django.db import models
from mongoengine import *

from bethelgroups.models.groups import *
from bethelgroups.models.events import *
from bethelgroups.models.users import *


class Financial_account(Document):

	open_date = StringField(max_length=20)
	description = StringField(max_length=30)
	balance = StringField(max_length=30)
	group_owner = ReferenceField(Groups)
	user_owner = ReferenceField(Users)
	events_owner = ListField(ReferenceField(Events))
	active = StringField(max_length=1)


	def add_financial_account(self, open_date, description,balance, group_owner, users_owner, events_owner, active):

		Financial_account.objects.create(
			open_date = open_date,
			description = description,
			balance = balance,
			group_owner = group_owner,
			users_owner = users_owner,
			events_owner = events_owner,
			active = active,
		)

	def get_financial_account_by_group_id(self, group_id):

		return Financial_account.objects(host=group_id)

	def get_financial_account_by_id(self, financial_account_id):

		return Financial_account.objects.get(id=financial_account)


	def get_financial_account_users(self, financial_account):

		f_account = Financial_account.objects.get(id=financial_account)

		return f_account.user_origin

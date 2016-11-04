from django.db import models
from mongoengine import *
# Create your models here.


class Groups_types(Document):
	code = StringField(max_length=50)
	name = StringField(max_length=50)
	extra_data = DictField()

	def add_group_type(self, code, name, extra_data=None):

		Groups_types.objects.create(
			code=code,
			name=name,
			extra_data=extra_data
		)

	def get_grouptype_by_id(self, grouptype_id):

		return Groups_types.objects.get(id=grouptype_id)
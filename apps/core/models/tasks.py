from django.db import models
from mongoengine import *


#TODO: Adicionar usuarios assigned=None, um ou VARIOS usuarios pode estar assigned para esta tarefa
#Colocar também concluida ou não
class Tasks(Document):
	name = StringField(max_length=50)
	start_date = StringField(max_length=50)
	end_date = StringField(max_length=50)
	extra_data = DictField()

	def add_task(self, task_name, start_date='', end_date='', extra_data=None):
		
		Tasks.objects.create(
			name = task_name,
			start_date=start_date,
			end_date=end_date,
			extra_data = extra_data
		)

	def get_task_by_id(self, task_id):

		return Tasks.objects.get(id=task_id)

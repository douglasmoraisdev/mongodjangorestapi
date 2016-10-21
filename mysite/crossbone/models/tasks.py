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
		
		ex_data = dict()

		if extra_data:

			#empty 
			extra_data['description'] = extra_data['description'] if ('description' in extra_data) else ''
			
			ex_data = dict( 
				{'description':
					{'name':'Descrição','value': extra_data.description}

				}
			)

		Tasks.objects.create(
			name = task_name,
			start_date=start_date,
			end_date=end_date,
			extra_data = ex_data
		)

from django.test import TestCase
from django.test import Client

client = Client()

class ViewsTest_Users(TestCase):

	def test_add_user(self):

		response = client.post('/crossbone/novouser', {'nome_usuario':'TioJoao'})

		self.assertEquals(response.status_code, 201)
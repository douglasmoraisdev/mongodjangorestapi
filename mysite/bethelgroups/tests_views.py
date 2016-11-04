import test_addons

from django.test import TestCase
from django.test import Client

client = Client()

class ViewsTest_Users(test_addons.MongoTestCase):

	def test_add_user(self):

		response = client.post('/bethelgroups/novouser', {'nome_usuario':'TioPaulo'})

		self.assertEquals(response.status_code, 200)
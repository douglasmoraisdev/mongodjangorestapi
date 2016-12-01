from django.conf import settings

def my_context(request):
	context_data = dict()
	context_data['base_url'] = settings.BASE_URL
	return context_data
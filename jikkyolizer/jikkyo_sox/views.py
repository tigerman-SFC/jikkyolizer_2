from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

# Create your views here.

class Index(LoginRequiredMixin,TemplateView):
	template_name = 'voice.html'
	def get(self, request):
		context = {
			'voice_id' : 0
		}
		return render(
			request,
			'voice.html',
			context
		)
		
			


class Backend(LoginRequiredMixin,TemplateView):
	def post(self, request):
		pass

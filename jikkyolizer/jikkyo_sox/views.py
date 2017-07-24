from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.http import HttpResponse as AjaxResponse

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
		
			


class NewVoice(LoginRequiredMixin, TemplateView):
	def post(self, request):
		#new_voice_no = tools.
		#new_voice_no = '00001' 
		test='A'
		past_voices = []
		for i in range(5):
			past_voices.append(request.POST['used_voice' + str(i)])
		#new_voice = tools.fetch_new_voice(past_voices)
		return AjaxResponse(test)

	def get(self, request):
		return AjaxResponse('a')




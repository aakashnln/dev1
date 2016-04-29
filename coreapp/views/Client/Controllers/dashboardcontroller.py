from django.shortcuts import render,render_to_response,redirect,get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponseRedirect,HttpResponse
from django.views.generic import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..Forms.clientcampaignform import CampaignForm
from coreapp.models import *
from django.template.context_processors import csrf
from django.core.mail import send_mail
import hashlib, datetime, random
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
# Create your views here.

# class ClientController(object):
#	 """docstring for ClientController"""
#	 def __init__(self, arg):
#		 super(ClientController, self).__init__()
#		 self.arg = arg

# class ClientDashboardController(View):
# 	"""ClientDashboardController does the following:
# 		- ClientDashboard LandingPage
# 		# - ClientDashboard Start campaign
# 		# - ClientDashboard Campaign analytics
# 	"""
# 	# def __init__(self, arg):
# 	# 	super(ClientController, self).__init__()
# 	# 	self.arg = arg
# 	def create(request):
# 		# perform client creation task ==> signup
		
# 		pass

# 	def login(request):
# 		# client login

# 		pass

def is_logged_in(request):
	if 'client_id' not in request.session.keys():
		return False
	return True

@csrf_protect
def client_campaign_create(request):
	if not is_logged_in(request):
		# print 'redirect to login',request.user
		return redirect('Client_login')

	client = Client.objects.get(id=request.session['client_id'])

	if request.method == 'POST':
		form = CampaignForm(request.POST)
	
		# is_valid validates a form and returns True if it is valid and
		# False if it is invalid.
		if form.is_valid():
			campaign_name = form.cleaned_data['campaign_name']
			cars_required = form.cleaned_data['cars_required']
			impression_target = form.cleaned_data['impression_target']
			campaign_perimeter = form.cleaned_data['campaign_perimeter'] # stored as string version of geoJson
			c = campaign_perimeter.replace('(','[')
			c = c.replace(')',']')
			campaign_perimeter = c

			start_date = form.cleaned_data['start_date']
			
			# print campaign_perimeter
			# print type(campaign_perimeter)

			wrap_type = form.cleaned_data['wrap_type']
			import dateutil.relativedelta
			end_date = start_date + dateutil.relativedelta.relativedelta(months=form.cleaned_data['campaign_duration'])

			datas = {}
			datas['campaign_name']=campaign_name
			datas['client'] = client
			datas['cars_required'] = cars_required
			datas['impression_target'] = impression_target
			datas['start_date'] = start_date
			datas['end_date'] = end_date
			datas['campaign_perimeter'] = campaign_perimeter
			datas['wrap_type'] = wrap_type
			campaign = form.save(datas)

			return render(request, "dashboard/campaign_form_success.html")
	# This means that the request is a GET request. So we need to
	# create an instance of the RegistrationForm class and render it in
	# the template
	else:
		form = CampaignForm()

	return render(request,'dashboard/campaign_form.html',{'title':"Add Campaign","form" : form })

def client_dashboard(request):
	# if request.user==None or request.user == AnonymousUser():
	if not is_logged_in(request):
		# print 'redirect to login',request.user
		return redirect('Client_login')
	# print request.user
	# print request.session['client_id']
	client = Client.objects.get(id=request.session['client_id'])
	campaigns = ClientCampaign.objects.filter(client=client)
	if len(campaigns)>0:
		default_camp_id = campaigns[0].id
	else:
		default_camp_id = -1

	return render(request,'dashboard/dashboard2.html',{'client':client,'title':"DUA Dashboard",'campaigns':campaigns,'default_camp_id':default_camp_id})

def load_campaign_details(request, camp_id=None):
	if not is_logged_in(request):
		# print 'redirect to login',request.user
		return redirect('Client_login')
	client = Client.objects.get(id=request.session['client_id'])
	campaign = ClientCampaign.objects.filter(client=client,id=camp_id)
	# for c in [campaign[0].campaign_perimeter]:
	# c = campaign[0].campaign_perimeter
	# c = c.replace('(','[')
	# c = c.replace(')',']')
	# campaign[0].campaign_perimeter = c
	# print campaign[0].campaign_perimeter
	# print c
	print 'length',type(campaign[0].campaign_perimeter)
	if len(campaign)<1:
		return render(request,'dashboard/dashboard_iframe.html',{'client':client,'title':"DUA Dashboard",'campaigns':[]})

	return render(request,'dashboard/dashboard_iframe.html',{'client':client,'title':"DUA Dashboard",'campaigns':campaign})

	
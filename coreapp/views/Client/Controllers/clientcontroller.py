from django.shortcuts import render,render_to_response,redirect,get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponseRedirect,HttpResponse
from django.views.generic import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..Forms.clientsignupform import RegistrationForm
from coreapp.models import *
from django.template.context_processors import csrf
from django.core.mail import send_mail
import hashlib, datetime, random
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from dashboardcontroller import *
# Create your views here.

# class ClientController(object):
#	 """docstring for ClientController"""
#	 def __init__(self, arg):
#		 super(ClientController, self).__init__()
#		 self.arg = arg

def homepage(request):
	print 'Loading landing page'
	return render(request, 'client_templates/index.html')

# class ClientController(View):
"""ClientController does the followin:
	- Client Create (Signup)
	- Client Login
	- Client preferences update
	- Client details updation
"""
# def __init__(self, arg):
# 	super(ClientController, self).__init__()
# 	self.arg = arg

@api_view(['GET','POST'])
def client_create(request):
	# perform client creation task ==> signup
	print 'Client create page requested'
	# This function-based view handles the requests to the root URL /. See
	# urls.py for the mapping.
	# If the request method is POST, it means that the form has been submitted
	# and we need to validate it.
	# Create and save user profile
	# new_profile = Client(user=user, activation_key=activation_key,key_expires=key_expires)
	if request.method == 'POST':	
		# Create a RegistrationForm instance with the submitted data
		form = RegistrationForm(request.POST)
	
		# is_valid validates a form and returns True if it is valid and
		# False if it is invalid.
		if form.is_valid():
			# The form is valid and you could save it to a database
			# by creating a model object and populating the
			# data from the form object, but here we are just
			# rendering a success template page.
			return render(request, "client_templates/success.html")
	# This means that the request is a GET request. So we need to
	# create an instance of the RegistrationForm class and render it in
	# the template
	else:
		form = RegistrationForm()
	# Render the registration form template with a RegistrationForm instance. If the
	# form was submitted and the data found to be invalid, the template will
	# be rendered with the entered data and error messages. Otherwise an empty
	# form will be rendered. Check the comments in the registration_form.html template
	# to understand how this is done.
	return render(request, "client_templates/clientsignup.html",
				{ "form" : form })
	# return render(request, 'client_templates/clientsignup.html')
	# pass

@csrf_protect
def client_register(request):
	# args = {}
	# args.update(csrf(request))

	if 'client_id' in request.session.keys():
		return redirect('Client_dashboard')

	if request.user.is_authenticated():
		return redirect(home)

	registration_form = RegistrationForm()
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():

			client_name = form.cleaned_data['name']
			client_username = form.cleaned_data['username']
			client_email = form.cleaned_data['email']
			client_address = form.cleaned_data['address']
			client_phone_number = form.cleaned_data['phone_number']
			client_company = form.cleaned_data['company']

			client_password = hashlib.sha1(form.cleaned_data['password']).hexdigest()

			salt = hashlib.sha1(str(random.random())).hexdigest()[:5]

			activation_key = hashlib.sha1(salt+client_email).hexdigest()			
			key_expires = datetime.datetime.today() + datetime.timedelta(2)

			datas = {}
			datas['client_name'] = client_name
			datas['client_username'] = client_username
			datas['client_email'] = client_email
			datas['client_address'] = client_address
			datas['client_phone_number'] = client_phone_number
			datas['client_company'] = client_company
			datas['client_password'] = client_password
			datas['client_status']='1'
			#save client data
			client = form.save(datas)

			#Get client by username
			# client=Client.objects.get(client_username=client_username)

			# Create and save user profile
			new_profile = ClientProfile(client=client, activation_key=activation_key,key_expires=key_expires)
			new_profile.save()

			# Send email with activation key
			email_subject = 'Account confirmation'
			email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
			48hours http://127.0.0.1:8000/client/client_confirmation/%s" % (client_username, activation_key)
			print email_body

			# send_mail(email_subject, email_body, 'aakashnln11.4@gmail.com',[client_email], fail_silently=False)

			# return HttpResponseRedirect('/client/register_success')

			request.session['registered']=True #For display purposes
			return redirect('/client/register_success/')
	else:
		form = RegistrationForm()
		#args['form'] = RegistrationForm()
	# return render_to_response('client_templates/clientsignup.html', args, context_instance=RequestContext(request))
	return render(request, 'client_templates/clientsignup.html', { "form" : form })

def authenticate(email=None, password=None):
		"""
		Authentication method
		"""
		try:
			client = Client.objects.get(client_email=email)
			if client.check_password(password):
				print client.client_email
				return client
		except Client.DoesNotExist:
			return None

def get_client(_id):
	try:
		client = Client.objects.get(pk=_id)
		if client.client_status in ['2','3']:
			return client
		return None
	except Client.DoesNotExist:
		return None

@csrf_protect
def client_register_success(request):
	print 'success page'
	return render(request, 'client_templates/success.html')

def client_confirmation(request, activation_key):
	#check if user is already logged in and if he is redirect him to some other url, e.g. home
	if request.user.is_authenticated():
		print 'user authenticated'
		HttpResponseRedirect('/')

	# check if there is ClientProfile which matches the activation key (if not then display 404)
	client_profile = get_object_or_404(ClientProfile, activation_key=activation_key)

	#check if the activation key has expired, if it hase then render client_templates/confirm_expired.html
	if client_profile.key_expires < timezone.now():
		return render_to_response('client_templates/confirm_expired.html')
	#if the key hasn't expired save user and set him as active and render some template to confirm activation
	client = client_profile.client
	client.client_status = '2'
	client.save()
	return render_to_response('client_templates/confirm.html')

def client_login(request):
	# client login
	# print 'user',request.user
	logout(request)
	username = password = ''
	if request.method == 'POST':
		if request.POST:
			logout(request)
			email = request.POST['email']
			password = request.POST['password']

			client = authenticate(email=email, password=password)
			if client is not None:
				if client.client_status == '2':
					request.user = client
					# print request.user.client_name
					client.client_login(request)
					# return HttpResponseRedirect('/client/register_success/')
					return redirect('/client/dashboard/')
					# client_dashboard(request)
				else:
					print 'user not activated',client.client_status
					error = 'Email has not been activated, our team has been informed and they will connect with you shortly.'
					return render(request,'client_templates/login.html',{'error':error})
			else:
				print 'user not found'
				error = 'Email or password is not correct'
				return render(request,'client_templates/login.html',{'error':error})
	return render(request,'client_templates/login.html')

def client_logout(request):
	logout(request)
	return redirect('homepage')
# @login_required(login_url='/login/')


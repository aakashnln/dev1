from django.shortcuts import render,render_to_response,redirect,get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponseRedirect,HttpResponse
from django.views.generic import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from coreapp.models import *
# from django.template.context_processors import csrf
from django.core.mail import send_mail
import hashlib, datetime, random
from mongoengine import connect
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import coreapp.utils as utils
from django.db.models import F
import coreapp.signals
from coreapp.tasks import *
import json
# Create your views here.

def driver_homepage(request):
	print 'Loading landing page'
	return render(request, 'driver_templates/index.html')

# def is_logged_in(request):
# 	if 'client_id' not in request.session.keys():
# 		return False
# 	return True

def driver_register(request):
	# args = {}
	# args.update(csrf(request))

	if 'driver_id' in request.session.keys():
		# return redirect('driver_dashboard')
		logout(request)

	if request.user.is_authenticated():
		return redirect(home)

	if request.method == 'POST':
		data = json.loads(request.body)
		# print type(request.body)
		uuid = data['uuid']
		username = data['username']
		email = data['email']
		# address = form.cleaned_data['address']
		phone_number = data['phnum']
		# company = form.cleaned_data['company']

		password = hashlib.sha1(data['password']).hexdigest()
		password_confimation = hashlib.sha1(data['password_confirmation']).hexdigest()
		if password!=password_confimation:
			return JsonResponse({'valid':False,'errors':'Passwords not same'})

		salt = hashlib.sha1(str(random.random())).hexdigest()[:5]

		activation_key = hashlib.sha1(salt+email).hexdigest()			
		key_expires = datetime.datetime.today() + datetime.timedelta(2)

		datas = {}
		datas['uuid'] = uuid
		datas['username'] = username
		datas['email'] = email
		# datas['client_address'] = client_address
		datas['phone_number'] = phone_number
		# datas['client_company'] = client_company
		datas['password'] = password
		datas['status']='1'
		#save client data
		client = form.save(datas)

		#Get client by username
		# client=Client.objects.get(client_username=client_username)

		# Create and save user profile
		new_profile = DriverProfile(driver=driver, activation_key=activation_key,key_expires=key_expires)
		new_profile.save()

		# Send email with activation key
		email_subject = 'Account confirmation'
		email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
		48hours http://127.0.0.1:8000/client/client_confirmation/%s" % (username, activation_key)
		print email_body

		# send_mail(email_subject, email_body, 'aakashnln11.4@gmail.com',[client_email], fail_silently=False)

		# return HttpResponseRedirect('/client/register_success')

		request.session['registered']=True #For display purposes
		return JsonResponse({'valid':False,'errors':'Passwords not same'})
	else:
		form = RegistrationForm()
		#args['form'] = RegistrationForm()
	# return render_to_response('client_templates/clientsignup.html', args, context_instance=RequestContext(request))
	return render(request, 'client_templates/clientsignup.html', { "form" : form })

def authenticate(email=None,phone_number=None, password=None):
		"""
		Authentication method
		"""
		try:
			if email == None:
				driver = Driver.objects.get(email=email)
			else:
				driver = Driver.objects.get(phone_number=phone_number)
			if driver.check_password(password):
				print driver.email
				return driver
		except Driver.DoesNotExist:
			return None

def get_client(_id):
	try:
		driver = Driver.objects.get(pk=_id)
		if driver.driver_status in ['2','3']:
			return driver
		return None
	except Driver.DoesNotExist:
		return None

def get_driver_status(request):
	res = {}
	if request.method == 'POST':
		if request.POST: #TODO add session check for returning the status
			data = json.loads(request.body)
			username = data['username']
			driver = Driver.objects.get(username=username)
			if driver is not None:
				res['valid'] = True
				res['status'] = driver.status
				# res['email'] = email
				# res['username'] = driver.drive_username
			else:
				print 'user not found'
				res['valid'] = False
				res['errors'] = 'No info'

def driver_login(request):
	# client login
	# print 'user',request.user
	logout(request)
	username = password = ''
	res = {}
	if request.method == 'POST':
		if request.POST:
			data = json.loads(request.body)
			password = data['password']

			if 'phnum' in data.keys:
				phone_number = data['phnum']
				driver = authenticate(phone_number=phone_number, password=password)
			else:
				email = data['email']
				driver = authenticate(email=email, password=password)

			if driver is not None:
				if driver.status == '3':
					request.user = driver
					# print request.user.client_name
					drive.driver_login(request)
					# return HttpResponseRedirect('/client/register_success/')
					# return redirect('/client/dashboard/')
					# client_dashboard(request)
					res['valid'] = True
					res['messages'] = "Welcome"
					res['email'] = email
					res['username'] = driver.drive_username
				else:
					print 'user not activated'
					res['valid'] = True
					res['email'] = email
					res['username'] = driver.drive_username
					res['errors'] = "Your account is yet to be activated."
			else:
				print 'user not found'
				res['valid'] = False
				res['errors'] = 'Email/Phone number and password combination did not match.'
	return JsonResponse(res)

def get_active_campaigns(request):
	res = {}
	campaigns_details = ClientCampaignDetail.objects.filter() 
	return JsonResponse(res)


# @csrf_protect
def get_trip_earning(request):
	if 'uuid' not in request.GET.keys():
		return JsonResponse({'error':'unknown device'})

	driver = Driver.objects.filter(id=request.GET['uuid'])	
	if driver == []:
		return JsonResponse({'error':'unknown driver'})
	print driver
	driver = driver[0] # get the driver

	print 'Trip earnings requested'
	# trip_id = request.GET['trip_id']
	uuid = request.GET['uuid']
	trip_points = LocationLog.objects.filter(device_uuid='6889cee8-4039-3c41-9995-1f7048d646c5',campaignId=campaignId)
	if len(trip_points)<2:
		return JsonResponse({'error':'Trip to short'})
	
	campaign = ClientCampaign.objects.get(id = trip_points[0].campaignId)
	polyline = []
	for point in trip_points:
		polyline.append(point.gps_loc['coordinates'])

	print utils.cal_polyline_dist(polyline)

	poly = campaign.campaign_perimeter

	campaign_detail = ClientCampaignDetail.objects.get(id = trip_points[0].campaign_detailId)

	campaign = DriverCampaign.objects.get(driver=driver,campaign_detail=campaign_detail)
	
	daily_cap = campaign_detail.daily_cap
	daily_km_cap = campaign_detail.daily_km_cap

	trip_dict = trip_earning(poly,trip_points,{})

	if trip_dict == 0.0:
		return JsonResponse({'error':'Trip to short'})

	# code to update the daily earnings 
	try:
		dde = DriverDailyEarning.objects.get(driver=driver,create_at__date = datetime.date.today())

		if float(dde.total_trip_earning)+trip_dict['earning']>=daily_cap:
			trip_dict['earning'] = daily_cap
			km_cap = True
		else:
			trip_dict['earning'] = float(dde.total_trip_earning)+trip_dict['earning']
			km_cap = False

		if float(dde.total_trip_distance)+trip_dict['trip_distance']>=daily_km_cap:
			trip_dict['trip_distance'] = daily_km_cap
			km_cap = True
		else:
			trip_dict['trip_distance'] = float(dde.total_trip_distance)+trip_dict['trip_distance']
			km_cap = False

		dde.update(total_trip_earning = trip_dict['earning'],trip_count = F('trip_count') + 1,total_trip_distance = trip_dict['trip_distance'])
		dde.save()
	except:
		if trip_dict['earning']>=daily_cap:
			trip_dict['earning'] = daily_cap
			km_cap = True
		else:
			km_cap = False

		if trip_dict['trip_distance']>=daily_km_cap:
			trip_dict['trip_distance'] = daily_km_cap
			km_cap = True
		else:
			km_cap = False

		dde = DriverDailyEarning(driver=driver,total_trip_earning = trip_dict['earning'],trip_count = 1,total_trip_distance = trip_dict['trip_distance'])
		dde.save()

	tp = TripLog(device_uuid=trip_points[0].device_uuid, userId=trip_points[0].userId,trip_uuid=trip_points[0].trip_uuid,campaignId=trip_points[0].campaignId,trip_loc_path = trip_dict['trip_loc_path'],trip_distance=trip_dict['trip_distance'])
	tp.save()
	
	#TODO optimise the above by creating async tasks and sending user a simple response saying completed or somthing like that

	coreapp.signal.update_dashboad(sender='TripLog', request=request,trip_points=trip_points,trip_dict=trip_dict)

	# envoke async task to update client dashboard data
	update_dashboard(request,driver,campaign_detail,trip_points,trip_dict).delay()
	return JsonResponse({'earnings':trip_dict,
	flags:{'km_cap':km_cap,'earning_cap':earning_cap}})
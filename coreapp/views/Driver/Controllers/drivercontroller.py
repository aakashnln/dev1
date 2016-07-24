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
from django.db.models import F # for conter updates in db
from django.db.models import Q as django_Q# for complex queries
import coreapp.signals
from coreapp.tasks import *
import json
import traceback
import uuid
from dua.settings import SECRET_KEY
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

	# if request.user.is_authenticated():
	# 	return redirect(home)

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
			return JsonResponse({'valid':False,'error':'Passwords not same'})

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
		# client = form.save(datas)
		try:
			driver = Driver(uuid=uuid,name=datas['username'],username=datas['username'],company='',address='',phone_number=datas['phone_number'],email=datas['email'],password=datas['password'],status=datas['status'])
			driver.save()
			#Get client by username
			# client=Client.objects.get(client_username=client_username)

			# Create and save user profile
			# add change to OTP system
			# new_profile = DriverProfile(driver=driver, activation_key=activation_key,key_expires=key_expires)
			# new_profile.save()

			# Send email with activation key
			email_subject = 'Account confirmation'
			email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
			48hours http://127.0.0.1:8000/driver/driver_confirmation/%s" % (username, activation_key)
			print email_body

			# send_mail(email_subject, email_body, 'aakashnln11.4@gmail.com',[client_email], fail_silently=False)

			# return HttpResponseRedirect('/client/register_success')

			request.session['registered']=True #For display purposes
			return JsonResponse({'valid':True,'status':datas['status']})
		# else:
		# 	form = RegistrationForm()
			#args['form'] = RegistrationForm()
		# return render_to_response('client_templates/clientsignup.html', args, context_instance=RequestContext(request))
		# return render(request, 'client_templates/clientsignup.html', { "form" : form })
		except:
			return JsonResponse({'valid':False,'error':'Email or phone number already registered, try forgot password'})
	return JsonResponse({'valid':False})

# def driver_confirmation(request, activation_key):
# 	#check if user is already logged in and if he is redirect him to some other url, e.g. home
# 	if request.user.is_authenticated():
# 		print 'user authenticated'
# 		HttpResponseRedirect('/')

# 	# check if there is ClientProfile which matches the activation key (if not then display 404)
# 	client_profile = get_object_or_404(ClientProfile, activation_key=activation_key)

# 	#check if the activation key has expired, if it hase then render client_templates/confirm_expired.html
# 	if client_profile.key_expires < timezone.now():
# 		return render_to_response('client_templates/confirm_expired.html')
# 	#if the key hasn't expired save user and set him as active and render some template to confirm activation
# 	client = client_profile.client
# 	client.client_status = '2'
# 	client.save()
# 	return render_to_response('client_templates/confirm.html')

def authenticate(email=None,phone_number=None, password=None):
		"""
		Authentication method
		"""
		try:
			if email != None:
				driver = Driver.objects.get(email=email)
			else:
				driver = Driver.objects.get(phone_number=phone_number)
			if driver.check_password(password):
				# print driver.email
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
	res = {'valid':False}
	if request.method == 'POST':
		try:
			# if request.POST: #TODO add session check for returning the status
			data = json.loads(request.body)
			email = data['email']
			uuid = data['uuid']
			driver = Driver.objects.get(uuid=uuid,email=email)
			if driver is not None:
				res['valid'] = True
				res['status'] = driver.status
				try:
					# dc = DriverCampaign.objects.get(driver=driver,campaign_status='2')
					dc = DriverCampaign.objects.filter(django_Q(driver=driver),django_Q(campaign_status='1') | django_Q(campaign_status='2'))
					# print dc
					if dc!=None and len(dc)!=0:  # check if driver has not signed up for any campaign
						res['status'] += dc[0].campaign_status
						# print dc[0].campaign_detail.campaign.id
						if dc[0].campaign_status == '2':
							res['campaignId'] = dc[0].campaign_detail.campaign.id
						print 'YOLO',res
				except:
					# print 'YOLO'
					print traceback.format_exc()
					pass
				# res['email'] = email
				# res['username'] = driver.drive_username
			else: # this is not going to reached as the Driver.objects.get with cause the exception to be triggered
				print 'user not found'
				res['valid'] = False
				res['error'] = 'Some error occured, please try again after some time.'
		except:
			print traceback.format_exc()
			res['valid'] = False
			res['status'] = '-1'
			res['error'] = 'You are being logged out, please log in again'
	return JsonResponse(res)

def driver_login(request):
	# client login
	# print 'user',request.user
	logout(request)
	username = password = ''
	res = {}
	if request.method == 'POST':
		data = json.loads(request.body)
		password = data['password']

		if '@' not in data['email']:
			phone_number = data['email']
			driver = authenticate(phone_number=phone_number, password=password)
		else:
			email = data['email']
			driver = authenticate(email=email, password=password)

		if driver is not None:
			if driver.status == '3':
				request.user = driver
				# print request.user.client_name
				driver.driver_login(request)
				# return HttpResponseRedirect('/client/register_success/')
				# return redirect('/client/dashboard/')
				# client_dashboard(request)
				res['valid'] = True
				res['messages'] = "Welcome"
				res['email'] = driver.email
				res['phnum'] = driver.phone_number
				res['username'] = driver.username
				res['status'] = driver.status
				if driver.uuid != data['uuid']:
					driver.uuid = data['uuid']
					driver.save()
			else:
				print 'User not activated'
				res['valid'] = True
				res['email'] = driver.email
				res['username'] = driver.username
				res['phnum'] = driver.phone_number
				res['status'] = driver.status
				res['error'] = "Your account is yet to be activated."
				if driver.uuid != data['uuid']:
					driver.uuid = data['uuid']
					driver.save()
		else:
			print 'user not found'
			res['valid'] = False
			res['error'] = 'Email/Phone number and password combination did not match.'
	print res
	return JsonResponse(res)

# def get_active_campaigns(request):
# 	res = {}
# 	campaigns_details = ClientCampaignDetail.objects.filter() 
# 	return JsonResponse(res)

def get_active_campaigns(request):
	res = {'valid':False}
	if request.method == 'GET':
		if request.GET: #TODO add session check for returning the status
			# data = json.loads(request.body)
			# username = data['username']
			# uuid = data['uuid']
			# city = 'bangalore'#data['city']
			city = request.GET['city']
			# driver = Driver.objects.get(uuid=uuid,username=username)
			driver = 1
			try:
				# print '$$$$$$$$$$$$$$'
				if driver is not None:
					res['valid']=True
					cc = ClientCampaign.objects.filter(campaign_city__contains=city.lower(),campaign_status='3').values('id','client__client_name','campaign_name', 'cars_required','campaign_perimeter','campaign_city','start_date','end_date')
					for c in cc:
						campaign_length = c['end_date'].month - c['start_date'].month
						c['campaign_length'] = campaign_length
					# for c in cc:
					# 	# ccd = ClientCampaignDetail.objects.filter(campaign=c.campaign,cars_remaining!=0)
					# 	# ccd = ccd.values('id','daily_cap', 'daily_km_cap','daily_earning_max','daily_earning_min','cars_remaining','wrap_type')
					# 	c = c.
						#TODO, form a car details structure and render a page with list of campaings in the city
						# on the next page, get_active_campaing_details show type of wraps available , permeter and getit button, also accept terms and conditions
					res['cc'] = cc
					print 'values',cc.values()
			except:
				print traceback.format_exc()
				pass
				
	return render(request,'driver_templates/campaigns_list.html',{'res':res})		

def get_campaign_detail(request):
	res = {'valid':False}
	if request.method == 'GET':
		if request.GET: #TODO add session check for returning the status
			# data = json.loads(request.body)
			# username = data['username']
			# uuid = data['uuid']
			# city = data['city']
			# campaign = data['campaignId']
			campaign = request.GET['campaignId']
			# driver = Driver.objects.get(uuid=uuid,username=username)
			driver = 1
			try:
				if driver is not None:
					cc = ClientCampaign.objects.filter(id = campaign).values('id','client__client_name','campaign_name', 'cars_required','campaign_perimeter','campaign_city','start_date','end_date')

					campaign_length = cc[0]['end_date'].month - cc[0]['start_date'].month
					res['campaign_length'] = campaign_length
					print 'campaign_length',campaign_length
					ccd = ClientCampaignDetail.objects.filter(campaign = campaign)
					if ccd is not None and cc is not None:
						res['valid']=True
						daily_km_cap = 0
						daily_earning_min = 0
						daily_earning_max = 0
						for cd in ccd:
							# if cd.wrap_type == '1':
							if daily_km_cap<cd.daily_km_cap:
								daily_km_cap = int(cd.daily_km_cap)
							if daily_earning_max<cd.daily_earning_max:
								daily_earning_max = int(cd.daily_earning_max)
							if daily_earning_min<cd.daily_earning_min:
								daily_earning_min = int(cd.daily_earning_min)
						res['cc']=cc
						res['daily_km_cap']=daily_km_cap
						res['daily_earning_max']=daily_earning_max
						res['daily_earning_min']=daily_earning_min
			except:
				print traceback.format_exc()
				pass

	return render(request,'driver_templates/campaign_detail.html',{'res':res})		

def get_active_campaign_wrap_details(request):
	res = {'valid':False}
	if request.method == 'GET':
		if request.GET: #TODO add session check for returning the status
			# data = json.loads(request.body)
			# username = data['username']
			# uuid = data['uuid']
			# city = data['city']
			# driver = Driver.objects.get(uuid=uuid,username=username)
			# campaign = data['campaignId']
			campaign = request.GET['campaignId']
			driver = 1
			if driver is not None:
				res['valid']=True
				res['campaigns']={}
				temp = []
				ccd = ClientCampaignDetail.objects.filter(campaign = campaign)#.values('id','campaign__campaign_name','daily_cap', 'daily_km_cap','daily_earning_max','daily_earning_min','cars_required','cars_remaining','wrap_type')
				if ccd is not None:
					# print ccd.values()
					res['ccd'] = ccd
					print ccd.values()
				# for cd in ccd:
				# 	campaign_length = cd['end_date'].month - c['start_date'].month
				# 	cd['campaign_length'] = campaign_length
	return render(request,'driver_templates/campaign_detail_wrap.html',{'res':res})

def get_active_campaign_specific_wrap_detail(request):
	res = {'valid':False}
	if request.method == 'GET':
		if request.GET: #TODO add session check for returning the status
			# data = json.loads(request.body)
			# username = data['username']
			# uuid = data['uuid']
			# city = data['city']
			# driver = Driver.objects.get(uuid=uuid,username=username)
			# campaign = data['campaignId']
			campaign = request.GET['campaignId']
			wrap_type = request.GET['wrap_type']
			driver = 1
			if driver is not None:
				res['valid']=True
				res['campaigns']={}
				temp = []
				ccd = ClientCampaignDetail.objects.filter(campaign = campaign,wrap_type=wrap_type)#.values('id','campaign__campaign_name','daily_cap', 'daily_km_cap','daily_earning_max','daily_earning_min','cars_required','cars_remaining','wrap_type')
				if ccd is not None:
					# print ccd.values()
					res['ccd'] = ccd
					print ccd.values()
					cc = ClientCampaign.objects.filter(id = campaign).values('id','client__client_name','campaign_name', 'cars_required','campaign_perimeter','campaign_city','start_date','end_date')

					campaign_length = cc[0]['end_date'].month - cc[0]['start_date'].month
					res['campaign_length'] = campaign_length
					print 'campaign_length',campaign_length
					ccd = ClientCampaignDetail.objects.filter(campaign = campaign)
					if ccd is not None and cc is not None:
						res['valid']=True
						daily_km_cap = 0
						daily_earning_min = 0
						daily_earning_max = 0
						for cd in ccd:
							# if cd.wrap_type == '1':
							if daily_km_cap<cd.daily_km_cap:
								daily_km_cap = int(cd.daily_km_cap)
							if daily_earning_max<cd.daily_earning_max:
								daily_earning_max = int(cd.daily_earning_max)
							if daily_earning_min<cd.daily_earning_min:
								daily_earning_min = int(cd.daily_earning_min)
						res['cc']=cc
						res['daily_km_cap']=daily_km_cap
						res['daily_earning_max']=daily_earning_max
						res['daily_earning_min']=daily_earning_min
				# for cd in ccd:
				# 	campaign_length = cd['end_date'].month - c['start_date'].month
				# 	cd['campaign_length'] = campaign_length
	return render(request,'driver_templates/campaign_specific_wrap_detail.html',{'res':res})

def campaign_join_post(request):
	res = {'valid':False}
	if request.method == 'POST': #TODO add session check for returning the status
		# print 'yolo'
		data = json.loads(request.body)
		print data
		# username = data['username']
		# uuid = data['uuid']
		# city = data['city']
		# driver = Driver.objects.get(uuid=uuid,username=username)
		# campaign = data['campaignId']
		campaign = data['campaign_id']
		wrap_type = data['wrap_type']

		username = data['username']
		uuid = data['uuid']

		driver = Driver.objects.get(uuid=uuid,username=username)
		# driver = 1
		ccd = ClientCampaignDetail.objects.get(campaign=campaign,wrap_type=wrap_type)
		print ccd.id
		if driver is not None and ccd is not None:
			res['valid']=True
			res['campaigns']={}
			temp = []
			if ccd.cars_required>=1:
				# dc = DriverCampaign.objects.fil TODO avoid multiple requests
				# register a request for campaign by driver
				dc = DriverCampaign(driver=driver,campaign_detail=ccd,campaign_status=1)
				dc.save()
				res['message']='Congratulations, your request to join campaign has been submitted, we will short schedule a appointment for you!'

				ccd.cars_required -= 1
				ccd.cars_remaining -= 1
				ccd.save()
			else:
				res['error']=True
				res['message']='Sorry we are out of spots for this type wrap, kindly select other wrap type'
		else:
			res['error'] = 'Wrong credentials'
	return JsonResponse(res)

def gen_trip_id(request):
	res = {'valid':False}
	if request.method == 'POST':
		data = json.loads(request.body)
		try: #TODO validate for uuid and campaignId
			if data['key'] == SECRET_KEY:
				res['valid'] = True
				res['trip_id'] = str(uuid.uuid4())
		except:
			print traceback.format_exc()

	return JsonResponse(res)

def get_earning_update(request): # Working here................
	if 'uuid' not in request.GET.keys():
		return JsonResponse({'error':'unknown device'})

	driver = Driver.objects.filter(id=request.GET['uuid'])	
	if driver == []:
		return JsonResponse({'error':'unknown driver'})
	print driver
	driver = driver[0] # get the driver

	res = {'valid':False}
	if request.method == 'POST':
		try:
			if data['key'] == SECRET_KEY:
				dde = DriverDailyEarning.objects.get(driver=driver,create_at__date = datetime.date.today())
				res['valid'] = True
				res['earning_today'] = dde.total_trip_earning
				res['earning_month'] = DriverCampaign.objects.filter(create_at__date = datetime.date.month()).aggregate(Sum('total_trip_earning'))
		except:
			print traceback.format_exc()
			res['message'] = "Error updating earning, please contact coustmer support"

	return JsonResponse(res)

# @csrf_protect Make this work with stoptrip in android and then make get earning method work
def get_trip_earning(request):
	res = {'valid':False}
	if request.method == 'POST':
		data = json.loads(request.body)
		if 'uuid' not in data.keys():
			res['error']='unknown device'
			return JsonResponse(res)
		if 'campaignId' not in data.keys():
			res['error']='unknown campaign'
			return JsonResponse(res)
		if 'tripId' not in data.keys():
			res['error']='unknown trip'
			return JsonResponse(res)

		try:
			uuid = data['uuid']
			tripId = data['tripId']
			campaignId = data['campaignId']

			driver = Driver.objects.filter(uuid=uuid)	
			if driver == None or len(driver)==0:
				res['error']='unknown driver'
				return JsonResponse(res)

			print driver
			driver = driver[0] # get the driver

			print 'Trip earnings requested'
			# trip_id = request.GET['trip_id']

			dc = DriverCampaign.objects.filter(driver=driver,campaign_status='2')
			print dc
			if len(dc)==0 or len(dc)>1:
				res['error']='No or more than one active campaigns'
				return JsonResponse(res)

			# campaignId = dc[0].campaign_detail.campaign #TODO test weather this line of code works

			trip_points = LocationLog.objects.filter(device_uuid=uuid,trip_uuid=tripId)

			print trip_points[0],trip_points[0]['campaignId']

			if len(trip_points)<2:
				res['error']='Trip to short'
				return JsonResponse(res)
			
			campaign = ClientCampaign.objects.get(id = trip_points[0]['campaign_id'])
			polyline = []
			for point in trip_points:
				polyline.append(point.gps_loc['coordinates'])

			print utils.cal_polyline_dist(polyline)

			poly = campaign.campaign_perimeter

			campaign_detail = ClientCampaignDetail.objects.get(campaign = campaign)#trip_points[0].campaign_detailId)

			campaign = DriverCampaign.objects.get(driver=driver,campaign_detail=campaign_detail)
			
			daily_cap = campaign_detail.daily_cap
			daily_km_cap = campaign_detail.daily_km_cap

			trip_dict = trip_earning(poly,trip_points,{})

			#trip_dict structure => {'earning':earning,'trip_distance':trip_distance,'trip_loc_path':trip_loc_path}

			if trip_dict == 0.0: # if the trip_earning function returns 0, then the trip is too short
				res['error']='Trip too short'
				return JsonResponse(res)

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
			
			#TODO optimise the above by creating async tasks rabbitmq and sending user a simple response saying completed or somthing like that

			coreapp.signal.update_dashboad(sender='TripLog', request=request,trip_points=trip_points,trip_dict=trip_dict)

			# envoke async task (rabbitmq) to update client dashboard data
			update_dashboard(request,driver,campaign_detail,trip_points,trip_dict).delay()
			res['valid']=True
			res['earnings']=trip_dict
			res['flags']={'km_cap':km_cap,'earning_cap':earning_cap}
		except:
			print traceback.format_exc()
			res['error'] = "Error updating earning, please contact coustmer support"
	return JsonResponse(res)



# def get_trip_earning(request):
# 	if 'uuid' not in request.GET.keys():
# 		return JsonResponse({'error':'unknown device'})

# 	driver = Driver.objects.filter(id=request.GET['uuid'])	
# 	if driver == []:
# 		return JsonResponse({'error':'unknown driver'})
# 	print driver
# 	driver = driver[0] # get the driver

# 	print 'Trip earnings requested'
# 	# trip_id = request.GET['trip_id']
# 	uuid = request.GET['uuid']
# 	trip_points = LocationLog.objects.filter(device_uuid='6889cee8-4039-3c41-9995-1f7048d646c5',campaignId=campaignId)
# 	if len(trip_points)<2:
# 		return JsonResponse({'error':'Trip to short'})
	
# 	campaign = ClientCampaign.objects.get(id = trip_points[0].campaignId)
# 	polyline = []
# 	for point in trip_points:
# 		polyline.append(point.gps_loc['coordinates'])

# 	print utils.cal_polyline_dist(polyline)

# 	poly = campaign.campaign_perimeter

# 	campaign_detail = ClientCampaignDetail.objects.get(id = trip_points[0].campaign_detailId)

# 	campaign = DriverCampaign.objects.get(driver=driver,campaign_detail=campaign_detail)
	
# 	daily_cap = campaign_detail.daily_cap
# 	daily_km_cap = campaign_detail.daily_km_cap

# 	trip_dict = trip_earning(poly,trip_points,{})

# 	if trip_dict == 0.0:
# 		return JsonResponse({'error':'Trip to short'})

# 	# code to update the daily earnings 
# 	try:
# 		dde = DriverDailyEarning.objects.get(driver=driver,create_at__date = datetime.date.today())

# 		if float(dde.total_trip_earning)+trip_dict['earning']>=daily_cap:
# 			trip_dict['earning'] = daily_cap
# 			km_cap = True
# 		else:
# 			trip_dict['earning'] = float(dde.total_trip_earning)+trip_dict['earning']
# 			km_cap = False

# 		if float(dde.total_trip_distance)+trip_dict['trip_distance']>=daily_km_cap:
# 			trip_dict['trip_distance'] = daily_km_cap
# 			km_cap = True
# 		else:
# 			trip_dict['trip_distance'] = float(dde.total_trip_distance)+trip_dict['trip_distance']
# 			km_cap = False

# 		dde.update(total_trip_earning = trip_dict['earning'],trip_count = F('trip_count') + 1,total_trip_distance = trip_dict['trip_distance'])
# 		dde.save()
# 	except:
# 		if trip_dict['earning']>=daily_cap:
# 			trip_dict['earning'] = daily_cap
# 			km_cap = True
# 		else:
# 			km_cap = False

# 		if trip_dict['trip_distance']>=daily_km_cap:
# 			trip_dict['trip_distance'] = daily_km_cap
# 			km_cap = True
# 		else:
# 			km_cap = False

# 		dde = DriverDailyEarning(driver=driver,total_trip_earning = trip_dict['earning'],trip_count = 1,total_trip_distance = trip_dict['trip_distance'])
# 		dde.save()

# 	tp = TripLog(device_uuid=trip_points[0].device_uuid, userId=trip_points[0].userId,trip_uuid=trip_points[0].trip_uuid,campaignId=trip_points[0].campaignId,trip_loc_path = trip_dict['trip_loc_path'],trip_distance=trip_dict['trip_distance'])
# 	tp.save()
	
# 	#TODO optimise the above by creating async tasks and sending user a simple response saying completed or somthing like that

# 	coreapp.signal.update_dashboad(sender='TripLog', request=request,trip_points=trip_points,trip_dict=trip_dict)

# 	# envoke async task to update client dashboard data
# 	update_dashboard(request,driver,campaign_detail,trip_points,trip_dict).delay()
# 	return JsonResponse({'earnings':trip_dict,flags:{'km_cap':km_cap,'earning_cap':earning_cap}})
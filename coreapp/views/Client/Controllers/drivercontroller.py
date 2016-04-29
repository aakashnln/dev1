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
# Create your views here.

def driver_homepage(request):
	print 'Loading landing page'
	return render(request, 'driver_templates/index.html')

# def is_logged_in(request):
# 	if 'client_id' not in request.session.keys():
# 		return False
# 	return True

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

	driver_campaign = DriverCampaign.objects.get(driver=driver,campaign_detail=campaign_detail)
	
	daily_cap = campaign_detail.daily_cap
	daily_km_cap = campaign_detail.daily_km_cap

	trip_dict = trip_earning(poly,trip_points,{})

	if trip_dict == 0.0:
		return JsonResponse({'error':'Trip to short'})

	trip_earning_limit_reached = False	
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
			trip_dict['earning'] = float(dde.total_trip_distance)+trip_dict['trip_distance']
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

	return JsonResponse({'earnings':trip_dict,
	flags = {'km_cap':km_cap,'earning_cap':earning_cap}})
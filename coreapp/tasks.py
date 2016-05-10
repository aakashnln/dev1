from __future__ import absolute_import

from celery import shared_task
from coreapp.models import *


@shared_task
def update_dashboard(request,driver,campaign_detail,trip_points,trip_dict):
	#TODO update the ClientCampaignDailyDashboard and ClientCampaignDashboard
	print 'update_dashboard task........'
	if driver.driver_vehicle_type == 1:
		if campaign_detail.wrap_type == 1 :
			impressions = trip_dict['trip_distance']+3.5
	elif driver.driver_vehicle_type == 2:
		impressions = trip_dict['trip_distance']+4.5
	elif driver.driver_vehicle_type == 3:
		impressions = trip_dict['trip_distance']+5

	try:
		dde = ClientCampaignDailyDashboard.objects.get(campaign_detail=campaign_detail,create_at__date = datetime.date.today())

		if float(dde.total_trip_earning)+trip_dict['earning']>=daily_cap:
			trip_dict['earning'] = daily_cap
			km_cap = True
		else:
			trip_dict['earning'] = float(dde.total_trip_earning)+trip_dict['earning']
			km_cap = False
		
		trip_dict['earning'] = float(dde.total_trip_distance)+trip_dict['trip_distance']

		dde.update(total_trip_earning = trip_dict['earning'],daily_total_distance_km = F('daily_total_distance_km')+
			trip_dict['trip_distance'])
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

		dde = ClientCampaignDailyDashboard(campaign=campaign_detail.campaign,campaign_detail=campaign_detail,driver=driver,total_trip_earning = trip_dict['earning'],trip_count = 1,total_trip_distance = trip_dict['trip_distance'])
		dde.save()
		
	try:
		dde = ClientCampaignDashboard.objects.get(driver=driver,create_at__date = datetime.date.today())

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

		dde.update(total_trip_earning = trip_dict['earning'],trip_count = daily_total_distance_km + 1,total_trip_distance = trip_dict['trip_distance'])
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

		dde = ClientCampaignDashboard(driver=driver,total_trip_earning = trip_dict['earning'],trip_count = 1,total_trip_distance = trip_dict['trip_distance'])
		dde.save()

	return

@shared_task
def update_dashboard_temp():
	#TODO update the ClientCampaignDailyDashboard and ClientCampaignDashboard
	print 'update_dashboard task........'

	return 1
from __future__ import absolute_import

from celery import shared_task
from coreapp.models import *


@shared_task
def update_dashboard(request,driver,campaign_detail,trip_uuid,trip_points,trip_dict):
	#TODO update the ClientCampaignDailyDashboard and ClientCampaignDashboard
	print 'update_dashboard task........'

	# TODO use trip points to calculate correct impressions

	impressions = 0
	if driver.driver_vehicle_type == 1:
		if campaign_detail.wrap_type == 1 :
			impressions = trip_dict['trip_distance']+3.5
	elif driver.driver_vehicle_type == 2:
		impressions = trip_dict['trip_distance']+4.5
	elif driver.driver_vehicle_type == 3:
		impressions = trip_dict['trip_distance']+5

	# save trips impressions in TripLog
	tl = TripLog(trip_uuid=trip_uuid)
	tl.impressions = impressions
	tl.save()
	
	drivers_on_road = DriverDailyEarning.objects.filter(campaign_detail=campaign_detail,create_at__date = datetime.date.today()).count()
	if drivers_on_road == None or drivers_on_road < 1: # check if this is the any active driver
		pass
		# issue and alert as this task was called.
		print 'Flooding the log about update_dashboard task being called without any driver\'s daily earning'
		return

	try:
		ccdd = ClientCampaignDailyDashboard.objects.get(campaign_detail=campaign_detail)
		ccdd.update(daily_total_impressions = F('daily_total_impressions')+impressions,
					daily_total_distance_km = F('daily_total_distance_km')+trip_dict['trip_distance'],
					daily_driver_on_road = driver_on_road,
					daily_total_cost = F('daily_total_cost')+trip_dict['earning']*2.0
					)
		ccdd.save()
	except:
		ccdd = ClientCampaignDailyDashboard(campaign = campaign_detail.campaign,
									campaign_detail = campaign_detail,
									daily_driver_on_road = driver_on_road,
									daily_total_distance_km = total_distance_km,
									daily_total_impressions = impressions,
									daily_total_cost = trip_dict['earning']*2.0,#1000000.00, #get the cost function here
									wrap_type = campaign_detail.wrap_type
									# was here last
									)
	try:
		# updating the Client Campaing dashboard count
		# daily_total_impressions total_impressions
		ccd = ClientCampaignDashboard.objects.get(campaign_detail=campaign_detail)
		ccd.update(total_impressions = F('total_impressions')+impressions,
					total_distance_km = F('total_distance_km')+trip_dict['trip_distance'],
					driver_on_road = driver_on_road,
					total_cost = F('total_cost')+trip_dict['earning']*2.0
					)
		ccd.save()
	except:
		ccd = ClientCampaignDashboard(campaign = campaign_detail.campaign,
									campaign_detail = campaign_detail,
									driver_on_road = driver_on_road,
									total_distance_km = total_distance_km,
									total_impressions = impressions,
									total_cost = trip_dict['earning']*2.0,#1000000.00, #get the cost function here
									wrap_type = campaign_detail.wrap_type
									# was here last
									)

	return

@shared_task
def update_dashboard_temp():
	#TODO update the ClientCampaignDailyDashboard and ClientCampaignDashboard
	print 'update_dashboard task........'

	return 1
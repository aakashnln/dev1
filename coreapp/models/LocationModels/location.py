from mongoengine import *
import datetime

class LocationLog(Document):
	device_uuid = StringField(max_length=500, required=True)
	gps_loc = PointField(required=True,auto_index=False)
	gps_speed = FloatField(required=True)
	gps_heading = FloatField(required=True)
	gps_provider = StringField(max_length=100, required=True)
	# traffic
	gps_timestamp = DateTimeField(required=True,default=datetime.datetime.now)
	userId = LongField(required=True,auto_index=True)#a userID sent by app
	trip_uuid = LongField(required=True,auto_index=True)#a trip UUID send by app
	campaignId = LongField(required=True,default=0)
	campaign_detailId = LongField(required=True,default=0)
	meta = {
		'indexes': [[("gps_loc", "2dsphere"), ("created_at", 1)]]
	}

class TripLog(Document):
	device_uuid = StringField(max_length=500, required=True)
	# timestamp = DateTimeField(required=True)
	userId = LongField(required=True,auto_index=True)#a userID sent by app
	trip_uuid = LongField(required=True,auto_index=True)#a trip UUID send by app
	campaignId = LongField(required=True,default=0)
	trip_loc_path = LineStringField(required=True,auto_index=True)
	trip_distance = FloatField(required=True)
	created_at = DateTimeField()
	updated_at = DateTimeField(default=datetime.datetime.now)
	def save(self, *args, **kwargs):
		if not self.created_at:
			self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
		return super(TripLog, self).save(*args, **kwargs)

	meta = {
		'indexes': [
			[("trip_loc", "2dsphere"), ("created_at", 1)]
		]
	}	



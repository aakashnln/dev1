import math
import datetime
from geopy.distance import vincenty

def __init__():
	pass
# Haversine formula:
def cal_polyline_dist(polyline):
	dist = 0.0
	p0 = polyline[0]
	# p0 = exchange_lat_long(p0)
	for p in polyline:
		dist += float(vincenty(p,p0).m)
		p0 = p
	return dist

def deg2rad(x):
	return x * math.pi / 180;

def exchange_lat_long(point):
	return [point[1],point[0]]

def cal_dist(point1,point2):
	R = 6378137.0
	dLat = deg2rad(point2[1] - point1[1])
	dLong = deg2rad(point2[0] - point1[0])
	a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(deg2rad(point1[1])) * math.cos(deg2rad(point2[0])) * math.sin(dLong / 2) * math.sin(dLong / 2)
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
	d = R * c
	return d # returns the distance

def is_point_in_poly(x,y,poly):
	n = len(poly)
	inside = False
	p1x,p1y = poly[0]
	for i in range(n+1):
		p2x,p2y = poly[i % n]
		if y > min(p1y,p2y):
			if y <= max(p1y,p2y):
				if x <= max(p1x,p2x):
					if p1y != p2y:
						xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
					if p1x == p2x or x <= xints:
						inside = not inside
		p1x,p1y = p2x,p2y
	return inside

def trip_earning(poly,trip_points,constants):
	pass
	# constants
	# trip_points
	# trip_perimeter poly
	# max capcapss => distance and daily earnings
	# timestamp print datetime.datetime.fromtimestamp(int("1461420252734")/1000).strftime('%y-%m-%d %H:%M:%S.%f')
	# have to return zero earning for travel distance less than 500m
	earning = 0.0
	trip_distance = 0.0
	trip_loc_path = []
	if len(trip_points)<2:
		return 0.0
	trip_point1 = trip_points[0]
	dist = 0.0
	for p in trip_points:
		point = p.gps_loc['coordinates']
		if is_point_in_poly(point[1],point[0],poly):
			dist = vincenty(exchange_lat_long(trip_point1.gps_loc['coordinates']),exchange_lat_long(p.gps_loc['coordinates'])).km * 1000.00
			# dist = cal_dist(trip_point1.gps_loc['coordinates'],p.gps_loc['coordinates'])
			trip_distance += dist
			# speed = (trip_point1.gps_speed + p.gps_speed)/2
			dt = (datetime.datetime.fromtimestamp(int(p.gps_timestamp)/1000)-datetime.datetime.fromtimestamp(int(trip_point1.gps_timestamp)/1000)).total_seconds()
			if trip_distance!=p and dt!=0.0:
				speed = dist/abs(dt)
				if speed<0.0:
					print 'speed',speed
				if dt<0.0:
					print 'DT',dt
				if dist<0.0:
					print 'dist',dist
				earning += dist/(speed+1)
				trip_loc_path.append(p.gps_loc['coordinates'])

		trip_point1 = p
	if trip_distance <= 500:
		return 0.0

	return {'earning':earning,'trip_distance':trip_distance,'trip_loc_path':trip_loc_path}

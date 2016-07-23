#OM

from django.db import models
from  django.core.validators import RegexValidator
import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.middleware.csrf import rotate_token
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from multiselectfield import MultiSelectField
# from django.contrib.gis.db import models as gismodels

class Client(AbstractBaseUser):
	client_name = models.CharField(max_length=200,blank=False)
	client_username = models.CharField(max_length=200,blank=False)
	client_company = models.CharField(max_length=200,blank=False)
	client_address  = models.TextField(max_length=500)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999999'. Up to 15 digits allowed.")
	client_phone_number = models.CharField(max_length=15,validators=[phone_regex], blank=False) # validators should be a list
	client_email = models.CharField(max_length=100,unique=True,blank=False)
	# password = models.CharField(max_length=200,blank=False)
	CLIENT_STATUS = (
		('1', 'New'),
		('2', 'Verified'),# verified by the client
		('3', 'Active'), # activated by us
		('4', 'Unknown'),
		)
	client_status = models.CharField(max_length=1,choices=CLIENT_STATUS)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	is_admin = models.BooleanField(default=False)
	class Meta:
		app_label = 'coreapp'

	USERNAME_FIELD = 'email'

	def __unicode__(self):
		return self.client_email

	def check_password(self, raw_password):
		import hashlib
		# ... get 'hsh_passwd' from database based on 'user' ...
		hsh_passwd = self.password
		# hsh_passwd = hsh_passwd.split('$')
		salt = ''#hsh_passwd[1]
		# print hsh_passwd
		# print hashlib.sha1(raw_password).hexdigest()
		if hsh_passwd == hashlib.sha1(raw_password).hexdigest():
			return True
		return False

	def client_login(self,request,backend=None):
		SESSION_KEY = 'client_id'
		BACKEND_SESSION_KEY = 'client_backend'
		HASH_SESSION_KEY = 'client_hash'
		REDIRECT_FIELD_NAME = 'next'
		session_auth_hash = ''
		if self is None:
			self = request.user
		if hasattr(self, 'get_session_auth_hash'):
			session_auth_hash = self.get_session_auth_hash()
		if SESSION_KEY in request.session:
			if self._meta.pk.to_python(request.session[SESSION_KEY]) != self.pk or (session_auth_hash and request.session.get(HASH_SESSION_KEY) != session_auth_hash):
				request.session.flush()
				# To avoid reusing another user's session, create a new, empty
				# session if the existing session corresponds to a different
				# authenticated user.
		else:
			request.session.cycle_key()

		request.session[SESSION_KEY] = self._meta.pk.value_to_string(self)
		request.session[BACKEND_SESSION_KEY] = backend
		request.session[HASH_SESSION_KEY] = session_auth_hash
		if hasattr(request, 'user'):
			# request.session['user']=self.
			request.user = self
		rotate_token(request)
		user_logged_in.send(sender=self.__class__, request=request, user=self)

	def client_logout(self,request,backend=None):
		request.session.flush()
		request.user = None
		if language is not None:
			request.session[LANGUAGE_SESSION_KEY] = language

class ClientProfile(models.Model):
	client = models.OneToOneField(Client)
	activation_key = models.CharField(max_length=40, blank=True)
	key_expires = models.DateTimeField(default=timezone.now)
	  
	def __str__(self):
		return self.client.client_username

	class Meta:
		app_label = 'coreapp'
		verbose_name_plural=u'Client profiles'

class ClientCampaign(models.Model):
	campaign_name = models.CharField(max_length=200,blank=False,default='')
	client = models.ForeignKey(Client, on_delete=models.CASCADE)
	cars_required = models.IntegerField(default=0)
	cars_on_road = models.IntegerField(default=0)
	impression_target = models.BigIntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	# campaign_perimeter = gismodels.PolygonField(blank=False) # stored as string version of geoJson
	campaign_perimeter = models.CharField(max_length=1000,blank=False) # stored as string version of geoJson
	campaign_city = models.CharField(max_length=100,default='') # to be filled from admin panel
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	total_distance = models.FloatField(default=0.0)# sums of drives distances having same campaign ids
	total_impressions = models.BigIntegerField(default=0)# sums of drives distances having same campaign ids
	WRAP_TYPES = (
		# ('0', 'All'),
		('1', 'Full'),
		('2', 'Partial'),# back doors and back hatch
		('3', 'Panel'), # only doors
		('4', 'Unknown'), # not defined
		)
	wrap_type = MultiSelectField(choices=WRAP_TYPES,max_choices=3,
								 max_length=1,default='4')
	CAMPAIGN_STATUS = (
		('1', 'New'),
		('2', 'Processing'),# verified by the client
		('3', 'Active'), # activated by us
		('4', 'Closed'),
		('5', 'Unknown'),
		)
	campaign_status = models.CharField(max_length=1,choices=CAMPAIGN_STATUS,default='1')
	def __unicode__(self):
		return self.campaign_name

class ClientCampaignDetail(models.Model): # can be multiple , one per wrap type
	campaign = models.ForeignKey(ClientCampaign, on_delete=models.CASCADE)
	daily_cap = models.FloatField(blank=False,default=0.0)
	daily_km_cap = models.FloatField(blank=False,default=0.0)
	daily_earning_max = models.FloatField(blank=False,default=0.0)
	daily_earning_min = models.FloatField(blank=False,default=0.0)
	cars_required = models.IntegerField(blank=False,default=0)
	cars_remaining = models.IntegerField(blank=False,default=0)
	WRAP_TYPES = (
		# ('0', 'All'),
		('1', 'Full'),
		('2', 'Partial'),# back doors and back hatch
		('3', 'Panel'), # only doors
		('4', 'Unknown'), # not defined
		)
	wrap_type = models.CharField(choices=WRAP_TYPES,max_length=1,default='4')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
    unique_together = ('campaign', 'wrap_type',) # one campaign must have only one entry per wrap_type


class ClientCampaignDailyDashboard(models.Model): # can be multiple , one per wrap type
	campaign = models.ForeignKey(ClientCampaign, on_delete=models.CASCADE)
	campaign_detail = models.OneToOneField(ClientCampaignDetail, on_delete=models.CASCADE)
	daily_driver_on_road = models.IntegerField(blank=False,default=0.0)
	daily_total_distance_km = models.FloatField(blank=False,default=0.0)
	daily_total_impressions = models.FloatField(blank=False,default=0.0)
	daily_total_cost = models.FloatField(blank=False,default=0.0)
	WRAP_TYPES = (
		# ('0', 'All'),
		('1', 'Full'),
		('2', 'Partial'),# back doors and back hatch
		('3', 'Panel'), # only doors
		('4', 'Unknown'), # not defined
		)
	wrap_type = models.CharField(choices=WRAP_TYPES,max_length=1,default='4')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class ClientCampaignDashboard(models.Model): # can be multiple , one per wrap type
	campaign = models.ForeignKey(ClientCampaign, on_delete=models.CASCADE)
	campaign_detail = models.OneToOneField(ClientCampaignDetail, on_delete=models.CASCADE)
	driver_on_road = models.IntegerField(blank=False,default=0.0)
	total_distance_km = models.FloatField(blank=False,default=0.0)
	total_impressions = models.FloatField(blank=False,default=0.0)
	total_cost = models.FloatField(blank=False,default=0.0)
	WRAP_TYPES = (
		# ('0', 'All'),
		('1', 'Full'),
		('2', 'Partial'),# back doors and back hatch
		('3', 'Panel'), # only doors
		('4', 'Unknown'), # not defined
		)
	wrap_type = models.CharField(choices=WRAP_TYPES,max_length=1,default='4')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
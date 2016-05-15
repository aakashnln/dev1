from django.db import models
from  django.core.validators import RegexValidator
import datetime
from django.utils import timezone
from coreapp.models import *
#OM
class Driver(models.Model):
    uuid = models.CharField(max_length=200,blank=False)
    name = models.CharField(max_length=200,blank=False,default='') #to be filled by agent upon call and vehicle inspection
    username = models.CharField(max_length=200,blank=False)
    company = models.CharField(max_length=200,blank=True)
    address  = models.TextField(max_length=500,blank=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(max_length=15,validators=[phone_regex],unique=True, blank=False) # validators should be a list
    email = models.CharField(max_length=100,unique=True,blank=False)
    password = models.CharField(max_length=200,blank=False)
    STATUS = (
        ('1', 'New'),
        ('2', 'Verified'),
        ('3', 'Active'),
        ('4', 'Wrapped'),
        ('5', 'Unknown'),
        )
    status = models.CharField(max_length=1,choices=STATUS)
    VEHICLE_TYPE = (
        ('1', 'Hatchback'),
        ('2', 'Sedan'),
        ('3', 'SUV'),
        ('4', 'Unknown'),
        )
    vehicle_type = models.CharField(max_length=1,choices=VEHICLE_TYPE,default='4')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'coreapp'

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

    def driver_login(self,request,backend=None):
        SESSION_KEY = 'driver_id'
        BACKEND_SESSION_KEY = 'driver_backend'
        HASH_SESSION_KEY = 'driver_hash'
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

    def driver_logout(self,request,backend=None):
        request.session.flush()
        request.user = None
        if language is not None:
            request.session[LANGUAGE_SESSION_KEY] = language


class DriverProfile(models.Model):
    driver = models.OneToOneField(Driver)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=timezone.now)
      
    def __str__(self):
        return self.driver.username

    class Meta:
        app_label = 'coreapp'
        verbose_name_plural=u'driver profiles'

class DriverCampaign(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    campaign_detail = models.ForeignKey(ClientCampaignDetail, on_delete=models.CASCADE)
    CAMPAIGN_STATUS = (
        ('1', 'Registered'),
        ('2', 'Active'),
        ('3', 'Finished'),
        ('4', 'Unknown'),
        )
    campaign_status = models.CharField(max_length=1,default=1,choices=CAMPAIGN_STATUS)
    campaign_earnings = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateTimeField() # must be filled by admins
    end_date = models.DateTimeField() # must be filled by admins
    total_distance = models.FloatField(default=0.0)# sums of trip ditances having same campaign ids every 15mins
    total_impressions = models.BigIntegerField(default=0)# a daily jobs calculates and stores this for every active driver campaign every 15mins
    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        return super(DriverCampaign, self).save(*args, **kwargs)
    
class DriverDailyEarning(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    total_trip_earning = models.FloatField(default=0.0)
    trip_count = models.IntegerField(default=0)
    total_trip_distance = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        return super(DriverDailyEarning, self).save(*args, **kwargs)

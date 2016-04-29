from django.db import models
from  django.core.validators import RegexValidator
import datetime
from django.utils import timezone
from coreapp.models import *
#OM
class Driver(models.Model):
    driver_uuid = models.CharField(max_length=200,blank=False)
    driver_name = models.CharField(max_length=200,blank=False)
    driver_username = models.CharField(max_length=200,blank=False)
    driver_company = models.CharField(max_length=200)
    driver_address  = models.TextField(max_length=500,blank=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999999'. Up to 15 digits allowed.")
    driver_phone_number = models.CharField(max_length=15,validators=[phone_regex], blank=False) # validators should be a list
    driver_email = models.CharField(max_length=100,blank=False)
    driver_password = models.CharField(max_length=200,blank=False)
    DRIVER_STATUS = (
        ('1', 'New'),
        ('2', 'Verified'),
        ('3', 'Active'),
        ('4', 'Unknown'),
        )
    driver_status = models.CharField(max_length=1,choices=DRIVER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'coreapp'


class DriverProfile(models.Model):
    driver = models.OneToOneField(Driver)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=timezone.now)
      
    def __str__(self):
        return self.driver.driver_username

    class Meta:
        app_label = 'coreapp'
        verbose_name_plural=u'driver profiles'

class DriverCampaign(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    campaign_detail = models.ForeignKey(ClientCampaignDetail, on_delete=models.CASCADE)
    DRIVER_CAMPAIGN_STATUS = (
        ('1', 'Registered'),
        ('2', 'Active'),
        ('3', 'Finished'),
        ('4', 'Unknown'),
        )
    driver_campaign_status = models.CharField(max_length=1,default=1,choices=DRIVER_CAMPAIGN_STATUS)
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
    
class DriverDailyEarning(object):
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

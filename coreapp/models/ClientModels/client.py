from django.db import models
from  django.core.validators import RegexValidator
import datetime
from django.utils import timezone
#OM
class Client(models.Model):
    client_name = models.CharField(max_length=200,blank=False)
    client_username = models.CharField(max_length=200,blank=False)
    client_company = models.CharField(max_length=200,blank=False)
    client_address  = models.TextField(max_length=500)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999999'. Up to 15 digits allowed.")
    client_phone_number = models.CharField(max_length=15,validators=[phone_regex], blank=False) # validators should be a list
    client_email = models.CharField(max_length=100,blank=False)
    client_password = models.CharField(max_length=200,blank=False)
    CLIENT_STATUS = (
        ('1', 'New'),
        ('2', 'Verified'),
        ('3', 'Active'),
        ('4', 'Unknown'),
        )
    client_status = models.CharField(max_length=1,choices=CLIENT_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ClientProfile(models.Model):
    client = models.OneToOneField(Client)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=timezone.now)
      
    def __str__(self):
        return self.client.client_username

    class Meta:
        verbose_name_plural=u'Client profiles'
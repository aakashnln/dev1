from django.db import models
from  django.core.validators import RegexValidator
#OM
class Client(models.Model):
    client_username = models.CharField(max_length=200,blank=False)
    client_company = models.CharField(max_length=200,blank=False)
    client_address  = models.TextField(max_length=500)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999999'. Up to 15 digits allowed.")
    client_phone_number = models.CharField(max_length=15,validators=[phone_regex], blank=False) # validators should be a list
    client_email = models.CharField(max_length=100,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    CLIENT_STATUS = (
        ('1', 'New'),
        ('2', 'Verified'),
        ('3', 'Active'),
        ('4', 'Unknown'),
        )
    client_status = models.CharField(max_length=1,choices=CLIENT_STATUS)

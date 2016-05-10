from django.db.models.signals import pre_save, pre_delete, post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
import os.path
from coreapp.models import *
import django.dispatch

update_dashboad = django.dispatch.Signal(providing_args=["post","request"])

@receiver(update_dashboad, sender=TripLog)
def model_post_save(sender, **kwargs):
	print 'new trip saved in TripLog'
	# TODO add impresions analytics code here and other 
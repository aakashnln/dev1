# Import the forms library to create forms
from django import forms
# from django.contrib.gis import forms as gisforms

# Import the CaptchaField from 'django-simple-captcha'
from captcha.fields import CaptchaField

from  django.core.validators import RegexValidator
from coreapp.models import *
# Create form class for the Registration form
class CampaignForm(forms.Form):
	campaign_name = forms.CharField()
	cars_required = forms.IntegerField(label='Number of cars to be deployed')
	impression_target = forms.IntegerField(label='Impression target',required=False)
	start_date = forms.DateField(initial=datetime.date.today,widget=forms.TextInput(attrs={
				'class':'datepicker1',
				'data-provide':"datepicker"
				}))
	campaign_duration = forms.IntegerField(label='Length of campaign in months',initial=1,min_value=1)
	WRAP_TYPES = (
		# ('0', 'All'),
		('1', 'Full'),
		('2', 'Partial'),# back doors and back hatch
		('3', 'Panel')
		)
	wrap_type = forms.MultipleChoiceField(choices=WRAP_TYPES, widget=forms.CheckboxSelectMultiple())
	# vertices = gisforms.PolygonField()
	campaign_perimeter = forms.CharField(label='Draw campaign perimeter in the map below',widget=forms.TextInput(attrs={
				'id':'vertices',
				'style':'display:none'
				}))
	#Override of save method for saving both User and Profil objects
	def save(self, datas):
		u = ClientCampaign(campaign_name=datas['campaign_name'],client=datas['client'],cars_required=datas['cars_required'],impression_target=datas['impression_target'],campaign_perimeter=datas['campaign_perimeter'],start_date=datas['start_date'],end_date=datas['end_date'],wrap_type=datas['wrap_type'])
		u.save()

		# client_profile=ClientProfile()
		# client_profile.client=u
		# client_profile.activation_key=datas['activation_key']
		# client_profile.key_expires=datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
		# client_profile.save()
		return u
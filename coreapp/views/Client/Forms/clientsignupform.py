# Import the forms library to create forms
from django import forms

# Import the CaptchaField from 'django-simple-captcha'
from captcha.fields import CaptchaField

from  django.core.validators import RegexValidator
from coreapp.models import *
# Create form class for the Registration form
class RegistrationForm(forms.Form):
	name = forms.CharField()
	username = forms.CharField()
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput) # Set the widget to
	                                                     # PasswordInput
	password2 = forms.CharField(widget=forms.PasswordInput,
	                          label="Confirm password") # Set the widget to
	                                                    # PasswordInput and
	                                                    # set an appropriate
														# label
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999999'. Up to 15 digits allowed.")
	phone_number = forms.CharField(max_length=15,validators=[phone_regex]) # validators should be a list
	address = forms.CharField()
	company = forms.CharField()
	captcha = CaptchaField()

	# clean_<fieldname> method in a form class is used to do custom validation
	# for the field.
	# We are doing a custom validation for the 'password2' field and raising
	# a validation error if the password and its confirmation do not match
	def clean_password2(self):
		password = self.cleaned_data['password'] # cleaned_data dictionary has the
		                                         # the valid fields
		password2 = self.cleaned_data['password2']
		if password != password2:
			raise forms.ValidationError("Passwords do not match.")
		return password2

	#clean email field
	def clean_email(self):
		email = self.cleaned_data["email"]
		try:
			Client._default_manager.get(client_email=email)
		except Client.DoesNotExist:
			return email
		raise forms.ValidationError('duplicate email')

	#clean username field
	def clean_username(self):
		username = self.cleaned_data["username"]
		try:
			Client._default_manager.get(client_username=username)
		except Client.DoesNotExist:
			return username
		raise forms.ValidationError('duplicate username')

	def clean_phone_number(self):
		phone_number = self.cleaned_data.get('phone_number', None)
		try:
			int(phone_number)
		except (ValueError, TypeError):
			raise ValidationError('Please enter a valid phone number')
		return phone_number

	#Override of save method for saving both User and Profil objects
	def save(self, datas):
		u = Client(client_name=datas['client_name'],client_username=datas['client_username'],client_company=datas['client_company'],client_address=datas['client_address'],client_phone_number=datas['client_phone_number'],client_email=datas['client_email'],password=datas['client_password'],client_status=datas['client_status'])
		u.save()

		# client_profile=ClientProfile()
		# client_profile.client=u
		# client_profile.activation_key=datas['activation_key']
		# client_profile.key_expires=datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
		# client_profile.save()
		return u

	#Handling of activation email sending ------>>>!! Warning : Domain name is hardcoded below !!<<<------
	#I am using a text file to write the email (I write my email in the text file with templatetags and then populate it with the method below)
	# def sendEmail(self, datas):
	# 	link="http://yourdomain.com/activate/"+datas['activation_key']
	# 	c=Context({'activation_link':link,'username':datas['username']})
	# 	f = open(MEDIA_ROOT+datas['email_path'], 'r')
	# 	t = Template(f.read())
	# 	f.close()
	# 	message=t.render(c)
	# 	#print unicode(message).encode('utf8')
	# 	send_mail(datas['email_subject'], message, 'yourdomain <no-reply@trialkart.com>', [datas['email']], fail_silently=False)
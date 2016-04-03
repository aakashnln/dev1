from django.conf.urls import url,include
from django.views.generic import TemplateView
from . import views

urlpatterns = [

    # url(r'^client/signup/$',views.client_create),
    # url(r'^client/signup/$', TemplateView.as_view(template_name="clientsignup.html")),
    url(r'^$', views.homepage, name='homepage'),
	# url(r'^client/signup/',views)
	# Map the root URL / to be handled by 
	# 'registration.views.registration_form' view
	url(r'^client/signup/$',views.client_register,name='Signup'),
	url(r'^client/register_success/',views.client_register_success),
    url(r'^client/client_confirmation/(?P<activation_key>\w+)/', views.client_confirmation),
	# Allow the URLs beginning with /captcha/ to be handled by
	# the urls.py of captcha module from 'django-simple-captcha'
	url(r'^captcha/', include('captcha.urls')),
]

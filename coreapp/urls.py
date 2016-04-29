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
	url(r'^client/signup/$',views.client_register,name='Client_signup'),
	url(r'^client/register_success/',views.client_register_success),
    url(r'^client/client_confirmation/(?P<activation_key>\w+)/', views.client_confirmation),
    url(r'^client/login/$', views.client_login,name='Client_login'),
    url(r'^client/logout/$', views.client_login,name='Client_logout'),
    url(r'^client/dashboard/$', views.client_dashboard,name='Client_dashboard'),
    url(r'^client/dashboard/load_campaign_details/(?P<camp_id>[-\d]+)/$', views.load_campaign_details,name='dashboard_iframe'),
    url(r'^client/create/campaign/$', views.client_campaign_create,name='Client_campaign'),

    url(r'^driver/get_trip_earning/$', views.get_trip_earning,name='Client_campaign'),
	# Allow the URLs beginning with /captcha/ to be handled by
	# the urls.py of captcha module from 'django-simple-captcha'
	url(r'^captcha/', include('captcha.urls')),
]

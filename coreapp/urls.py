from django.conf.urls import url,include
from django.views.generic import TemplateView
from . import views
from django.views.decorators.csrf import csrf_exempt
import coreapp.signals

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

    url(r'^driver/get_trip_earning/$', views.get_trip_earning,name='Trip_stop'),

    url(r'^api/gen_trip_id/$', csrf_exempt(views.gen_trip_id),name='Gen_trip_id'),
    url(r'^api/get_earning_update/$', csrf_exempt(views.get_earning_update),name='Get_earning_update'),
    # TODO add driver confirmation link
    # url(r'^driver/driver_confirmation/(?P<activation_key>\w+)/', views.client_confirmation),
    url(r'^api/register/$', csrf_exempt(views.driver_register),name='Driver_register'),
    url(r'^api/login/$', csrf_exempt(views.driver_login),name='Driver_login'),
	url(r'^api/get_status/$',csrf_exempt(views.get_driver_status),name='Driver_status'),
    url(r'^api/campaigns_list/$',csrf_exempt(views.get_active_campaigns),name='Campaign_List'),# shows the campaign details with maps
    url(r'^api/campaign_detail/$',csrf_exempt(views.get_campaign_detail),name='Campaign_Detail'), # shows different available wrap types
    url(r'^api/campaign_detail_wrap/$',csrf_exempt(views.get_active_campaign_wrap_details),name='Campaign_Detail_wrap'), # shows details of a specific wrap 
    url(r'^api/campaign_detail_wrap_specific/$',csrf_exempt(views.get_active_campaign_specific_wrap_detail),name='Campaign_Specific_Detail_wrap'), # final page in a specific wrap
    url(r'^api/join_campaign/$',csrf_exempt(views.campaign_join_post),name='Campaign_Detail_wrap'), # final page in a specific wrap
    # Allow the URLs beginning with /captcha/ to be handled by
	# the urls.py of captcha module from 'django-simple-captcha'
	url(r'^captcha/', include('captcha.urls')),
]

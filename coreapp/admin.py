from django.contrib import admin
from coreapp.models import *

# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Client._meta.fields if field.name != "id"]
	pass

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
	list_display = [field.name for field in ClientProfile._meta.fields if field.name != "id"]
	pass

@admin.register(ClientCampaign)
class ClientCampaignAdmin(admin.ModelAdmin):
	list_display = [field.name for field in ClientCampaign._meta.fields if field.name != "id"]
	pass

@admin.register(ClientCampaignDetail)
class ClientCampaignDetailAdmin(admin.ModelAdmin):
	list_display = [field.name for field in ClientCampaignDetail._meta.fields if field.name != "id"]
	pass

@admin.register(ClientCampaignDailyDashboard)
class ClientCampaignDailyDashboardAdmin(admin.ModelAdmin):
	list_display = [field.name for field in ClientCampaignDailyDashboard._meta.fields if field.name != "id"]
	pass

# MONGO models not working in admin board
# @admin.register(LocationLog)
# class LocationLogAdmin(admin.ModelAdmin):
# 	pass

# @admin.register(TripLog)
# class TripLogAdmin(admin.ModelAdmin):
# 	pass

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Driver._meta.fields if field.name != "id"]
	pass

@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
	list_display = [field.name for field in DriverProfile._meta.fields if field.name != "id"]
	pass

@admin.register(DriverCampaign)
class DriverCampaignAdmin(admin.ModelAdmin):
	list_display = [field.name for field in DriverCampaign._meta.fields if field.name != "id"]
	pass

@admin.register(DriverDailyEarning)
class DriverDailyEarningAdmin(admin.ModelAdmin):
	list_display = [field.name for field in DriverDailyEarning._meta.fields if field.name != "id"]
	pass

# admin.site.register(Client, ClientAdmin)
# admin.site.register(ClientProfile, ClientProfileAdmin)
# admin.site.register(ClientCampaign, ClientCampaignAdmin)
# admin.site.register(ClientCampaignDetail, ClientCampaignDetailAdmin)
# admin.site.register(ClientCampaignDailyDashboard, ClientCampaignDailyDashboardAdmin)
# admin.site.register(ClientCampaignDashboard, ClientCampaignDashboardAdmin)
# admin.site.register(LocationLog, LocationLogAdmin)
# admin.site.register(TripLog, TripLogAdmin)
# admin.site.register(Driver, DriverAdmin)
# admin.site.register(DriverProfile, DriverProfileAdmin)
# admin.site.register(DriverCampaign, DriverCampaignAdmin)
# admin.site.register(DriverDailyEarning, DriverDailyEarningAdmin)

from django.shortcuts import render,render_to_response
from django.http import JsonResponse
from django.http import HttpResponse
from django.db import models
from django.views.generic import View
# Create your views here.

# class ClientController(object):
#     """docstring for ClientController"""
#     def __init__(self, arg):
#         super(ClientController, self).__init__()
#         self.arg = arg

class ClientDashboardController(View):
	"""ClientDashboardController does the following:
		- ClientDashboard LandingPage
		# - ClientDashboard Start campaign
		# - ClientDashboard Campaign analytics
	"""
	# def __init__(self, arg):
	# 	super(ClientController, self).__init__()
	# 	self.arg = arg
	def create(request):
		# perform client creation task ==> signup
		
		pass

	def login(request):
		# client login

		pass

	
from django.shortcuts import render,render_to_response
from django.http import JsonResponse
from django.http import HttpResponse
from django.db import models
# Create your views here.

# class ClientController(object):
#     """docstring for ClientController"""
#     def __init__(self, arg):
#         super(ClientController, self).__init__()
#         self.arg = arg

def homepage(request):
    return render(request, 'index.html')

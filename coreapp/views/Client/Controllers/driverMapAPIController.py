from django.shortcuts import render,render_to_response
from django.http import JsonResponse
from django.http import HttpResponseRedirect,HttpResponse
from django.views.generic import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..Forms.clientsignupform import RegistrationForm
from coreapp.models import *
from django.template.context_processors import csrf
from django.core.mail import send_mail
import hashlib, datetime, random
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail




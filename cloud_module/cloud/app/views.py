import os
import datetime
import time
import base64
import numpy as np
import cv2
import jsonpickle
import json
from werkzeug import secure_filename


from django.http import JsonResponse
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render
from django.core.files.base import ContentFile


from .models import *
from .serializers import *


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser

from annoying.functions import get_object_or_None


@api_view(['POST'])
def save_image(request, format=None):
	serializer = WebCamSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
		return JsonResponse({'message':'saved image'}, status=200)
	return JsonResponse({'message':'Image cannot saved'}, status=400)


@api_view(['GET'])
def list_images(request, format=None):
	images = WebCamImages.objects.all()
	serializer = WebCamSerializer(images, many=True)
	return Response(serializer.data)
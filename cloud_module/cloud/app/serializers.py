from rest_framework import serializers
from .models import *
from django.conf import settings

import datetime

class WebCamSerializer(serializers.ModelSerializer):
	date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%s")
	class Meta:
		model = WebCamImages
		fields = '__all__'
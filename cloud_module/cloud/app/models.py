import datetime
import time

from django.db import models
from django.conf import settings

class WebCamImages(models.Model):
	image = models.FileField()
	date = models.DateTimeField()
	grayscale = models.BooleanField()

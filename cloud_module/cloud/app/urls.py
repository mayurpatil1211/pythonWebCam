from django.conf.urls import url
from . import views

urlpatterns=[
	url(r'^save_image', views.save_image, name='save_image'),
	url(r'^list_images', views.list_images, name='list_images'),
]

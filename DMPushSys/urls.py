"""DMPushSys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from DMPush.views import code_page, message_page, message_list_api, message_api, message_delete_api, norm_api, \
    norm_delete_api, norm_list_api, code_file_api

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    # page
    url(r'^code/', code_page),
    url(r'^messagelist/', message_page),
    # rest api
    url(r'^message_list/$', message_list_api),
    url(r'^message/$', message_api),
    url(r'^message_delete/$', message_delete_api),
    url(r"norm_list/$", norm_list_api),
    url(r'^norm/$', norm_api),
    url(r'^norm_delete/$', norm_delete_api),
    url(r'^code_file/$', code_file_api),
]

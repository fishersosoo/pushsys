# coding=utf-8

import os

from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render, render_to_response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from serialize import jsonfy, load

# Create your views here.
from DMPush.models import Message, Norm
from DMPushSys.settings import collection


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = data
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def code_page(request):
    collection.insert({"1": "sda"})
    return render_to_response("codes.html")


def message_page(request):
    return render_to_response("messages.html")


@api_view(['GET'])
def message_list_api(request):
    if request.method == 'GET':
        query = dict()
        for key, value in request.GET.iteritems():
            query[key] = value
        messages = Message.find_all(**query)
        if messages is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return JSONResponse(jsonfy(messages))


@api_view(["GET"])
def norm_list_api(request):
    if request.method == 'GET':
        query = dict()
        for key, value in request.GET.iteritems():
            query[key] = value
        norms = Norm.find_all(**query)
        if norms is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return JSONResponse(jsonfy(norms))


@api_view(["GET", "POST"])
def message_api(request):
    if request.method == 'GET':
        query = dict()
        for key, value in request.GET.iteritems():
            query[key] = value
        message = Message.find_one(**query)
        if message is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return JSONResponse(jsonfy(message))
    elif request.method == 'POST':
        query = dict()
        for key, value in request.POST.iteritems():
            query[key] = value
        message = Message.find_one(name=query["name"])
        if message is None:
            message = Message(**query)
            message.save()
            return JSONResponse(jsonfy(message))
        else:
            message.update(**query)
            return JSONResponse(jsonfy(message))


@api_view(["POST"])
def message_delete_api(request):
    if request.method == "POST":
        query = dict()
        for key, value in request.POST.iteritems():
            query[key] = value
        message = Message.find_one(**query)
        if message is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        message.remove()
        return JSONResponse(status=status.HTTP_200_OK, data=jsonfy({'result': 'ok'}))


@api_view(["GET", "POST"])
def norm_api(request):
    if request.method == 'GET':
        query = dict()
        for key, value in request.GET.iteritems():
            query[key] = value
        norm = Norm.find_one(**query)
        if norm is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return JSONResponse(jsonfy(norm))
    elif request.method == 'POST':
        query = dict()
        for key, value in request.POST.iteritems():
            query[key] = value
        norm = Norm.find_one(name=query["name"], belong_message=query["belong_message"])
        if norm is None:
            norm = Norm(**query)
            norm.save()
            return JSONResponse(jsonfy(norm))
        else:
            norm.update(**query)
            return JSONResponse(jsonfy(norm))


@api_view(["POST"])
def norm_delete_api(request):
    if request.method == "POST":
        query = dict()
        for key, value in request.POST.iteritems():
            query[key] = value
        norm = Norm.find_one(**query)
        if norm is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        norm.remove()
        return JSONResponse(status=status.HTTP_200_OK, data=jsonfy({'result': 'ok'}))


@api_view(["GET", "POST"])
def code_file_api(request):
    if request.method == "POST":
        # http://127.0.0.1:8000/code_file/
        #
        file_data = request.FILES["file"]
        file_dir = request.POST["dir"]
        if not os.path.exists("codes_file"):
            os.mkdir("codes_file")
        if not os.path.exists(os.path.join("codes_file", file_dir)):
            os.mkdir(os.path.join("codes_file", file_dir))
        new_file = open(os.path.join(os.path.join("codes_file", file_dir), file_data.name), "w")
        new_file.write(file_data.read())
        new_file.flush()
        new_file.close()
        return Response(status=status.HTTP_200_OK)
    if request.method == "GET":
        """
        http://127.0.0.1:8000/code_file/?file=文件名&dir=目录
        """
        file_name = request.GET["file"]
        file_dir = request.GET["dir"]
        new_file = open(os.path.join(os.path.join("codes_file", file_dir), file_name), "rb")
        response = StreamingHttpResponse(new_file.read())
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = str.format('attachment;filename="{0}"', file_name)
        new_file.close()
        return response

from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from serialize import jsonfy, load

# Create your views here.
from DMPush.models import Message
from DMPushSys.settings import collection


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content =data
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def code_page(request):
    collection.insert({"1": "sda"})
    return render_to_response("codes.html")


def message_page(request):
    return render_to_response("messages.html")


@api_view(['GET'])
def message_list(request,app=None):
    if request.method == 'GET':
        messages = Message.find_all(app="BOBO")
        if messages is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return JSONResponse(jsonfy(messages))


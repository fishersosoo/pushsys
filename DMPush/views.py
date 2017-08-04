# coding=utf-8

import os

import datetime
from bson import ObjectId
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render, render_to_response
from django.utils import log
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from DMPush.apifunction import format_message, get_current_user, send_message, MissingValueError, OverThresholdError, \
    send_all
from serialize import jsonfy, load

# Create your views here.
from DMPush.models import Message, Norm, PeopleGroup, Product
from DMPush.models import Message, Norm, JobTimmer
from DMPushSys.settings import collection, global_config, sched


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = data
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def code_page(request):
    # collection.insert({"1": "sda"})
    return render_to_response("codes.html")


def message_page(request):
    return render_to_response("messages.html")


@api_view(['GET'])
def message_list_api(request):
    if request.method == 'GET':
        query = dict()
        for key, value in request.GET.iteritems():
            if key != "order":
                query[key] = value
        messages = Message.find_all(**query)
        if len(messages) == 0:
            return JSONResponse(jsonfy({"errmsg": "not found"}))
        for message in messages:
            job = JobTimmer.find_one(message_id=ObjectId(message.id))
            if job is not None:
                message.__dict__["timer"] = job.run_time
            else:
                message.__dict__["timer"] = ""
        return JSONResponse(jsonfy(messages))


@api_view(["GET"])
def norm_list_api(request):
    if request.method == 'GET':
        query = dict()
        for key, value in request.GET.iteritems():
            if key != "order":
                query[key] = value
        norms = Norm.find_all(**query)
        if len(norms) == 0:
            return JSONResponse(jsonfy({"errmsg": "not found"}))
        return JSONResponse(jsonfy(norms))


@api_view(["GET", "POST"])
def message_api(request):
    if request.method == 'GET':
        query = dict()
        for key, value in request.GET.iteritems():
            query[key] = value
        message = Message.find_one(**query)
        if message is None:
            return JSONResponse(jsonfy({{"errmsg": "not found"}}))
        return JSONResponse(jsonfy(message))
    elif request.method == 'POST':
        query = dict()
        for key, value in request.POST.iteritems():
            query[key] = value
        if "_id" in query.keys():
            message = Message.find_one(_id=ObjectId(query["_id"]))
        else:
            message = Message.find_one(name=query["name"])
        if message is None:
            message = Message(**query)
            message.save()
            return JSONResponse(jsonfy(message))
        else:
            message.update(**query)
            if "module" in query:
                norms = Norm.find_all(belong_message=str(message.id))
                for norm in norms:
                    norm.update(module=query["module"])
            return JSONResponse(jsonfy(message))


@api_view(["POST"])
def message_delete_api(request):
    if request.method == "POST":
        query = dict()
        for key, value in request.POST.iteritems():
            query[key] = value
        message = Message.find_one(**query)
        if message is None:
            return JSONResponse(jsonfy({"errmsg": "not found"}))
        message.remove()
        norms = Norm.find_all(belong_message=(query["_id"]))
        for norm in norms:
            norm.remove()
        jobs = JobTimmer.find_all(message_id=ObjectId(query["_id"]))
        for job in jobs:
            job.remove()
        return JSONResponse(status=status.HTTP_200_OK, data=jsonfy({'result': 'ok'}))


@api_view(["GET", "POST"])
def norm_api(request):
    if request.method == 'GET':
        query = dict()
        for key, value in request.GET.iteritems():
            query[key] = value
        norm = Norm.find_one(**query)
        if norm is None:
            return JSONResponse(jsonfy({{"errmsg": "not found"}}))
        return JSONResponse(jsonfy(norm))
    elif request.method == 'POST':
        query = dict()
        for key, value in request.POST.iteritems():
            query[key] = value
        if "_id" in query.keys():
            norm = Norm.find_one(_id=ObjectId(query["_id"]))
        else:
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
            return JSONResponse(jsonfy({{"errmsg": "not found"}}))
        norm.remove()
        return JSONResponse(status=status.HTTP_200_OK, data=jsonfy({'result': 'ok'}))


@api_view(["GET"])
def message_str_api(request):
    if request.method == "GET":
        message_id = request.GET.get("id")
        date = (request.GET.get("date"))
        print datetime.datetime.strptime(date,
                                         "%Y-%m-%d").date()
        try:
            return JSONResponse(jsonfy({'message': format_message(message_id=message_id,
                                                                  date=datetime.datetime.strptime(date,
                                                                                                  "%Y-%m-%d").date())}))
        except ValueError, e:
            return JSONResponse(jsonfy({"errmsg": e.message}))
        except KeyError, e:
            errmsg = ""
            for norm in e.message:
                errmsg += norm.name + ", "
            return JSONResponse(jsonfy({"errmsg": errmsg + u"\n指标无法从APP接口获取"}))
        except Exception, e:
            return JSONResponse(jsonfy({"errmsg": "数据出错"}))


@api_view(["GET"])
def send_me_api(request):
    if request.method == "GET":
        try:
            message_id = request.GET.get("id")
            date = (request.GET.get("date"))
            current_user = get_current_user()
            message_str = format_message(message_id=message_id,
                                         date=datetime.datetime.strptime(date,
                                                                         "%Y-%m-%d").date())
            return JSONResponse((send_message(phone=current_user.get("phone"),
                                              msg=message_str,
                                              user_num=global_config.get("staffId"))))
        except ValueError, e:
            return JSONResponse(jsonfy({"errmsg": e.message}))
        except KeyError, e:
            errmsg = ""
            for norm in e.message:
                errmsg += norm.name + ", "
            return JSONResponse(jsonfy({"errmsg": errmsg + u"\n指标无法从APP接口获取"}))
            # except Exception, e:
            #     return JSONResponse(jsonfy({"errmsg": "出错"}))


@api_view(["GET"])
def send_others_api(request):
    if request.method == "GET":
        message_id = request.GET.get("id")
        date = (request.GET.get("date"))
        current_user = get_current_user()
        try:
            message_str = format_message(message_id=message_id,
                                         date=datetime.datetime.strptime(date,
                                                                         "%Y-%m-%d").date(),
                                         check=True)
        except ValueError, e:
            return JSONResponse(jsonfy({"errmsg": e.message}))
        except KeyError, e:
            errmsg = ""
            for norm in e.message:
                errmsg += norm.name + ", "
            return JSONResponse(jsonfy({"errmsg": errmsg + u"\n指标无法从APP接口获取"}))
        except MissingValueError, e:
            errmsg = u"""以下指标数据缺失:\n"""
            for missing_norm in e.norm:
                errmsg += missing_norm.name + ","
            return JSONResponse(jsonfy({"errmsg": errmsg}))
        except OverThresholdError, e:
            errmsg = u"""以下指标超过阈值:\n"""
            for missing_norm in e.norm:
                errmsg += missing_norm.name + ","
            return JSONResponse(jsonfy({"errmsg": errmsg}))
        # 数据合格，给领导发送
        fail_list = []
        success_list = []
        people_list = Message.find_one(_id=message_id).people_list
        for name, phone in load(people_list).iteritems():
            result = load(send_message(phone=phone,
                                       msg=message_str,
                                       user_num=global_config.get("staffId")))
            if result["errmsg"] != u"请求成功":
                fail_list.append(name)
            else:
                success_list.append(name)
        error_msg = u"成功发送给：\n"
        for one in success_list:
            error_msg += one + " "
        if len(fail_list) != 0:
            error_msg += u"\n以下发送失败：\n"
            for one in fail_list:
                error_msg += one + " "
        else:
            error_msg += u"\n全部成功"
        return JSONResponse(jsonfy({"errmsg": error_msg}))


@api_view(["GET", "POST"])
def people_group_api(request):
    if request.method == "GET":
        groups = PeopleGroup.find_all()
        return JSONResponse(jsonfy(groups))
    elif request.method == "POST":
        group_name = request.POST.get('group_name')
        people_list = load(request.POST.get("people_list"))
        # print people_list
        group = PeopleGroup.find_one(group_name=group_name)
        if group is None:
            group = PeopleGroup(group_name=group_name, people_list=people_list)
            group.save()
        else:
            group.update(people_list=people_list)
        return JSONResponse(jsonfy(group))


@api_view(["GET"])
def job_list_api(request):
    if request.method == 'GET':
        query = dict()
        for key, value in request.GET.iteritems():
            if key != "order":
                query[key] = value
        jobs = JobTimmer.find_all(**query)
        if len(jobs) == 0:
            return JSONResponse(jsonfy([]))
        return JSONResponse(jsonfy(jobs))


@api_view(["POST"])
def job_add_api(request):
    if request.method == 'POST':
        message_id = request.POST.get("message_id")
        run_time = request.POST.get("run_time")
        job = JobTimmer.find_one(message_id=ObjectId(message_id))
        if job is not None:
            job.remove()
        job = JobTimmer(message_id=ObjectId(message_id), run_time=run_time)
        job.save()
        return JSONResponse(jsonfy(job))


@api_view(["POST"])
def job_del_api(request):
    if request.method == 'POST':
        message_id = request.POST.get("message_id")
        job = JobTimmer.find_one(message_id=ObjectId(message_id))
        if job is not None:
            job.remove()
            return JSONResponse(status=status.HTTP_200_OK, data=jsonfy({'result': 'ok'}))
        return JSONResponse(status=status.HTTP_200_OK, data=jsonfy({'errmsg': 'not found'}))


@api_view(["GET"])
def product_list_api(request):
    if request.method == "GET":
        query = dict()
        for key, value in request.GET.iteritems():
            if key != "order":
                query[key] = value
        products = Product.find_all()
        # for product in products:
        #     product.remove()
        return JSONResponse(jsonfy(products))


@api_view(["GET", "POST"])
def product_api(request):
    product = None

    if request.method == "GET":
        query = dict()
        for key, value in request.GET.iteritems():
            if key != "order":
                query[key] = value
            product = Product.find_one(**query)
            return JSONResponse(jsonfy(product))

    elif request.method == 'POST':
        # print request.POST
        query = dict()
        for key, value in request.POST.iteritems():
            query[key] = value
        if "_id" in query.keys() and query["_id"] != u"":
            product = Product.find_one(_id=ObjectId(query["_id"]))
        if product is None:
            # 新增
            print "new product"
            if Product.find_one(name=(query["name"])):
                return JSONResponse(jsonfy({"errmsg": "产品已存在"}))
            product = Product(**query)
            product.add_job()
            product.save()
            return JSONResponse(jsonfy(product))
        else:
            print "edit product"
            # 修改
            product.update(**query)
            return JSONResponse(jsonfy(product))


@api_view(["POST"])
def product_del_api(request):
    if request.method == "POST":
        # print request.POST
        product = Product.find_one(_id=ObjectId(request.POST.get("_id")))
        if product is None:
            return JSONResponse(jsonfy({{"errmsg": "not found"}}))
        product.remove()
        return JSONResponse(status=status.HTTP_200_OK, data=jsonfy({'result': 'ok'}))

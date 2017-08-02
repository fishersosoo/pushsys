# coding=utf-8
import json

import datetime
import requests

from DMPush.models import Message, Norm
from DMPushSys.settings import global_config


def get_app_data(**kwargs):
    r = requests.get(
        "http://dm.sjfx.163.gz:8088/app/detail/", params=kwargs)
    return json.loads(r.text), r.request.url


# print get_app_data(
#     module="ent",
#     room_id="all",
#     template_id="all",
#     terminal_id="all",
#     date="2016/03/14",
#     staffId="g7079"
# )


def send_message(phone=None, msg=None, user_num=None):
    r = requests.get("http://60.191.80.5/app/yixin_send/",
                     params={
                         "phone_number": phone,
                         "msg": msg,
                         "send_user_num": user_num
                     })
    return json.loads(r.text)


#
# send_message(phone="13610019895",
#              msg="test",
#              user_num="GZS10558")
class MissingValueError(RuntimeError):
    def __init__(self, norm):
        self.norm = norm


def format_message(message_id=None, date=datetime.date.today(), ignore_missing=True):
    isOverThreshold = False
    message_str = ""
    message = Message.find_one(_id=message_id)
    message_str += message.name + "_" + date.strftime("%Y-%m-%d")
    norms = Norm.find_all(belong_message=str(message.id))
    data_dir = {}
    missing_norms = []
    fail_norms = []
    for norm in norms:
        if norm.app_name not in data_dir:
            app_data, url = get_app_data(
                module=norm.module,
                room_id=norm.room_id,
                template_id=norm.template_id,
                terminal_id=norm.terminal_id,
                date=date.strftime("%Y/%m/%d"),
                staffId=global_config.get("staffId")
            )
            if "data" not in app_data:
                raise ValueError(url + "接口无数据")
            for group in app_data.get("data"):
                for onedata in group.get("data"):
                    data_dir[onedata.get("name")] = onedata
        if norm.app_name not in data_dir:
            fail_norms.append(norm)
            continue

        if not ignore_missing and isMissing(data_dir[norm.app_name]["value"]):
            missing_norms.append(norm)
            continue
        message_str += "\n" + norm.name + ":" + data_dir[norm.app_name]["value"]
        if data_dir[norm.app_name].get("percent") != None:
            if not ignore_missing and isMissing(data_dir[norm.app_name].get("percent")):
                missing_norms.append(norm)
                continue
            message_str += "(" + data_dir[norm.app_name].get("percent") + ")"
            threshold = int(norm.threshold)
            if not isMissing(data_dir[norm.app_name].get("percent")) and threshold != 0:
                data_dir[norm.app_name].get("percent")
                percent = float(data_dir[norm.app_name].get("percent")[0:-1])
                if abs(percent) >= threshold:
                    isOverThreshold = True
        message_str += ";"
    if len(fail_norms) != 0:
        raise KeyError(fail_norms)
    if len(missing_norms) != 0:
        raise MissingValueError(missing_norms)
    if isOverThreshold:
        message_str += "\n" + message.desc
        message_str = message_str.replace(u"￥", u"")
    return message_str


def get_current_user():
    return {
        "staffId": "g7079",
        "phone": "13610019895"
    }


def isMissing(value):
    missing_values = [u'0', u'0.0%', u'--', u"￥0", u"￥--"]
    if value in missing_values:
        return True
    return False

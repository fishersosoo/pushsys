# coding=utf-8
import json

import requests


def get_app_data(**kwargs):
    r = requests.get(
        "http://dm.sjfx.163.gz:8088/app/detail/=", params=kwargs)
    return json.loads(r.text)


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

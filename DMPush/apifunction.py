# coding=utf-8
import json
import datetime

import logging
import requests

from DMPush.decorators import logged
from DMPush.models import Message, Norm, Product
from DMPushSys.settings import global_config, sched


def get_app_data(**kwargs):
    r = requests.get(
        "http://dm.sjfx.163.gz:8088/app/detail/", params=kwargs)
    return json.loads(r.text), r.request.url


def send_all(**kwargs):
    messages = Message.find_all(**kwargs)
    date = datetime.datetime.strptime(kwargs["date"], "%Y-%m-%d").date() \
        if "date" in kwargs \
        else datetime.datetime.now().date() - datetime.timedelta(days=1)
    for message in messages:
        try:
            message_str = format_message(message_id=message.id,
                                         date=date,
                                         check=True)
        except ValueError, e:
            return {"errmsg": e.message}
        except KeyError, e:
            errmsg = ""
            for norm in e.message:
                errmsg += norm.name + ", "
            return {"errmsg": errmsg + u"\n指标无法从APP接口获取"}
        except MissingValueError, e:
            errmsg = u"""以下指标数据缺失:\n"""
            for missing_norm in e.norm:
                errmsg += missing_norm.name + ","
            return {"errmsg": errmsg}
        except OverThresholdError, e:
            errmsg = u"""以下指标超过阈值:\n"""
            for missing_norm in e.norm:
                errmsg += missing_norm.name + ","
            return {"errmsg": errmsg}
        people_list = message.people_list
        # print people_list.__class__
        for name, phone in json.loads(people_list).iteritems():
            send_message(phone=phone,
                         msg=message_str,
                         user_num=global_config.get("staffId"))
            # except Exception, e:
            #     logger.error(e)


def startSched():
    import logging
    logging.basicConfig()
    Product.send_func.append(send_all)
    prodocts = Product.find_all()
    for prodoct in prodocts:
        if prodoct.run_time != "":
            prodoct.add_job()
    sched.print_jobs()
    sched.start()


def send_missing_alert(missing_norm, date="", message_name=""):
    error_msg = u"""指标数据缺失
所属消息:\n{message_name};
app指标名:\n{app_name};
来源表:\n{table_name};
来源字段:\n{field};
缺失日期:\n{date};""".format(message_name=message_name, app_name=missing_norm.app_name, table_name=missing_norm.table_name,
                         field=missing_norm.field,
                         date=date)
    send_message(phone=missing_norm.phone,
                 msg=error_msg,
                 user_num=global_config.get("staffId"))


def send_threshold_alert(missing_norm, date="", message_name="", percent=""):
    error_msg = u"""指标数据超过阈值
所属消息:\n{message_name};
app指标名:\n{app_name};
来源表:\n{table_name};
来源字段:\n{field};
数据日期:\n{date};
百分比:\n{desc};""".format(message_name=message_name, app_name=missing_norm.app_name, table_name=missing_norm.table_name,
                        field=missing_norm.field,
                        date=date, desc=percent)
    send_message(phone=missing_norm.phone,
                 msg=error_msg,
                 user_num=global_config.get("staffId"))


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


class OverThresholdError(RuntimeError):
    def __init__(self, norm):
        self.norm = norm


def format_message(message_id=None, date=datetime.date.today() - datetime.timedelta(days=1), check=False):
    is_over_threshold = False
    message_str = ""
    message = Message.find_one(_id=message_id)
    message_str += message.name + "_" + date.strftime("%Y%m%d")
    norms = Norm.find_all(belong_message=str(message.id))
    data_dir = {}
    missing_norms = []
    fail_norms = []
    over_threshold_norms = []
    for norm in norms:
        if norm.app_name not in data_dir:
            # 指标之前没有获取过
            app_data, url = get_app_data(
                module=norm.module,
                room_id=norm.room_id,
                template_id=norm.template_id,
                terminal_id=norm.terminal_id,
                date=date.strftime("%Y/%m/%d"),
                staffId=global_config.get("staffId")
            )
            if "data" not in app_data:
                # app数据解析失败u
                raise ValueError(url + "接口无数据")
            for group in app_data.get("data"):
                for onedata in group.get("data"):
                    data_dir[onedata.get("name")] = onedata
        if norm.app_name not in data_dir:
            # 指标不在APP数据中
            fail_norms.append(norm)
            continue
        if check and isMissing(data_dir[norm.app_name]["value"]):
            # 指标缺失
            send_missing_alert(norm, date=date.strftime("%Y%m%d"), message_name=message.name)
            missing_norms.append(norm)
            continue
        message_str += "\n" + norm.name + ":\n" + data_dir[norm.app_name]["value"]
        if data_dir[norm.app_name].get("percent") is not None:
            # 有百分比
            if check:
                if isMissing(data_dir[norm.app_name].get("percent")):
                    # 指标缺失
                    send_missing_alert(norm, date=date.strftime("%Y%m%d"), message_name=message.name)
                    missing_norms.append(norm)
                    continue
                else:
                    threshold = int(norm.threshold)
                    if threshold != 0 and abs(float(data_dir[norm.app_name].get("percent")[0:-1])) > threshold:
                        # 阈值警告
                        send_threshold_alert(norm, date=date.strftime("%Y%m%d"), message_name=message.name,
                                             percent=data_dir[norm.app_name].get("percent"))
                        is_over_threshold = True
                        over_threshold_norms.append(norm)
                        continue
            message_str += "(" + data_dir[norm.app_name].get("percent") + ")"
        message_str += ";"
    if len(fail_norms) != 0:
        raise KeyError(fail_norms)
    if len(missing_norms) != 0:
        raise MissingValueError(missing_norms)
    if is_over_threshold:
        raise OverThresholdError(over_threshold_norms)
    message_str = message_str.replace(u"￥", u"")
    if message.desc != "":
        message_str += u"\n说明:\n" + message.desc + ";"
    return message_str


def get_current_user():
    return {
        "staffId": "g7079",
        "phone": "13610019895"
    }


def isMissing(value):
    missing_values = [u'0', u'0.0%', u'--', u"￥0", u"￥--", u"", "0"]
    if value in missing_values:
        return True
    return False

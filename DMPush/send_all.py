# coding=utf-8
import datetime

from DMPush.apifunction import format_message, MissingValueError, send_message, OverThresholdError
from DMPush.models import Message
from DMPush.serialize import load

staffId = "g7079"


def send_all(**kwargs):
    messages = Message.find_all(**kwargs)
    date = datetime.datetime.strptime(kwargs["date"], "%Y-%m-%d").date()\
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
        for name, phone in load(people_list).iteritems():
            send_message(phone=phone,
                         msg=message_str,
                         user_num=staffId)


if __name__ == "__main__":
    send_all()

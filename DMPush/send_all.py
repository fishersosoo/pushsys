# coding=utf-8
import datetime

from DMPush.apifunction import format_message, MissingValueError, send_message
from DMPush.models import Message
from DMPush.serialize import load

staffId = "g7079"
if __name__ == "__main__":
    messages = Message.find_all()
    for message in messages:
        try:
            message_str = format_message(message_id=messages.id,
                                         date=datetime.datetime.now().date(),
                                         ignore_missing=False)
        except MissingValueError, e:
            missing_norm = e.norm
            error_msg = missing_norm.app_name + u"数据缺失"
            send_message(phone=missing_norm.phone,
                         msg=error_msg,
                         user_num=staffId)
        people_list = message.people_list
        for name, phone in load(people_list).iteritems():
            send_message(phone=phone,
                         msg=message_str,
                         user_num=staffId)

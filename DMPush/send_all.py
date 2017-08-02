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
            message_str = format_message(message_id=message.id,
                                         date=datetime.datetime.now().date(),
                                         ignore_missing=False)
        except MissingValueError, e:
            errmsg = u"""以下指标数据缺失:\n"""
            for missing_norm in e.norm:
                errmsg += missing_norm.name
                error_msg = u"""指标数据缺失
app指标名:{app_name}
来源表:{table_name}
来源字段:{field}
缺失日期:{date}
                            """.format(app_name=missing_norm.app_name, table_name=missing_norm.table_name,
                                       field=missing_norm.field,
                                       date=datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d"))
                send_message(phone=missing_norm.phone,
                             msg=error_msg,
                             user_num=staffId)
        people_list = message.people_list
        for name, phone in load(people_list).iteritems():
            send_message(phone=phone,
                         msg=message_str,
                         user_num=staffId)

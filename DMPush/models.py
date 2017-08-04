# coding=utf-8
import json

import datetime
import logging

from bson import ObjectId

from DMPush.decorators import logged
from DMPushSys.settings import collection, sched


class DMBaseModel(object):
    def __init__(self, **kwargs):
        for key in self.__class__.fields:
            if key not in kwargs.keys() and key != "_id":
                if key == "_id" and kwargs[key] == u"":
                    kwargs.pop(key)
                else:
                    kwargs[key] = ""
        self.__dict__.update(kwargs)

    @logged(logging.DEBUG)
    def save(self):
        self.__dict__.update(data_type=self.__class__.__name__)
        collection.insert(self.__dict__)

    @logged()
    def remove(self):
        self.__dict__.update(data_type=self.__class__.__name__)
        collection.remove(self.__dict__)

    @logged()
    def update(self, **kwargs):
        for key in kwargs:
            if key not in self.__class__.fields:
                raise KeyError("key " + str(key) + " not in fields")
        self.__dict__.update(data_type=self.__class__.__name__)
        if "_id" in kwargs.keys():
            kwargs.pop("_id")
        collection.update(self.__dict__, {"$set": kwargs})
        for key, value in kwargs.iteritems():
            self.__dict__[key] = value

    @classmethod
    @logged(logging.DEBUG)
    def find_one(cls, **kwargs):
        for key in kwargs:
            if key not in cls.fields:
                raise KeyError("key " + str(key) + " not in fields")
        if "_id" in kwargs.keys():
            # print "_id:", kwargs["_id"]
            result = collection.find_one({"_id": ObjectId(kwargs["_id"])})
            if result == None:
                return None
            return cls(**result)
        else:
            kwargs.update(data_type=cls.__name__)
            result = collection.find(kwargs)
            if result.count() == 0:
                return None
            return cls(**(result[0]))

    @classmethod
    @logged(logging.DEBUG)
    def find_all(cls, **kwargs):
        for key in kwargs:
            if key not in cls.fields:
                raise KeyError("key " + str(key) + " not in fields")
        kwargs.update(data_type=cls.__name__)
        results = collection.find(kwargs)
        if results.count() == 0:
            return list()
        object_list = list()
        for result in results:
            # print result
            object_list.append(cls(**result))
        return object_list

    @property
    def id(self):
        return self._id


class Message(DMBaseModel):
    fields = ["name", "app", "desc", "module", "people_list", "_id"]


class Norm(DMBaseModel):
    fields = ["belong_message", "name", "module", "template_id", "terminal_id", "room_id", "app_name",
              "table_name", "field", "incharge", "phone", "_id", "threshold"]


class PeopleGroup(DMBaseModel):
    fields = ["group_name", "people_list", "_id"]


class JobTimmer(DMBaseModel):
    fields = ["_id", "message_id", "run_time"]


class Product(DMBaseModel):
    send_func = []
    fields = ["_id", "name", "run_time"]

    @logged()
    def add_job(self):
        if self.run_time == "":
            return
        print"add " + str(sched.add_job(func=Product.send_func[0], trigger="cron",
                                        hour=datetime.datetime.strptime(self.run_time, "%H:%M").hour,
                                        minute=datetime.datetime.strptime(self.run_time, "%H:%M").minute,
                                        kwargs={"app": self.name}, id=self.name, name=self.name))

    @logged()
    def remove(self):
        job = sched.get_job(job_id=self.name)
        if job is not None:
            print "delete " + str(job)
            sched.remove_job(job_id=job.id)
        super(Product, self).remove()

    @logged()
    def update(self, **kwargs):
        job = sched.get_job(job_id=self.name)
        super(Product, self).update(**kwargs)
        if "name" in kwargs:
            if job is not None:
                sched.print_jobs()
                print "modify"
                new_job = sched.add_job(func=job.func, trigger=job.trigger, name=kwargs["name"], id=kwargs["name"],
                                        kwargs={"app": kwargs["name"]})
                job.remove()
                job = new_job
                sched.print_jobs()
        if "run_time" in kwargs:
            if job is not None:
                if kwargs["run_time"] != "":
                    job = job.reschedule(trigger="cron",
                                         hour=datetime.datetime.strptime(self.run_time, "%H:%M").hour,
                                         minute=datetime.datetime.strptime(self.run_time, "%H:%M").minute,
                                         )
                    print "reschedule " + str(job)
                else:
                    print "delete " + str(job)
                    sched.remove_job(job_id=job.id)

            else:
                print "add " + str(sched.add_job(func=Product.send_func[0], trigger="cron",
                                                 hour=datetime.datetime.strptime(self.run_time, "%H:%M").hour,
                                                 minute=datetime.datetime.strptime(self.run_time, "%H:%M").minute,
                                                 kwargs={"app": self.name}, id=self.name, name=self.name))

# coding=utf-8
import json

from bson import ObjectId

from DMPushSys.settings import collection


class DMBaseModel(object):
    def __init__(self, **kwargs):
        for key in self.__class__.fields:
            if key not in kwargs.keys() and key != "_id":
                raise KeyError("key " + str(key) + " is required")
        self.__dict__.update(kwargs)

    def save(self):
        self.__dict__.update(data_type=self.__class__.__name__)
        collection.insert(self.__dict__)

    def remove(self):
        self.__dict__.update(data_type=self.__class__.__name__)
        collection.remove(self.__dict__)

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
    def find_one(cls, **kwargs):
        for key in kwargs:
            if key not in cls.fields:
                raise KeyError("key " + str(key) + " not in fields")
        if "_id" in kwargs.keys():
            print "_id:", kwargs["_id"]
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

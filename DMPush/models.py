# coding=utf-8
from DMPushSys.settings import collection


class DMBaseModel(object):
    def __init__(self, **kwargs):
        for key in self.__class__.fields:
            if key not in kwargs.keys():
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
        collection.update(self.__dict__, {"$set": kwargs})
        for key, value in kwargs.iteritems():
            self.__dict__[key] = value

    @classmethod
    def find_one(cls, **kwargs):
        for key in kwargs:
            if key not in cls.fields:
                raise KeyError("key " + str(key) + " not in fields")
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
            return None
        object_list = list()
        for result in results:
            object_list.append(cls(**result))
        return object_list


class Message(DMBaseModel):
    fields = ["name", "app", "desc", "module", "people_list"]


class Norm(DMBaseModel):
    fields = ["belong_message", "name", "app_module", "app_template", "app_client", "app_room", "app_name",
              "table_name", "field", "incharge", "phone"]
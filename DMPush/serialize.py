import json

from bson import ObjectId

from DMPush.models import DMBaseModel


def serialize(obj):
    if isinstance(obj, DMBaseModel):
        return obj.__dict__
    if isinstance(obj, ObjectId):
        return str(obj)
    return json.dumps(obj)


def jsonfy(obj):
    return json.dumps(obj, default=serialize)


def load(json_s):
    return json.loads(json_s)

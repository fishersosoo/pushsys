import datetime
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.util import maybe_ref
from pymongo import MongoClient

from DMPush.apifunction import send_all

try:
    import cPickle as pickle
except ImportError:  # pragma: nocover
    import pickle

class DMMongoDBJobStore(MongoDBJobStore):
    def __init__(self, database='apscheduler', collection='jobs', client=None,
                 pickle_protocol=pickle.HIGHEST_PROTOCOL, **connect_args):
        super(MongoDBJobStore, self).__init__()
        self.pickle_protocol = pickle_protocol

        if not database:
            raise ValueError('The "database" parameter must not be empty')
        if not collection:
            raise ValueError('The "collection" parameter must not be empty')

        if client:
            self.client = maybe_ref(client)
        else:
            connect_args.setdefault('w', 1)
            self.client = MongoClient(**connect_args)

        self.collection = collection

conn = MongoClient("10.255.207.118", 27017)
db = conn.cc_system
db.authenticate("liangzhanning", "liangzhanning##20170713")
collection = db.messages_send
jobstores = {
    'mongo': DMMongoDBJobStore(collection=collection, database='cc_system', client=conn)
}
sched = BlockingScheduler(jobstores=jobstores)
sched.print_jobs(jobstore='mongo')
sched.add_job(func=send_all, trigger="cron",
                                    hour=datetime.datetime.strptime(u"23:22", "%H:%M").hour,
                                    minute=datetime.datetime.strptime(u"23:22", "%H:%M").minute,
                                    kwargs={"app": "CC"}, name="CC",jobstore='mongo')
sched.print_jobs(jobstore='mongo')
sched.start()

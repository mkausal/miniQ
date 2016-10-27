from miniQ.src.helpers import generate_long_id
from miniQ.src.mongo_wrapper import MongoWrapper
import datetime
import logging

logger = logging.getLogger(__name__)


class MiniQ(object):
    def __init__(self):
        self.messages_coll = MongoWrapper().get_mongo_collection('messages')
        # Time in which we expect a processed ACK from client - in seconds
        self.turn_around_time = 5


    def store_message(self, message, id):
        # Mark every message as unread and not processed by default
        self.messages_coll.insert({'_id': id, 'msg': message, 'status': {'read': False, 'processed': False}})

    def update_message_read_status(self, ids, status=True):
        # Mark every message as unread by default
        self.messages_coll.update({'_id': {'$in': ids}}, {'$set': {'status': {'read': status, 'processed': False},
                                                                   'ut': {'read': datetime.datetime.utcnow()}}})

    def write_to_Q(self, message):
        message_id = generate_long_id()
        self.store_message(message, message_id)
        # print "Written {0} to MiniQ".format(message)
        logger.debug("Written {0} to MiniQ".format(message))
        return message_id

    def get_unread_messages(self):
        unread_messages = list(self.messages_coll.find({'status.read': False}))
        return unread_messages

    def get_unprocessed_messages(self):
        spec = {'status.read': True,
                'ut.read': {'$lt': datetime.datetime.utcnow() - datetime.timedelta(seconds=self.turn_around_time)}}
        unprocessed_messages = list(self.messages_coll.find(spec))
        return unprocessed_messages

    def read_from_Q(self):
        unread_messages = self.get_unread_messages()
        message_ids = [x['_id'] for x in unread_messages]
        unprocessed_messages = self.get_unprocessed_messages()
        # Update unread message status
        self.update_message_read_status(message_ids)
        return unread_messages + unprocessed_messages

    def delete_messages(self, id):
        self.messages_coll.remove({'_id': id})

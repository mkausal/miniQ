import random
import logging

logger = logging.getLogger(__name__)


MAX_64BIT_INT = 2**63 - 1 #64-bit integer


def generate_long_id():
    return random.randint(0, MAX_64BIT_INT)


def notify_server(message_id):
    from miniQ.src.miniQ_models import MiniQ
    try:
        MiniQ().delete_messages(message_id)
    except:
        logger.critical("Error in deleting message ID {0}".format(message_id))
        return
    # print "Deleted message ID {0}".format(message_id)
    logger.debug("Notified server and deleted message ID {0}".format(message_id))
from miniQ.src.miniQ_models import MiniQ
from miniQ.src.helpers import notify_server
from multiprocessing import Process
import logging

logger = logging.getLogger(__name__)


def push_message(params):
    """
        This API pushes new message to the broker

        Args:
            params (dict): A dict with 'msg' indicating message text. Chosen dict, as it will be extensible without
            changing API parameters multiple times, for any future requirements

        Method Type:
            POST

        Returns:
            dict:a dict contain success and data containing the success or failure message

    """
    if 'msg' not in params:
        return {'success': False, 'data': 'msg is a required key'}
    try:
        written_msg_id = MiniQ().write_to_Q(params['msg'])
    except Exception as e:
        return {'success': False, 'data': 'Error storing message {0}'.format(e)}
    return {'success': True, 'data': 'Written msg with ID {0}'.format(written_msg_id)}


def read_messages():
    """
        This API reads unread and unprocessed messages from the broker

        Args:
            No Args, as the requirement is to read all available messages at any time. If required, can be modified

        Method Type:
            GET

        Returns:
            dict:a dict contain success (always True) and data containing all the messages

    """
    try:
        all_messages = MiniQ().read_from_Q()
    except Exception as e:
        return {'success': False, 'data': 'Error retrieving message {0}'.format(e)}

    for message in all_messages:
        # Make it run async
        p = Process(target=notify_server, args=(message['_id'],))
        p.start()
        p.join()
        # print "Processed message ID {0}".format(message['_id'])
        logger.info("Processed message ID {0}".format(message['_id']))
    # print len(all_messages)
    return {'success': True, 'data': all_messages}

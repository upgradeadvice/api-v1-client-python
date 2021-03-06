"""This module corresponds to functionality documented
at https://blockchain.info/api/api_receive
"""

from .. import util
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
import json

class ReceiveResponse:

    def __init__(self, address, index, callback):
        self.address = address
        self.index = index
        self.callback_url = callback

class LogEntry:

    def __init__(self, callback_url, called_at, raw_response, response_code):
        self.callback_url = callback_url
        self.called_at = called_at
        self.raw_response = raw_response
        self.response_code = response_code

def receive(xpub, callback, api_key):
    """Call the 'api/receive' endpoint and create a forwarding address.

    :param str xpub: extended public key to generate payment address
    :param str callback: callback URI that will be called upon payment
    :param str api_key: Blockchain.info API V2 key
    :return: an instance of :class:`ReceiveResponse` class
    """

    params = {'xpub': xpub, 'key': api_key, 'callback': callback }
    resource = 'v2/receive?' + urlencode(params)
    resp = util.call_api(resource, base_url = 'https://api.blockchain.info/')
    json_resp = json.loads(resp)
    payment_response = ReceiveResponse(json_resp['address'],
                                        json_resp['index'],
                                        json_resp['callback'])
    return payment_response

def callback_log(callback, api_key):
    params = {'key': api_key, 'callback': callback }
    resource = 'v2/receive/callback_log?' + urlencode(params)
    resp = util.call_api(resource, base_url = 'https://api.blockchain.info/')
    json_resp = json.loads(resp)
    return [ LogEntry(e['callback'], e['called_at'], e['raw_response'], e['response_code']) for e in json_resp]

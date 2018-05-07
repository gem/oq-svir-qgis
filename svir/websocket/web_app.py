from uuid import uuid4
import json


class WebApp(object):

    def __init__(self, wss, app_name=None):
        assert app_name is not None
        self.wss = wss  # thread running the websocket server
        self.app_name = app_name
        # self.allowed_meths = ['window_open']
        self.allowed_meths = ['window_open']
        self.pending = {}

    def run_command(self, command, args=()):
        # called when IRMT wants to send a command to the websocket
        if command not in self.allowed_meths:
            return 'Method "%s" not allowed' % command
        uuid = uuid4().get_urn()[9:]
        api_msg = {
            'uuid': uuid,
            'msg': {
                'command': command,
                'args': args
            }
        }
        self.send(api_msg)
        self.pending[uuid] = api_msg

    def receive(self, api_msg):
        # it happens when the websocket receives a message
        api_uuid = api_msg['uuid']
        if 'reply' in api_msg:
            app_msg = api_msg['reply']
            uuid = api_msg['uuid']
            if uuid in self.pending:
                print("Command pending found [%s]" % uuid)
                # FIXME: call CB
                if ('complete' not in app_msg or
                        app_msg['complete'] is True):
                    print("Command pending deleted [%s]" % uuid)
                    del self.pending[uuid]
            return
        else:
            app_msg = api_msg['msg']
            command = app_msg['command']
            if command not in self.allowed_meths:
                api_reply = {
                    'uuid': api_uuid,
                    'reply': {
                        'success': False,
                        'msg': 'Method "%s" not allowed' % command
                    }
                }
                self.send(api_reply)

            args = app_msg['args']
            meth = getattr(self, command)

            # FIXME: manage command exception
            ret = meth(*args)

            api_reply = {'uuid': api_uuid, 'reply': ret}
            self.send(api_reply)

    def send(self, api_msg):
        # it sends a message to the websocket
        hyb_msg = {'app': self.app_name, 'msg': api_msg}
        hyb_msg_str = json.dumps(hyb_msg)
        hyb_msg_unicode = unicode(hyb_msg_str, 'utf-8')
        self.wss.irmt_thread.send_to_wss_sig.emit(hyb_msg_unicode)
        # ret = self.wss.send_message(hyb_msg)
        # if ret is False:
        #     print('Send failed! No connections')

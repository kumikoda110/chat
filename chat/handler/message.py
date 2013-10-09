# coding: utf-8
import tornado.websocket

from chat.model.client import Client
from chat.chat import _CLIENTS_MAP, _CHANNEL


class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        _id = str(id(self))
        kwags = {
            "webSocketHandler": self,
            "email": self.get_secure_cookie('email'),
            "nickname": self.get_secure_cookie('nickname')
        }
        client = Client(_id, **kwags)
        _CLIENTS_MAP[_id] = client
        #self.write_message("欢迎进入聊天室！")

    def send_to_all(self, message):
        r = self.settings['redis']
        r.publish(_CHANNEL, message)

    def on_message(self, message):
        print message

    def on_close(self):
        del _CLIENTS_MAP[str(id(self))]
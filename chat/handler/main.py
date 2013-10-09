# coding: utf-8
import json
import tornado.web
from tornado.log import app_log
from chat.define import ChatSigletonDefine
from chat.util import getAvatar
from chat.handler import BaseHandler


class MainHandler(BaseHandler):

    def initialize(self):
        self.clients = ChatSigletonDefine.get_singleton_instance().clients
        self.channel = ChatSigletonDefine.get_singleton_instance().channel

    @tornado.web.authenticated
    def get(self):
        email = self.get_secure_cookie('email')

        app_log.debug(self.clients)
        params = {
            "avatar": getAvatar(self.get_secure_cookie('email')),
            "email": email,
            "nickname": self.get_secure_cookie('nickname'),
            "clients": self.clients
        }
        self.render("index.html", **params)

    @tornado.web.authenticated
    def post(self):
        message = self.get_argument("data")
        data = {
            "email": self.get_secure_cookie('email'),
            "nickname": self.get_secure_cookie('nickname'),
            "avatar": getAvatar(self.get_secure_cookie('email')),
            "message": message,
            "type": "normal"
        }
        r = self.settings['redis']
        r.publish(self.channel, json.dumps(data))

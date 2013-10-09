#!/usr/bin/env python

import logging
import os.path
from tornado import web, escape
from tornado.ioloop import IOLoop
from tornado import gen
from tornado.options import define, options, parse_command_line

define("port", default=8888, type=int)

class TwitHandler(web.RequestHandler):
    def get_username_id(self, username):
        return 0

class GetFeed(TwitHandler):
    def get(self, user):
        messages = []
        self.render("index.html", messages=messages)

class PostMessage(TwitHandler):
    def post(self):
        msg = self.get_argument("msg")
        user = self.get_argument("user")
        id = self.get_username_id(user)
        message = {
            "id": id,
            "from": user,
            "msg": msg,
        }
        # store msg

class GetFeed(TwitHandler):
    def get(self, username):
        pass

class CreateUser(TwitHandler):
    def post(self):
        username = self.get_argument("username")

def main():
    parse_command_line()
    app = web.Application([
            (r"/create", CreateUser),
            (r"/post", PostMessage),
            (r"/follow", Follow),
            (r"/unfollow", Unfollow),
            (r"/feed/(\w+)", GetFeed),
            (r"/globalfeed", GetGlobalFeed),
            ],
        )
    app.listen(options.port)
    IOLoop.instance().start()

if __name__ == "__main__":
    main()

#!/usr/bin/env python

import os.path
from tornado import web, escape, httpserver
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_command_line
#from tornado import auth
import torndb

define('port', default=8888, help='run on the given port', type=int)
define('mysql_host', default='127.0.0.1:3306', help='database host')
define('mysql_database', default='twit', help='database name')
define('mysql_user', default='twit', help='database user')
define('mysql_password', default='', help='database password')

class Application(web.Application):
    def __init__(self):
        handlers = [
            (r'/', HomeHandler),
            (r'/post', PostMessage),
            (r'/follow', Follow),
            (r'/unfollow', Unfollow),
            (r'/feed/(\w+)', GetFeed),
            (r'/globalfeed', GetGlobalFeed),
            (r'/create', CreateUser),
            (r'/login/(\w+)', Login),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            debug=True,
        )
        web.Application.__init__(self, handlers, **settings)
        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)

class BaseHandler(web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_user_by_id(self, user_id):
        return self.db.get('select * from users where id=%s', int(user_id))

    def get_current_user(self):
        user_id = self.get_cookie('user_id')
        if not user_id:
            return None
        return self.get_user_by_id(user_id)

class CreateUser(BaseHandler):
    def post(self):
        username = self.get_argument('username')
        user_id = self.db.execute('insert into users (username) values (%s)', username)
        self.set_cookie('user_id', str(user_id))
        self.set_cookie('username', username)
        self.redirect('/')

class Login(BaseHandler):
    def get(self, user_id):
        user = self.get_user_by_id(user_id)
        if user:
            self.set_cookie('user_id', user_id)
            self.set_cookie('username', user.username)
        self.redirect('/')

class GetFeed(BaseHandler):
    def get(self, user_id):
        user = self.get_user_by_id(user_id)
        msgs = self.db.query('select * from msgs where user_id=%s order by created desc limit 20',
            user.id)
        self.render('feed.html', msgs=msgs, user=user)

class HomeHandler(BaseHandler):
    def get(self):
        users = self.db.query('select * from users order by id desc limit 20')
        self.render('home.html', users=users)

class GetGlobalFeed(BaseHandler):
    def get(self):
        msgs = self.db.query('select * from msgs order by created desc limit 50')
        self.render('globalfeed.html', msgs=msgs)

class Follow(BaseHandler):
    def get(self, user):
        pass

class Unfollow(BaseHandler):
    def get(self, user):
        pass

class PostMessage(BaseHandler):
    def get(self):
        user = self.current_user
        self.render('post.html', user=user)

    def post(self):
        user = self.current_user
        if user:
            text = self.get_argument('text')
            self.db.execute('insert into msgs (user_id,username,text) values (%s,%s,%s)', 
                user.id, user.username, text)
        self.redirect('/')

def main():
    parse_command_line()
    server = httpserver.HTTPServer(Application())
    server.listen(options.port)
    IOLoop.instance().start()

if __name__ == '__main__':
    main()

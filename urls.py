from handlers.handlers import IndexHandler, HomeHandler, SockHandler

from tornado.web import url

url_patterns = (
    url(r'/', HomeHandler, name='home'),
    url(r'/([0-9]+)/demo', IndexHandler, name='index'),
    url(r'/([0-9]+)/websocket', SockHandler, name='websocket'),

)
from handlers.handlers import RoomHandler, HomeHandler, SockHandler

from tornado.web import url

url_patterns = (
    url(r'/', HomeHandler, name='home'),
    #url(r'/([0-9]+)/demo', IndexHandler, name='index'),
    url(r'/groups/([0-9]+)/rooms/([0-9]+)/', RoomHandler, name='room'),
    url(r'/websocket', SockHandler, name='websocket'),

)
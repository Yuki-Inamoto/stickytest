import tornado.web
import tornado.websocket
import json
import random


class RoomHandler(tornado.web.RequestHandler):

    def get(self, group_id, room_id):
        self.render('index.html', room_id=room_id)


class HomeHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        self.render('home.html')


class SockHandler(tornado.websocket.WebSocketHandler):
    from .rooms import Rooms
    from .cards import Cards
    rooms = Rooms()
    cards = Cards()

    def open(self, *args, **kwargs):
        print('WebSocket Opened')

    def on_message(self, message):
        print('WebSocket Received')
        print(json.loads(message))
        message = json.loads(message)
        if message['action'] == 'initializeMe':
            self.initClient()
        elif message['action'] == 'joinRoom':
            self.joinRoom(message)
        elif message['action'] == 'moveCard':
            self.move_card(message)
        elif message['action'] == 'createCard':
            self.create_card(message)
        elif message['action'] == 'editCard':
            self.edit_card(message)
        elif message['action'] == 'deleteCard':
            self.delete_card(message)
        elif message['action'] == 'changeTheme':
            self.change_theme(message)

    def on_close(self):
        print('WebSocket Closed')
        self.rooms.remove_client(self)

    def joinRoom(self, message):
        self.rooms.add_to_room(self, message['data'])
        self.write_message(json.dumps({'action': 'roomAccept', 'data': ''}))

    def roundRand(self, value):
        return random.randint(0, value)

    def initClient(self):
        room_id = self.rooms.get_room_id(self)
        self.write_message(json.dumps({'action': 'initCards', 'data': self.cards.get_all(room_id)}))
        self.write_message(json.dumps({'action': 'initColumns', 'data': ''}))
        self.write_message(json.dumps({'action': 'changeTheme', 'data': 'bigcards'}))
        self.write_message(json.dumps({'action': 'setBoardSize', 'data': ''}))
        self.write_message(json.dumps({'action': 'initialUsers', 'data': ''}))

    def move_card(self, message):
        message_out = {
            'action': message['action'],
            'data': {
                'id': message['data']['id'],
                'position': {
                    'left': message['data']['position']['left'],
                    'top': message['data']['position']['top'],
                }
            }
        }
        self.broadcast_to_room(self, message_out)
        room_id = self.rooms.get_room_id(self)
        self.cards.update_xy(room_id, card_id=message['data']['id'], x=message['data']['position']['left'], y=message['data']['position']['top'])

    def create_card(self, message):
        data = message['data']
        clean_data = {'text': data['text'], 'id': data['id'], 'x': data['x'], 'y': data['y'],
                      'rot': data['rot'], 'colour': data['colour'], 'sticker': None}
        message_out = {
            'action': 'createCard',
            'data': clean_data
        }
        self.broadcast_to_room(self, message_out)
        room_id = self.rooms.get_room_id(self)
        self.cards.add(room_id, clean_data)

    def edit_card(self, message):
        clean_data = {'value': message['data']['value'], 'id': message['data']['id']}
        message_out = {
            'action': 'editCard',
            'data': clean_data
        }
        self.broadcast_to_room(self, message_out)
        room_id = self.rooms.get_room_id(self)
        self.cards.update_text(room_id, card_id=message['data']['id'], text=message['data']['value'])

    def delete_card(self, message):
        clean_message = {
            'action': 'deleteCard',
            'data': {'id': message['data']['id']}
        }
        self.broadcast_to_room(self, clean_message)
        room_id = self.rooms.get_room_id(self)
        self.cards.delete(room_id, card_id=message['data']['id'])

    def change_theme(self, message):
        clean_message = {'data': message['data'], 'action': 'changeTheme'}
        self.broadcast_to_room(self, clean_message)

    def broadcast_to_room(self, client, message_out):
        room_id = self.rooms.get_room_id(client)
        for waiter in self.rooms.get_room_clients(room_id):
            if waiter == client:
                continue
            waiter.write_message(json.dumps(message_out))
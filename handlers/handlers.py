import tornado.web
import tornado.websocket
import json
import random


class IndexHandler(tornado.web.RequestHandler):

    def get(self, room_id):
        self.render('index.html', room_id=room_id)


class HomeHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        self.render('home.html')


class SockHandler(tornado.websocket.WebSocketHandler):
    from .rooms import Rooms
    waiters = set()
    rooms = Rooms()

    def open(self, *args, **kwargs):
        print('WebSocket Opened')
        SockHandler.waiters.add(self)
        #self.rooms.add_to_room(self, room_id=args[0])

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
        cards = []
        card = self.createCard('/demo', 'card1', 'Hello this is fun', self.roundRand(600), self.roundRand(300), random.random() * 10 - 5, 'yellow');
        cards.append(card)
        self.write_message(json.dumps({'action': 'initCards', 'data': cards}))
        self.write_message(json.dumps({'action': 'initColumns', 'data': ''}))
        self.write_message(json.dumps({'action': 'changeTheme', 'data': 'bigcards'}))
        self.write_message(json.dumps({'action': 'setBoardSize', 'data': ''}))
        self.write_message(json.dumps({'action': 'initialUsers', 'data': ''}))

    def createCard(self, room, id, text, x, y, rot, colour ):
        card = {'id': id, 'colour': colour, 'rot': rot,	'x': x,	'y': y,	'text': text, 'sticker': None}
        return card

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

    def create_card(self, message):
         data = message['data']
         clean_data = {'text': data['text'], 'id': data['id'], 'x': data['x'], 'y': data['y'],
                       'rot': data['rot'], 'colour': data['colour']}
         message_out = {
             'action': 'createCard',
             'data': clean_data
         }
         self.broadcast_to_room(self, message_out)

    def edit_card(self, message):
        clean_data = {'value': message['data']['value'], 'id': message['data']['id']}
        message_out = {
            'action': 'editCard',
            'data': clean_data
        }
        self.broadcast_to_room(self, message_out)

    def delete_card(self, message):
        clean_message = {
            'action': 'deleteCard',
            'data': {'id': message['data']['id']}
        }
        self.broadcast_to_room(self, clean_message)

    def change_theme(self, message):
        clean_message = {'data': message['data'], 'action': 'changeTheme'}
        self.broadcast_to_room(self, clean_message)

    def broadcast_to_room(self, client, message_out):
        room_id = self.rooms.get_room_id(client)
        print("room_id=")
        print(room_id)
        for waiter in self.rooms.get_room_clients(room_id):
            if waiter == client:
                continue
            waiter.write_message(json.dumps(message_out))
        """
        for waiter in self.waiters:
            if waiter == client:
                continue
            waiter.write_message(json.dumps(message_out))
        """
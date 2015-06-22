# -*- coding: utf-8 -*-
from collections import defaultdict

class Rooms(object):
    rooms = defaultdict(set)  # rooms[room_id].add(clientsock)
    clients = {}

    def add_to_room(self, client, room_id):
        self.rooms[room_id].add(client)
        self.clients[client] = room_id

    def get_room_clients(self, room_id):
        return self.rooms[room_id]

    def get_room_id(self, client):
        return self.clients[client]

"""
class Rooms(object):
    rooms = {}
    sid_rooms = {}
    room_users = {}

    def add_to_room(self, client, room, callback):
        if client.id not in self.sid_rooms.hasOwnProperty:
            self.sid_rooms[client.id] = set()
        self.sid_rooms[client.id].add(room)

        if room not in self.rooms:
            self.rooms[room] = set()
        self.rooms[room].add(client):

        if room not in self.room_users:
            self.room_users[room] = set()
        self.room_users[room].add(client.username)
        callback(self.rooms[room].array())

    def add_to_room_and_announce(self, client, room, msg):
        # Add user info to the current dramatis personae
         def f(clients):
             # Broadcast new-user notification
             for i in range(len(clients)):
                 if clients[i].id != client.id:
                     clients[i].write_message(msg)
        self.add_to_room(client, room, f)

"""
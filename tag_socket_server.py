# type: ignore
from flask import Flask, send_from_directory, request
from flask_socketio import SocketIO, Namespace, emit, send, leave_room, join_room, rooms
from data.namespaces import namespacesData
from classes.room import Room
import datetime
import os


class CustomNamespace(Namespace):
    def __init__(self, namespace):
        super().__init__(namespace=namespace)
        self.clients = set()
        self.room_clients = {}

    def on_connect(self):
        self.clients.add(request.sid)

    def on_disconnect(self):
        self.clients.remove(request.sid)
        self.client_leave_room()

    def on_joinRoom(self, room_title):
        self.client_leave_room()
        join_room(room_title)
        if room_title not in self.room_clients:
            self.room_clients[room_title] = set()
        self.room_clients[room_title].add(request.sid)
        emit(
            "roomNumUsersUpdate",
            {key: len(value) for key, value in self.room_clients.items()},
            broadcast=True,
        )
        room_chat_history = []
        for ns in namespacesData:
            if ns.endpoint == self.namespace:
                for room in ns.rooms:
                    if room.room_title == room_title:
                        room_chat_history = room.history
                        break
                break
        
        return {"numUsers": len(self.room_clients[room_title]),
                "history": room_chat_history}

    def on_newMessageToRoom(self, message_data):
        current_room = None
        for room_title in self.room_clients:
            if request.sid in self.room_clients[room_title]:
                current_room = room_title
                break
            
        current_room_obj = None
        for room_obj in namespacesData[message_data['namespaceId']].rooms:
            if room_obj.room_title == current_room:
                current_room_obj = room_obj
                break
        current_room_obj.add_message(message_data)
        print(current_room_obj.history)
        self.emit("newMessageToRoom", message_data, room=current_room)

    def client_leave_room(self):
        joined_rooms = rooms(request.sid, namespace=self.namespace)
        for entry in joined_rooms:
            if entry != request.sid:
                leave_room(entry, namespace=self.namespace)
                self.room_clients[entry].discard(request.sid)


app = Flask(__name__, static_folder="public", static_url_path="/public")
socketio = SocketIO(app)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists("public/" + path):
        return send_from_directory("public", path)
    else:
        return send_from_directory("public", "slack.html")


@app.route("/change-ns")
def change_ns():
    namespacesData[0].add_room(Room(0, "Deleted Articles", 0))
    # let everyone know in THIS namespace that there was a change
    socketio.emit(
        "nsChange", namespacesData[0].to_dict(), namespace=namespacesData[0].endpoint
    )
    return [ns.to_dict() for ns in namespacesData]


@socketio.on("connect")
def test_connect():
    print(f"{request.sid} connected")
    emit("welcome", "Welcome to python server")


@socketio.on("clientConnect")
def handle_client_connect():
    emit("nsList", [ns.to_dict() for ns in namespacesData])


@socketio.on("disconnect")
def test_disconnect():
    print("Client disconnected")


for ns in namespacesData:
    socketio.on_namespace(CustomNamespace(ns.endpoint))


if __name__ == "__main__":
    socketio.run(app, port=9000, debug=True)

# type: ignore
from flask import Flask, send_from_directory, request
from flask_socketio import SocketIO, Namespace, emit, send, leave_room, join_room
from data.namespaces import namespacesData
import json
import os

class CustomNamespace(Namespace):
   def on_connect(self):
      print(f'{request.sid} connected to {self.namespace} namespace')


app = Flask(__name__, static_folder='public', static_url_path='/public')
socketio = SocketIO(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists("public/" + path):
        return send_from_directory('public', path)
    else:
        return send_from_directory('public', 'slack.html')
    
@app.route('/change-ns')
def change_ns():
   return {'name': 'Wen', 'message': 'test'}
   

@socketio.on('connect')
def test_connect():
  print(f'{request.sid} connected')
  emit("welcome", "Welcome to python server")

@socketio.on('clientConnect')
def handle_client_connect():
  namespaces_json = json.dumps([ns.to_dict() for ns in namespacesData])
  emit("nsList", namespaces_json)
  

@socketio.on('disconnect')
def test_disconnect():
  print('Client disconnected')
  
for ns in namespacesData:
   socketio.on_namespace(CustomNamespace(ns.endpoint))


if __name__ == '__main__':
  socketio.run(app, port=9000, debug=True) 
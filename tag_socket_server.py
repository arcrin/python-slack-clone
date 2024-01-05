# type: ignore
from flask import Flask, send_from_directory, request
from flask_socketio import SocketIO, Namespace, emit, send, leave_room, join_room
from data.namespaces import namespaces
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

@socketio.on('connect')
def test_connect():
  print(f'{request.sid} connected')
  emit("welcome", "Welcome to python server")
  namespaces_json = json.dumps([ns.to_dict() for ns in namespaces])
  emit("nsList", namespaces_json)
  

@socketio.on('disconnect')
def test_disconnect():
  print('Client disconnected')


# @socketio.on('connect', namespace='/wiki')
# def handle_connect():
#    print(f'{request.sid} connected to wiki namespace')
  

# for ns in namespaces:
#    @socketio.on('connect', namespace=ns.endpoint)
#    def handle_connect():
#       print(f'{request.sid} connected to {ns.endpoint} namespace')

# @socketio.on('connect', namespace='/wiki')
# def handle_wiki_connect():
#    print(f'{request.sid} connected to wiki namespace')


# @socketio.on('connect', namespace='/mozilla')
# def handle_wiki_connect():
#    print(f'{request.sid} connected to mozilla namespace')


# @socketio.on('connect', namespace='/linux')
# def handle_wiki_connect():
#    print(f'{request.sid} connected to linux namespace')
  
for ns in namespaces:
   socketio.on_namespace(CustomNamespace(ns.endpoint))



if __name__ == '__main__':
  socketio.run(app, port=9000, debug=True) 
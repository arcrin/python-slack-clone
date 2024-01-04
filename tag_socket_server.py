import socketio
from starlette.responses import FileResponse
from fastapi import FastAPI
import os

sio = socketio.AsyncServer()
app = FastAPI()
app.mount('/ws', socketio.ASGIApp(sio))

@app.get('/{filename:path}')
async def read_file(filename: str):
  file_location = f"public/{filename}"
  if not os.path.isfile(file_location):
      return FileResponse("public/slack.html")
  return FileResponse(file_location)

@sio.event
def connect(sid, environ):
  print('Client connected: ', sid)

@sio.event
def disconnect(sid):
  print('Client disconnected: ', sid)

if __name__ == '__main__':
  import uvicorn
  uvicorn.run(app, host='localhost', port=9000)
# type: ignore
from .room import Room
from typing import List

class Namespace:
  def __init__(
      self,
      id: int, 
      name: str,
      image: str, 
      endpoint: str,
  ) -> None:
    self._id = id
    self._name = name
    self._image = image
    self._endpoint = endpoint
    self._rooms: List[Room] = []

  def add_room(self, room: Room):
    self._rooms.append(room)

  def to_dict(self):
    return {
      "id": self._id,
      "name": self._name,
      "image": self._image,
      "endpoint": self._endpoint,
      "rooms": [room.to_dict() for room in self._rooms],
    }
  
  @property
  def endpoint(self):
    return self._endpoint
  
  @property
  def rooms(self):
    return self._rooms
  
  @property
  def id(self):
    return self._id
  
  @property 
  def name(self):
    return self._name 
  
  @property
  def image(self):
    return self._image
  


from typing import Dict, Any, List

class Room:
  def __init__(
      self,
      room_id: int,
      room_title: str,
      namespace_id: int, 
      private_room: bool = False,
  ) -> None:
    self._room_id = room_id
    self._room_title = room_title
    self._namespace_id = namespace_id
    self._private_room = private_room
    self._history: List[Dict[str, Any]] = []

  def add_message(self, message: Dict[str, Any]):
    self._history.append(message)

  def clear_history(self):
    self._history = []

  @property
  def room_id(self):
    return self._room_id
  
  @property
  def room_title(self):
    return self._room_title
  
  @property
  def namespace_id(self):
    return self._namespace_id
  
  @property
  def private_room(self):
    return self._private_room
  
  @property
  def history(self):
    return self._history
  
  def to_dict(self):
    return {
      "roomId": self._room_id,
      "roomTitle": self._room_title,
      "namespaceId": self._namespace_id,
      "privateRoom": self._private_room,
    }
  
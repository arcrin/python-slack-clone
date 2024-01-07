from classes.namespace import Namespace
from classes.room import Room

wiki_ns = Namespace(
  0,
  "wiki",
  "https://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/103px-Wikipedia-logo-v2.svg.png",
  "/wiki"
)

moz_ns = Namespace(
  1,
  "mozilla",
  "https://www.mozilla.org/media/img/logos/firefox/logo-quantum.9c5e96634f92.png",
  "/mozilla"
)

linux_ns = Namespace(
  2,
  "linux",
  "https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Tux.svg/1200px-Tux.svg.png",
  "/linux"
)

wiki_ns.add_room(Room(0, "New Articles", 0))
wiki_ns.add_room(Room(1, "Editors", 0))
wiki_ns.add_room(Room(2, "Other", 0))

moz_ns.add_room(Room(0, "Firefox", 1))
moz_ns.add_room(Room(1, "SeaMonkey", 1))
moz_ns.add_room(Room(2, "SpiderMonkey", 1))
moz_ns.add_room(Room(3, "Rust", 1))

linux_ns.add_room(Room(0, "Debian", 2))
linux_ns.add_room(Room(1, "Red Hat", 2))
linux_ns.add_room(Room(2, "MacOs", 2))
linux_ns.add_room(Room(3, "Kernal Development", 2))

namespacesData = [wiki_ns, moz_ns, linux_ns]
const joinNs = (element, nsData) => {
  const nsEndpoint = element.getAttribute("ns");
  // console.log(nsEndpoint);

  const clickedNs = nsData.find((row) => row.endpoint === nsEndpoint);
  //  global variable, we can submit the new message to the right place
  selectedId = clickedNs.id;
  const rooms = clickedNs.rooms;

  let roomList = document.querySelector(".room-list");
  roomList.innerHTML = "";

  let firstRoom;

  // loop through each room, and add it to the DOM
  rooms.forEach((room, i) => {
    if (i == 0) {
      firstRoom = room.roomTitle;
    }
    roomList.innerHTML += `<li class="room" namespaceId=${room.namespaceId}>
    <span class="fa-solid fa-${room.privateRoom ? "lock" : "globe"}"></span>${
      room.roomTitle
    }
    </li>`;
  });

  // join first room
  joinRoom(firstRoom, clickedNs.id);

  const roomNodes = document.querySelectorAll(".room");
  Array.from(roomNodes).forEach((element) => {
    element.addEventListener("click", (event) => {
      // console.log("Someone clicked on ", event.target.innerText);
      const namespaceId = element.getAttribute("namespaceId");
      joinRoom(event.target.innerText, namespaceId);
    });
  });

  localStorage.setItem("lastNs", nsEndpoint);
};

const socket = io("http://localhost:9000");

const userName = prompt("What is your username?");

const nameSpaceSockets = [];
const listeners = {
  nsChange: [],
  roomNumUsersUpdate: [],
  newMessageToRoom: [],
};

let selectedNsId = 0;

document.querySelector("#message-form").addEventListener("submit", (e) => {
  e.preventDefault();
  const newMessage = document.querySelector("#user-message").value;
  // console.log(newMessage, selectedNsId);
  nameSpaceSockets[selectedNsId].emit("newMessageToRoom", {
    newMessage,
    date: Date.now(),
    avatar: "https://via.placeholder.com/30",
    userName,
    namespaceId: selectedNsId,
  });
  document.querySelector("#user-message").value = "";
});

const addListener = (nsId) => {
  if (!listeners.nsChange[nsId]) {
    nameSpaceSockets[nsId].on("nsChange", (data) => {
      // console.log("Namespace changed!");
      // console.log(data);
    });
    listeners.nsChange[nsId] = true;
  }
  if (!listeners.roomNumUsersUpdate[nsId]) {
    nameSpaceSockets[nsId].on("roomNumUsersUpdate", (data) => {
      // console.log("Room number of users changed!");
      // console.log(data);
      for (let key in data) {
        roomTitle = document.querySelector(".curr-room-text").innerHTML;
        if (key === roomTitle) {
          document.querySelector(
            ".curr-room-num-users"
          ).innerHTML = `${data[key]}<span class="fa-solid fa-user"></span>`;
        }
      }
    });
    listeners.roomNumUsersUpdate[nsId] = true;
  }
  if (!listeners.newMessageToRoom[nsId]) {
    nameSpaceSockets[nsId].on("newMessageToRoom", (messageData) => {
      console.log(messageData);
      document.querySelector("#messages").innerHTML += buildMessageHtml(messageData);
    });
    listeners.newMessageToRoom[nsId] = true;
  }
};

socket.on("welcome", (data) => {
  // console.log(data);
  socket.emit("clientConnect");
});

// listen to the nsList event, which gives the client the list of all the namespaces
socket.on("nsList", (nsData) => {
  // console.log(nsData);
  const nameSpaceDiv = document.querySelector(".namespaces");
  nameSpaceDiv.innerHTML = "";
  nsData.forEach((ns) => {
    // update the HTML with each ns
    const nameSpaceDiv = document.querySelector(".namespaces");
    nameSpaceDiv.innerHTML += `<div class="namespace" ns=${ns.endpoint}><img src="${ns.image}" /></div>`;

    if (!nameSpaceSockets[ns.id]) {
      // only join this namespace with io() if we haven't already joined
      nameSpaceSockets[ns.id] = io(`http://localhost:9000${ns.endpoint}`);
    }
    addListener(ns.id);
  });
  Array.from(document.getElementsByClassName("namespace")).forEach(
    (element) => {
      // // console.log(element);
      element.addEventListener("click", (e) => {
        joinNs(element, nsData);
      });
    }
  );
  joinNs(document.getElementsByClassName("namespace")[0], nsData);
});
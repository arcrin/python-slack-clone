const joinRoom = async (roomTitle, namespaceId) => {
  // console.log(roomTitle, namespaceId);
  const ackResponse = await nameSpaceSockets[namespaceId].emitWithAck("joinRoom", roomTitle);
  // console.log(ackResponse.numUsers);
  document.querySelector(
    ".curr-room-num-users"
  ).innerHTML = `${ackResponse.numUsers}<span class="fa-solid fa-user"></span>`;
  document.querySelector(".curr-room-text").innerHTML = roomTitle;
  document.querySelector("#messages").innerHTML = "";
  ackResponse.history.forEach((message) => {
    document.querySelector("#messages").innerHTML += buildMessageHtml(message);
  });
};

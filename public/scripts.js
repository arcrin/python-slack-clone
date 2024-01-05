const socket = io("http://localhost:9000");
const wikiSocket = io("http://localhost:9000/wiki");
const mozSocket = io("http://localhost:9000/mozilla");
const linuxSocket = io("http://localhost:9000/linux");

// socket.on("connect", () => {

// });

socket.on("welcome", (data) => {
  // console.log(data);
});

// listen to the nsList event, which gives the client the list of all the namespaces
socket.on("nsList", (nsDataJson) => {
  let nsData = JSON.parse(nsDataJson);
  // console.log(nsData);
  nsData.forEach((ns) => {
    // update the HTML with each ns
    const nameSpaceDiv = document.querySelector(".namespaces");
    nameSpaceDiv.innerHTML += `<div class="namespace" ns=${ns.endpoint}><img src="${ns.image}" /></div>`;
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

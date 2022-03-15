// change the web socket address to hosted.
const ws = new WebSocket(`ws://localhost:5050/xumm`);

/** called when connection opens, sends join info to server. */

ws.onopen = function (evt) {
  console.log("open", evt);
  // data :
  ws.send(JSON.stringify(data));
};

/** called when msg received from server; displays it. */

ws.onmessage = function (evt) {
  console.log("message", evt);

  let msg = JSON.parse(evt.data);
  let item;

  if (msg.type === "note") {
    item = $(`<li><i>${msg.text}</i></li>`);
  } else if (msg.type === "chat") {
    item = $(`<li><b>${msg.name}: </b>${msg.text}</li>`);
  } else {
    return console.error(`bad message: ${msg}`);
  }
};

/** called on error; logs it. */

ws.onerror = function (evt) {
  console.error(`err ${evt}`);
};

/** called on connection-closed; logs it. */

ws.onclose = function (evt) {
  console.log("close", evt);
};

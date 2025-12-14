const URL = "ws://localhost:8765/ws";

export default function createWsClient(onMessage) {
  const ws = new WebSocket(URL);

  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    onMessage(msg);
  };

  return {
    send: (msg) => {
      ws.send(JSON.stringify(msg));
    },
    close: () => {
      ws.close();
    },
  }
}
export const signatureResult = async (websocketUrl) => {
  return new Promise((resolve, _reject) => {
    const ws = new WebSocket(websocketUrl);
    ws.onmessage = (msg) => {
      const payload = JSON.parse(msg.data);
      if (payload.signed) {
        ws.close();
        resolve(payload);
      }
    };
  });
};

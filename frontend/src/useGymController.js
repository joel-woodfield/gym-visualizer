import { useRef, useState, useEffect } from "react";
import createWsClient from "./wsClient.js";


function onMessage(msg, setStepData) {
  if (msg.type === "step" || msg.type === "reset") {
    setStepData(msg.data); 
  }
}

function onOpen(setWsConnected) {
  setWsConnected(true);
}

function onClose(setWsConnected) {
  setWsConnected(false);
}

function onError(error, setWsConnected) {
  console.error("WebSocket error:", error);
  setWsConnected(false);
}

export default function useGymController() {
  const wsRef = useRef(null);
  const [stepData, setStepData] = useState(null);
  const [wsConnected, setWsConnected] = useState(false);

  useEffect(() => {
    wsRef.current = createWsClient(
      (msg) => onMessage(msg, setStepData),
      () => onOpen(setWsConnected),
      () => onClose(setWsConnected),
      (error) => onError(error, setWsConnected),
    );
    return () => {
      wsRef.current.close();
    };
  }, []);

  return {
    wsConnected,
    stepData,
    step: () => wsRef.current.send({ type: "step" }),
    play: () => wsRef.current.send({ type: "play" }),
    pause: () => wsRef.current.send({ type: "pause" }),
    reset: () => wsRef.current.send({ type: "reset" }),
  };
}
import { useRef, useState, useEffect } from "react";
import createWsClient from "./wsClient.js";


export default function useGymController() {
  const wsRef = useRef(null);
  const [stepData, setStepData] = useState(null);
  const [wsConnected, setWsConnected] = useState(false);

  function onMessage(msg) {
    if (msg.type === "step" || msg.type === "reset") {
      setStepData(msg.data); 
    } else if (msg.type === "error") {
      alert(`Error from server:\n${msg.data}`);
    }
  }

  function onOpen() {
    setWsConnected(true);
  }

  function onClose() {
    setWsConnected(false);
  }

  function onError(error) {
    console.error("WebSocket error:", error);
    setWsConnected(false);
  }

  useEffect(() => {
    wsRef.current = createWsClient(
      onMessage,
      onOpen,
      onClose,
      onError,
    );
    return () => {
      wsRef.current.close();
    };
  }, []);

  return {
    wsConnected,
    stepData,
    step: () => wsRef.current.send({ type: "step" }),
    play: (fps) => wsRef.current.send({ type: "play", fps: fps }),
    pause: () => wsRef.current.send({ type: "pause" }),
    reset: () => wsRef.current.send({ type: "reset" }),
    submitPolicy: (policyProgram) => wsRef.current.send({ type: "submitPolicy", data: policyProgram }),
    submitEnv: (envId) => wsRef.current.send({ type: "submitEnv", data: envId }),
  };
}
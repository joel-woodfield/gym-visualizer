import { useRef, useState, useEffect } from "react";
import createWsClient from "./wsClient.js";

export default function useGymController() {
  const wsRef = useRef(null);
  const [stepData, setStepData] = useState(null);

  useEffect(() => {
    wsRef.current = createWsClient((msg) => {
      if (msg.type === "step" || msg.type === "reset") {
        setStepData(msg.data); 
      }
    });
    return () => {
      wsRef.current.close();
    };
  }, []);

  return {
    stepData,
    step: () => wsRef.current.send({ type: "step" }),
    reset: () => wsRef.current.send({ type: "reset" }),
  };
}
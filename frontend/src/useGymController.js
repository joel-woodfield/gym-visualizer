import { useRef, useState, useEffect } from "react";
import createWsClient from "./wsClient.js";

export default function useGymController() {
  const wsRef = useRef(null);
  const [stepData, setStepData] = useState(null);

  useEffect(() => {
    wsRef.current = createWsClient((msg) => {
      if (msg.type === "step") {
        setStepData(msg.data); 
      }
    });
    return () => {
      wsRef.current.close();
    };
  }, []);

  return {
    stepData,
    step: (data) => wsRef.current.send({ type: "step", data }),
  };
}
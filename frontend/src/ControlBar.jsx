import { useState } from "react";
import ControlButton from "./ui/ControlButton";
import InputField from "./ui/InputField";


export default function ControlBar({ onStep, onPlay, onPause, onReset, onEnvSubmit }) {
  const [envId, setEnvId] = useState("CartPole-v1")
  const [fps, setFps] = useState("60");
  
  function handleEnvSubmit() {
    onEnvSubmit(envId);
  }

  return (
    <div className="flex justify-between p-4 border-t-2 border-gray-200 align-center">
      <div className="flex gap-4 text-2xl">
        <ControlButton onClick={() => onPlay(fps)} icon={"▶"} />
        <ControlButton onClick={onPause} icon={"⏸"} />
        <ControlButton onClick={onReset} icon={"■"} />
        <ControlButton onClick={onStep} icon={"»"} />
        <InputField label="fps: " value={fps} onChange={setFps} />
      </div>

      <InputField
        label="env-id: "
        value={envId}
        onChange={setEnvId}
        onSubmit={handleEnvSubmit}
        buttonLabel="Submit"
      />
    </div>
  );
}

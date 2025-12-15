import { useState } from "react";


export default function ControlBar({ onStep, onPlay, onPause, onReset, onEnvSubmit }) {
  const [envId, setEnvId] = useState("CartPole-v1")

  function handleSubmit(e) {
    e.preventDefault();
    onEnvSubmit?.(envId);
  }

  return (
    <div className="control-bar">
      <form onSubmit={handleSubmit}>
        <label>env-id: </label>
        <input 
          type="text" 
          value={envId}
          onChange={(e) => setEnvId(e.target.value)}
        />
        <button type="submit">Submit</button>
      </form>
      <button onClick={onStep}>Step</button>
      <button onClick={onPlay}>Play</button>
      <button onClick={onPause}>Pause</button>
      <button onClick={onReset}>Reset</button>
    </div>
  );
}

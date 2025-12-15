import { useState } from "react";


export default function ControlBar({ onStep, onPlay, onPause, onReset, onEnvSubmit }) {
  const [envId, setEnvId] = useState("CartPole-v1")

  function handleSubmit(e) {
    e.preventDefault();
    onEnvSubmit?.(envId);
  }

  return (
    <div className="control-bar">
      <div className="playback-controls">
        <button onClick={onPlay} className="control-button">▶</button>
        <button onClick={onPause} className="control-button">⏸</button>
        <button onClick={onReset} className="control-button">■</button>
        <button onClick={onStep} className="control-button">»</button>
      </div>
      <form onSubmit={handleSubmit}>
        <label>env-id: </label>
        <input 
          type="text" 
          value={envId}
          onChange={(e) => setEnvId(e.target.value)}
        />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

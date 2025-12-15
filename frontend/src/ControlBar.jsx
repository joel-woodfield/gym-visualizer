export default function ControlBar({ onStep, onPlay, onPause, onReset }) {
  return (
    <div className="control-bar">
      <button onClick={onStep}>Step</button>
      <button onClick={onPlay}>Play</button>
      <button onClick={onPause}>Pause</button>
      <button onClick={onReset}>Reset</button>
    </div>
  );
}

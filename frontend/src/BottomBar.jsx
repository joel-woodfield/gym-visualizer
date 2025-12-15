export default function BottomBar({ onStep, onPlay, onPause, onReset }) {
  return (
    <div>
      <button onClick={onStep}>Step</button>
      <button onClick={onPlay}>Play</button>
      <button onClick={onPause}>Pause</button>
      <button onClick={onReset}>Reset</button>
    </div>
  );
}

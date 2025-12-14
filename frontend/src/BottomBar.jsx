export default function BottomBar({ onStep, onRun, onPause, onReset }) {
  return (
    <div>
      <button onClick={onStep}>Step</button>
      <button onClick={onRun}>Run</button>
      <button onClick={onPause}>Pause</button>
      <button onClick={onReset}>Reset</button>
    </div>
  );
}

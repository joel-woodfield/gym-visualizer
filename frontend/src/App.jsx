import StatusBar from "./StatusBar.jsx";
import ControlBar from "./ControlBar.jsx";
import MainLayout from "./MainLayout.jsx";
import useGymController from "./useGymController.js";


export default function App() {
  const { wsConnected, stepData, step, play, pause, reset, submitPolicy, submitEnv } = useGymController();

  return (
    <div className="h-dvh grid grid-rows-[auto_1fr_auto]">
      <StatusBar stepData={stepData} connected={wsConnected} />
      <MainLayout stepData={stepData} onCodeSubmit={submitPolicy} />
      <ControlBar
        onStep={step}
        onPlay={play}
        onPause={pause}
        onReset={reset}
        onEnvSubmit={submitEnv}
      />
    </div>
  );
}

import TopBar from "./TopBar.jsx";
import BottomBar from "./BottomBar.jsx";
import MainLayout from "./MainLayout.jsx";
import useGymController from "./useGymController.js";
import "./App.css";


export default function App() {
  const { wsConnected, stepData, step, play, pause, reset } = useGymController();

  return (
    <>
      <h1>Gymnasium Visualizer</h1>
      <h4>Status: {wsConnected ? "Connected" : "Disconnected" }</h4>
      <TopBar stepData={stepData} />
      <MainLayout stepData={stepData} />
      <BottomBar
        onStep={step}
        onPlay={play}
        onPause={pause}
        onReset={reset}
      />
    </>
  );
}

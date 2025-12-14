import TopBar from "./TopBar.jsx";
import BottomBar from "./BottomBar.jsx";
import MainLayout from "./MainLayout.jsx";
import useGymController from "./useGymController.js";
import "./App.css";


export default function App() {
  const { stepData, step } = useGymController();

  return (
    <>
      <h1>Gymnasium Visualizer</h1>
      <TopBar stepData={stepData} />
      <MainLayout stepData={stepData} />
      <BottomBar
        onStep={() => step(stepData)}
      />
    </>
  );
}

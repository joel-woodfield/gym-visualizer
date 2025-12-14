import FrameViewer from "./FrameViewer.jsx"
import ObsViewer from "./ObsViewer.jsx"
import Editor from "./Editor.jsx"

export default function MainLayout({ stepData }) {
  return (
    <div>
      <FrameViewer frame={`data:image/png;base64,${stepData?.frame}`}/>
      <ObsViewer observation={stepData?.observation} />
      <Editor />
    </div>
  );
}

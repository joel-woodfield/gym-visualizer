import FrameViewer from "./FrameViewer.jsx"
import ObsViewer from "./ObsViewer.jsx"
import CodeEditor from "./CodeEditor.jsx"

export default function MainLayout({ stepData, onCodeSubmit }) {
  return (
    <div className="main-layout">
      <FrameViewer frame={stepData?.frame ? `data:image/png;base64,${stepData?.frame}` : null} />
      <ObsViewer obs={stepData?.observation} />
      <CodeEditor onCodeSubmit={onCodeSubmit} />
    </div>
  );
}

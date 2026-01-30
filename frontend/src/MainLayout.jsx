import FrameViewer from "./FrameViewer.jsx"
import ObsViewer from "./ObsViewer.jsx"
import CodeEditor from "./CodeEditor.jsx"

export default function MainLayout({ stepData, onCodeSubmit }) {
  return (
    <div className="min-h-0 grid grid-cols-[1fr_auto_1fr] gap-10">
      <FrameViewer frame={stepData?.frame ? `data:image/png;base64,${stepData?.frame}` : null} />
      <ObsViewer obs={stepData?.observation} />
      <CodeEditor onCodeSubmit={onCodeSubmit} />
    </div>
  );
}

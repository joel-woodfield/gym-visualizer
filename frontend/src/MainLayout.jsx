import FrameViewer from "./FrameViewer.jsx"
import ObsViewer from "./ObsViewer.jsx"
import Editor from "./Editor.jsx"

export default function MainLayout() {
  return (
    <div>
      <FrameViewer />
      <ObsViewer />
      <Editor />
    </div>
  );
}

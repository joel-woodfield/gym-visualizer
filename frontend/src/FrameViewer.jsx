export default function FrameViewer({ frame }) {
  return (
    <div className="frame-viewer">
      <img 
        src={frame}
        alt="Frame" 
      />
    </div>
  )
}
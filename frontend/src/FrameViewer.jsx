export default function FrameViewer({ frame }) {
  return (
    <div className="min-w-0 min-h-0 border-r-2 border-gray-200">
      <img 
        src={frame}
        alt="Frame" 
        className="h-full w-full object-contain"
      />
    </div>
  )
}
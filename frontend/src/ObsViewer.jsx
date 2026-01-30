export default function ObsViewer({ obs }) {
  return (
    <div className="min-h-0 overflow-auto">
      <div className="text-sm font-mono">
        {obs?.map((value, index) => (
          <div key={index} className="obs-item">
            {index} -> {value}
          </div>
        ))}
      </div>
   </div>
  )
}
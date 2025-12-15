export default function ObsViewer({ obs }) {
  return (
    <div className="obs-viewer">
      {obs?.map((value, index) => (
        <div key={index}>
          {index}: {value}
        </div>
      ))}
    </div>
  )
}
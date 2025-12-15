export default function ObsViewer({ obs }) {
  return (
    <div className="obs-viewer">
      <h3>Observations</h3>

      {obs?.map((value, index) => (
        <div key={index}>
          {index}: {value}
        </div>
      ))}
    </div>
  )
}
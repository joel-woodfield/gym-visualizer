export default function ObsViewer({ obs }) {
  return (
    <div className="obs-viewer">
      <h3>Observations</h3>

      <div className="obs-list">
        {obs?.map((value, index) => (
          <div key={index} className="obs-item">
            {index}: {value}
          </div>
        ))}
      </div>
   </div>
  )
}
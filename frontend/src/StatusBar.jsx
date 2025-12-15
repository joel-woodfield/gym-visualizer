export default function StatusBar({ stepData, connected }) {
  return (
    <div className="status-bar">
      <h4>Status: {connected ? "Connected" : "Disconnected" }</h4>
      <p>Current Step: {stepData?.stepIdx}</p>
      <p>Current Episode Return: {stepData?.episodeReturn}</p>
      <p>Done: {stepData?.done ? "Yes" : "No"}</p>
    </div>
  )
}


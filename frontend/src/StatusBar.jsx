export default function StatusBar({ stepData, connected }) {
  return (
    <div className="status-bar">
      <h4>Status: {connected ? "Connected" : "Disconnected" }</h4>
      <h4>Current Step: {stepData?.stepIdx}</h4>
      <h4>Current Episode Return: {stepData?.episodeReturn}</h4>
      <h4>Previous Action: {stepData?.action}</h4>
      <h4>Done: {stepData?.done ? "Yes" : "No"}</h4>
    </div>
  )
}


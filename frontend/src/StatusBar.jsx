export default function StatusBar({ stepData, connected }) {
  return (
    <div className="grid grid-cols-5 border-gray-200 border-b-2 p-2 justify-items-center">
      <h4>Python: {connected ? "Connected" : "Disconnected" }</h4>
      <h4>Current Step: {stepData?.stepIdx}</h4>
      <h4>Current Episode Return: {stepData?.episodeReturn}</h4>
      <h4>Previous Action: {stepData?.action}</h4>
      <h4>Done: {stepData?.done ? "Yes" : "No"}</h4>
    </div>
  )
}


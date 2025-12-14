export default function TopBar( {stepData} ) {
  return (
    <div>
      <p>Current Step: {stepData?.stepIdx}</p>
      <p>Current Episode Return: {stepData?.episodeReturn}</p>
      <p>Done: {stepData?.done ? "Yes" : "No"}</p>
    </div>
  )
}


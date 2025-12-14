export default function TopBar( {stepData} ) {
  return (
    <div>
      <p>Current Step: {stepData?.stepIdx}</p>
      <p>Current Episode Return: {stepData?.episodeReturn}</p>
      
      <p>Current Episode: {stepData?.episodeIdx}</p>
      <p>Average Episode Return: {stepData?.avgEpisodeReturn}</p>
    </div>
  )
}


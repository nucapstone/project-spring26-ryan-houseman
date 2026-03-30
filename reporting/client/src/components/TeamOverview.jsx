export default function PlayerDetail({SelectedDate, changeView, data}) {

  // const player = data.find(item => item.session_date === SelectedDate && item.player_id === player_id);

  return (
    <div>
      <h2>Team Overview</h2>
      <button onClick={() => changeView("player_overview")}>Return to Player Overview</button>
      {/* <p><strong>Player ID:</strong> {player.player_id}</p>
      <p><strong>Player Name:</strong> {player.player_name}</p>
      <p><strong>Likelihood of Injury (SelectedDate):</strong> {player.injury_predicted_prob}</p>
      <p><strong>Predicted Injury Flag Rate (Previous Week):</strong> {player.predicted_injury_flag_rate}</p> */}
    </div>
  );
}
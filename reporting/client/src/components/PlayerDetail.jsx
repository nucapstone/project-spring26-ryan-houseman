export default function PlayerDetail({SelectedDate, changeView, player_id, data}) {

  const player = data.find(item => item.session_date === SelectedDate && item.player_id === player_id);
  const toPercent = (val, decimals = 1) => `${(val * 100).toFixed(decimals)}%`;

  return (
    <div>
      <h2>Player Detail</h2>
      {/* <button onClick={() => changeView("player_overview")}>Return to Player Overview</button> */}
      <p><strong>Player ID:</strong> {player.player_id}</p>
      <p><strong>Player Name:</strong> {player.player_name}</p>
      <p><strong>Likelihood of Injury (SelectedDate):</strong> {toPercent(player.injury_predicted_prob)}</p>
      <p><strong>Predicted Injury Flag Rate (Previous Week):</strong> {toPercent(player.predicted_injury_flag_rate)}</p>
    </div>
  );
}
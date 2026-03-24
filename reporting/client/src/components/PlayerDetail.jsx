import { useEffect, useState } from "react";

export default function PlayerDetail({SelectedDate, changeView, player_id}) {
  const [player, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
      const facility_url = `http://127.0.0.1:5000/api/player_detail/${encodeURIComponent(player_id)}/${encodeURIComponent(SelectedDate)}`;
      fetch(facility_url)
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json();
        })
        .then((json) => {
          setData(json);
          setLoading(false);
        })
        .catch((err) => {
          setError(err.message);
          setLoading(false);
        });
    }, [player_id,SelectedDate]);
  
    if (loading) return <p>Loading data...</p>;
    if (error) return <p style={{ color: "red" }}>Error: {error}</p>;


  return (
    <div>
      <h2>Player Detail</h2>
      <button onClick={() => changeView("player_overview")}>Return to Player Overview</button>
      <p><strong>Player ID:</strong> {player.player_id}</p>
      <p><strong>Player Name:</strong> {player.player_name}</p>
      <p><strong>Likelihood of Injury (SelectedDate):</strong> {player.injury_predicted_prob}</p>
      <p><strong>Predicted Injury Flag Rate (Previous Week):</strong> {player.predicted_injury_flag_rate}</p>
    </div>
  );
}
import { useState } from "react";

export default function PlayerOverview({SelectedDate, changeView,selectedPlayer, data}) {
  const [player_id, setPlayer] = useState("");
  const filtered_data = data.filter(item => item.session_date === SelectedDate).sort((a, b) => b.predicted_injury_flag_rate_7d - a.predicted_injury_flag_rate_7d);
  const toPercent = (val, decimals = 1) => `${(val * 100).toFixed(decimals)}%`;

  const getRowStyle = (predicted_injury_flag_rate) => {
    if (predicted_injury_flag_rate < 0.01) {
      return { backgroundColor: "#E9FCF8", color:"#2c3e50"}; 
    } else if (predicted_injury_flag_rate < 0.25) {
      return { backgroundColor: "#98F1DF", color:"#2c3e50"};
    } else if (predicted_injury_flag_rate < 0.75) {
      return { backgroundColor: "#1ABC9C", color:"#2c3e50"};
    } else {
      return { backgroundColor: "#0E6755", color:"whitesmoke"}; 
    }
  };
  return (
    <div style={{width: "100%"}}>
      <h3>BMS Player Overview - {SelectedDate} </h3>
      <table border="1" cellPadding="8" style={{ borderCollapse: "collapse", cursor: "pointer", width: "100%", tableLayout: "fixed"}}>
        <thead>
          <tr>
            <th className="th-cell">Player ID</th>
            <th className="th-cell">Player</th>
            <th className="th-cell">Likelihood of Overuse Injury</th>
            <th className="th-cell">Predicted Injury Flag Rate</th>
            <th className="th-cell">Date</th>
          </tr>
        </thead>
        <tbody>
          {filtered_data.map((dp) => (
            <tr key={dp.player_id} style={getRowStyle(dp.predicted_injury_flag_rate_7d)} onClick={() => {
              changeView("player_detail");
              setPlayer(dp.player_id);
              selectedPlayer(dp.player_id);
              }}>
              <td className="td-cell">{dp.player_id}</td>
              <td className="td-cell">{dp.player_name}</td>
              <td className="td-cell">{toPercent(dp.injury_predicted_prob)}</td>
              <td className="td-cell">{toPercent(dp.predicted_injury_flag_rate_7d)}</td>
              <td className="td-cell">{dp.session_date}</td>
            </tr>
          ))}
        </tbody>

      </table>
      
    </div>
  );
} 


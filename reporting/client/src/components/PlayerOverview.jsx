import { useState } from "react";

export default function PlayerOverview({SelectedDate, changeView,selectedPlayer, data}) {
  const [player_id, setPlayer] = useState("");
  const filtered_data = data.filter(item => item.session_date === SelectedDate).sort((a, b) => b.predicted_injury_flag_rate_window - a.predicted_injury_flag_rate_window);
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

  const kpis = [
    { label: "Total Players", value: 128 },
    { label: "Injury Rate",   value: "12.5%" },
    { label: "Avg Sessions",  value: 4.2 },
    { label: "AP Score",      value: 0.87 },
  ];

  return (
    <div style={{width: "100%"}}>
      {/* <h3>BMS Player Overview - {SelectedDate} </h3> */}
      <div style={{display: "flex", gap: "1rem", marginBottom: "1.5rem", marginTop: "1.5rem"}}>
        {kpis.map(({ label, value }) => (
          <div key={label} style={{ flex: 1, padding: "1rem", border: "3px solid #e2e8f0", borderRadius: "8px" }}>
              <p>{label}</p>
              <h2>{value}</h2>
            </div>
        ))}
      </div>
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
            <tr key={dp.player_id} style={getRowStyle(dp.predicted_injury_flag_rate_window)} onClick={() => {
              changeView("player_detail");
              setPlayer(dp.player_id);
              selectedPlayer(dp.player_id);
              }}>
              <td className="td-cell">{dp.player_id}</td>
              <td className="td-cell">{dp.player_name}</td>
              <td className="td-cell">{toPercent(dp.injury_predicted_prob)}</td>
              <td className="td-cell">{toPercent(dp.predicted_injury_flag_rate_window)}</td>
              <td className="td-cell">{dp.session_date}</td>
            </tr>
          ))}
        </tbody>

      </table>
      
    </div>
  );
} 






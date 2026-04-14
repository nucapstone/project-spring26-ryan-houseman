import { useState } from "react";

export default function PlayerOverview({SelectedDate, changeView,selectedPlayer, data}) {
  const [player_id, setPlayer] = useState("");
  const filtered_data = data.filter(item => item.session_date === SelectedDate).sort((a, b) => a.player_freshness - b.player_freshness);
  const toPercent = (val, decimals = 1) => `${(val * 100).toFixed(decimals)}%`;

  const prediction_window = Math.max(...filtered_data.map(item => item.prediction_window));
  const threshold = Math.max(...filtered_data.map(item => item.prediction_threshold));

  const high_risk = filtered_data.filter(item => item.player_freshness <= 200).length;
  const medium_risk = filtered_data.filter(item => item.player_freshness > 200 && item.player_freshness <= 500).length;
  const mean_llk = filtered_data.reduce((sum, item) => sum + item.injury_predicted_prob, 0) / filtered_data.length;
  const mean_freshness = filtered_data.reduce((sum, item) => sum + item.player_freshness, 0) / filtered_data.length;

  const KPIstyle = (label, value, threshold) => {
    if (label === "Average Injury Likelihood" && value > threshold) {
      return { flex: 1, padding: "1rem", border: "3px solid #f87171", borderRadius: "8px", textAlign:"center", backgroundColor: "rgba(248, 113, 113, 0.15)"}; 
    } else if (label === "# of High Risk Players"  && value >= 1) {
      return { flex: 1, padding: "1rem", border: "3px solid #f87171", borderRadius: "8px", textAlign:"center", backgroundColor: "rgba(248, 113, 113, 0.15)"}; 
    } else if (label === "# of Medium Risk Players"  && value >= 1) {
      return { flex: 1, padding: "1rem", border: "3px solid #f87171", borderRadius: "8px", textAlign:"center", backgroundColor: "rgba(248, 113, 113, 0.15)"}; 
    } else {
      return { flex: 1, padding: "1rem", border: "3px solid #e2e8f0", borderRadius: "8px", textAlign:"center"}; 
    }
  };

  const getRowStyle = (player_freshness) => {
    if (player_freshness > 800) {
      return { backgroundColor: "#E9FCF8", color:"#2c3e50"}; 
    } else if (player_freshness > 500) {
      return { backgroundColor: "#98F1DF", color:"#2c3e50"};
    } else if (player_freshness > 200) {
      return { backgroundColor: "#1ABC9C", color:"whitesmoke"};
    } else {
      return { backgroundColor: "#0E6755", color:"whitesmoke"}; 
    }
  };

  const kpis = [
    { label: "Average Injury Likelihood",      value: toPercent(mean_llk), raw_value: mean_llk },
    { label: "Average Player Freshness",      value: (mean_freshness).toFixed(2), raw_value: mean_freshness },
    { label: "# of High Risk Players",   value: high_risk, raw_value: high_risk },
    { label: "# of Medium Risk Players",  value: medium_risk, raw_value: medium_risk }
  ];

  return (
    <div style={{width: "100%", textAlign:"center"}}>
      <div style={{ display: "flex", gap: "1rem", marginBottom: "1.5rem", marginTop: "1.5rem", 
                  alignItems: "center", marginRight:"1.5rem", minHeight:"100px"}}>
        {kpis.map(({ label, value, raw_value }) => (
          <div key={label} style={KPIstyle(label,raw_value,threshold)}>
              <p>{label}</p>
              <h2>{value}</h2>
            </div>
        ))}
      </div>
      <table border="1" cellPadding="8" style={{ borderCollapse: "collapse", cursor: "pointer", width: "100%", tableLayout: "fixed", textAlign:"center"}}>
        <thead>
          <tr>
            <th className="th-cell">Player</th>
            <th className="th-cell">Predicted Likelihood of Overuse Injury</th>
            <th className="th-cell">Sessions Flagged in Previous {prediction_window} Days</th>
            <th className="th-cell">Player Freshness</th>
          </tr>
        </thead>
        <tbody>
          {filtered_data.map((dp) => (
            <tr key={dp.player_id} style={getRowStyle(dp.player_freshness)} onClick={() => {
              changeView("player_detail");
              setPlayer(dp.player_id);
              selectedPlayer(dp.player_id);
              }}>
              <td className="td-cell">{dp.player_name}</td>
              <td className="td-cell">{toPercent(dp.injury_predicted_prob)}</td>
              <td className="td-cell">{`${toPercent(dp.predicted_injury_flag_rate_window)} - (${dp.injury_flag_cnt_window}/${dp.session_cnt_window}) sessions`}</td>
              <td className="td-cell">{dp.player_freshness}</td>
            </tr>
          ))}
        </tbody>

      </table>
      
    </div>
  );
} 






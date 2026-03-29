import { useState } from "react";

export default function HospitalSearch({SelectedDate, changeView,selectedPlayer, data}) {
  const [player_id, setPlayer] = useState("");

  const filtered_data = data.filter(item => item.session_date === SelectedDate).sort((a, b) => b.predicted_injury_flag_rate - a.predicted_injury_flag_rate);


  const getRowStyle = (predicted_injury_flag_rate) => {
    if (predicted_injury_flag_rate < 0.01) {
      return { backgroundColor: "#FCE8F9", color:"#000000"}; 
    } else if (predicted_injury_flag_rate < 0.25) {
      return { backgroundColor: "#EF6CD7", color:"#000000"};
    } else if (predicted_injury_flag_rate < 0.75) {
      return { backgroundColor: "#E61AC0", color:"#000000"};
    } else {
      return { backgroundColor: "#850F6F", color:"#F5F5F5"}; 
    }
  };
  return (
    <div>
      <h3>BMS Player Overview - {SelectedDate} </h3>
      <table border="1" cellPadding="8" style={{ borderCollapse: "collapse", cursor: "pointer" }}>
        <thead>
          <tr>
            <th>Player ID</th>
            <th>Player</th>
            <th>Likelihood of Overuse Injury</th>
            <th>Predicted Injury Flag Rate</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {filtered_data.map((dp) => (
            <tr key={dp.player_id} style={getRowStyle(dp.predicted_injury_flag_rate)} onClick={() => {
              changeView("player_detail");
              setPlayer(dp.player_id);
              selectedPlayer(dp.player_id);
              }}>
              <td>{dp.player_id}</td>
              <td>{dp.player_name}</td>
              <td>{dp.injury_predicted_prob}</td>
              <td>{dp.predicted_injury_flag_rate}</td>
              <td>{dp.session_date}</td>
            </tr>
          ))}
        </tbody>

      </table>
      
    </div>
  );
} 


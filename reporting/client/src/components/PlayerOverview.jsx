import { useEffect, useState } from "react";



export default function HospitalSearch({SelectedDate, changeView,selectedPlayer}) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [player_id, setPlayer] = useState("");


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

  useEffect(() => {
      const state_url = `http://127.0.0.1:5000/api/model_results/${encodeURIComponent(SelectedDate)}`;
      fetch(state_url)
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
    }, [SelectedDate]);
  
    if (loading) return <p>Loading data...</p>;
    if (error) return <p style={{ color: "red" }}>Error: {error}</p>;

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
          {data.map((dp) => (
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


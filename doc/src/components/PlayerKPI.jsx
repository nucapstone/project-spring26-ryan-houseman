import { PieChart, Pie, Cell, Label} from "recharts";

const COLORS = ["#1ABC9C","#f87171"];

export default function PlayerKPI({SelectedDate, player_id, playerData}) {
  const player = playerData.find(item => item.session_date === SelectedDate && item.player_id === player_id);
  const toPercent = (val, decimals = 1) => `${(val * 100).toFixed(decimals)}%`;

  const donut_input  = [
    {name: "Freshness", value: player.player_freshness/10},
    {name: "Fatigue", value: (1000 - player.player_freshness)/10},
  ]
  
  const KPIstyle = (label, value, threshold) => {
    if (label === "Predicted Injury Likelihood" && value > threshold) {
      return { flex: 1, padding: "1rem", border: "3px solid #f87171", borderRadius: "8px", textAlign:"center", backgroundColor: "rgba(248, 113, 113, 0.15)"}; 
    } else {
      return { flex: 1, padding: "1rem", border: "3px solid #e2e8f0", borderRadius: "8px", textAlign:"center"}; 
    }
  };

  const kpis = [
  { label: "Predicted Injury Likelihood", value: toPercent(player.injury_predicted_prob)},
  { label: `Sessions Flagged in Previous ${player.prediction_window} Days`,   value: `${toPercent(player.predicted_injury_flag_rate_window)} (${player.injury_flag_cnt_window}/${player.session_cnt_window})`},
  { label: "Distance Covered",  value: player.distance.toLocaleString()},
  ];

  const CenterLabel = () => {
    return (
      <>
        <text x={150} y={140} textAnchor="middle" dominantBaseline="middle" style={{ fontSize: "3rem", fontWeight: "bold", fill:"#2c3e50" }}>
          {player.player_freshness}
        </text>
        <text x={150} y={170} textAnchor="middle" dominantBaseline="middle" style={{ fontSize: "1.5rem", fill: "#2c3e50" }}>
          Player Freshness
        </text>
      </>
    );
  };


  return (
    <div>
        <h2>{player.player_name}</h2>
    <div style={{ display: "flex", gap: "1rem", marginBottom: "1.5rem", marginTop: "1.5rem", 
                  alignItems: "center", marginRight:"1.5rem", minHeight:"100px"}}>
      <div style={{ position: "relative", width: 300, height: 300, flex: 1 }}>
        <PieChart width={300} height={300}>
          <Pie
            data={donut_input}
            cx={150}
            cy={150}
            innerRadius={80}
            outerRadius={110}
            dataKey="value"
          >
            {donut_input.map((entry, index) => (
              <Cell key={index} fill={COLORS[index]} />
            ))}
            <Label content={<CenterLabel />} position="center" />
          </Pie>
        </PieChart>

      </div>
      {kpis.map(({ label, value }) => (
        <div key={label} style={KPIstyle(label,player.injury_predicted_prob,player.prediction_threshold)}>  
          <p>{label}</p>
          <h2>{value}</h2>
        </div>
      ))}
    </div>
    </div>
  );
}

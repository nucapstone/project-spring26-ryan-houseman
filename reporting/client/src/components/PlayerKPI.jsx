import { PieChart, Pie, Cell, Tooltip } from "recharts";

const COLORS = ["#1ABC9C","#f87171"];

export default function PlayerKPI({SelectedDate, player_id, playerData}) {
  const player = playerData.find(item => item.session_date === SelectedDate && item.player_id === player_id);
  // const toPercent = (val, decimals = 1) => `${(val * 100).toFixed(decimals)}%`;

  console.log(player);

  const donut_input  = [
    {name: "Freshness", value: player.player_freshness/10},
    {name: "Fatigue", value: (1000 - player.player_freshness)/10},
  ]
  


  const kpis = [
  { label: "Injury Likelihood", value: player.injury_predicted_prob},
  { label: "Sessions Flag in Previous Week",   value: player.predicted_injury_flag_rate_window },
  { label: "Distance Covered",  value: player.distance },
  ];


  return (
    <div style={{ display: "flex", gap: "1rem", marginBottom: "1.5rem", marginTop: "1.5rem", alignItems: "center" }}>
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
          </Pie>
          <Tooltip />
        </PieChart>

        {/* Center label now sits over the donut */}
        <div style={{
          position: "absolute",
          top: "50%", left: "50%",
          transform: "translate(-50%, -50%)",
          textAlign: "center"
        }}>
          <div style={{ fontSize: "3rem", fontWeight: "bold" }}>{player.player_freshness}</div>
          <div style={{ fontSize: "1.5rem", color: "#6b7280" }}>Player Freshness</div>
        </div>
      </div>
      {kpis.map(({ label, value }) => (
        <div key={label} style={{ flex: 1, padding: "1rem", border: "3px solid #e2e8f0", borderRadius: "8px" }}>
          <p>{label}</p>
          <h2>{value}</h2>
        </div>
      ))}
    </div>
  );
}

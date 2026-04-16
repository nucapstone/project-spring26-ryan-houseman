import { PieChart, Pie, Cell, Label} from "recharts";

const COLORS = ["#1ABC9C","#f87171"];

export default function teamOverview({SelectedDate, teamData}) {
  const team_info = teamData.find(item => item.session_date === SelectedDate);
  const toPercent = (val, decimals = 1) => `${(val * 100).toFixed(decimals)}%`;

  const donut_input  = [
    {name: "Freshness", value: team_info.team_freshness/10},
    {name: "Fatigue", value: (1000 - team_info.team_freshness)/10},
  ]
  
  const KPIstyle = (label, value, threshold) => {
    if (label === "Average Injury Likelihood" && value > threshold) {
      return { flex: 1, padding: "1rem", border: "3px solid #f87171", borderRadius: "8px", textAlign:"center", backgroundColor: "rgba(248, 113, 113, 0.15)"}; 
    } else if (label === `Sessions Flagged in Previous ${team_info.prediction_window} Days` && value >= 0.2) {
      return { flex: 1, padding: "1rem", border: "3px solid #f87171", borderRadius: "8px", textAlign:"center", backgroundColor: "rgba(248, 113, 113, 0.15)"}; 
    } else {
      return { flex: 1, padding: "1rem", border: "3px solid #e2e8f0", borderRadius: "8px", textAlign:"center"}; 
    }
  };

  const kpis = [
  { label: "Average Injury Likelihood", value: toPercent(team_info.team_injury_predicted_prob), raw_value: team_info.team_injury_predicted_prob},
  { label: `Sessions Flagged in Previous ${team_info.prediction_window} Days`,   value: `${toPercent(team_info.team_predicted_injury_flag_rate_window)} (${team_info.injury_flag_cnt_window}/${team_info.team_session_cnt_window})`, raw_value: team_info.team_predicted_injury_flag_rate_window},
  { label: "Average Distance Covered",  value: team_info.distance.toLocaleString(), raw_value: team_info.distance},
  ];

  const CenterLabel = () => {
    return (
      <>
        <text x={150} y={140} textAnchor="middle" dominantBaseline="middle" style={{ fontSize: "3rem", fontWeight: "bold", fill:"#2c3e50" }}>
          {team_info.team_freshness}
        </text>
        <text x={150} y={170} textAnchor="middle" dominantBaseline="middle" style={{ fontSize: "1.5rem", fill: "#2c3e50" }}>
          Team Freshness
        </text>
      </>
    );
  };


  return (
    <div>
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
      {kpis.map(({ label, value, raw_value }) => (
        <div key={label} style={KPIstyle(label,raw_value,team_info.prediction_threshold)}>  
          <p>{label}</p>
          <h2>{value}</h2>
        </div>
      ))}
    </div>
    </div>
  );
}

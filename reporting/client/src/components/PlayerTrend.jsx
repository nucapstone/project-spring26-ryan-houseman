import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import trendlinePlugin from 'chartjs-plugin-trendline';

// Register Chart.js components and the trendline plugin
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  trendlinePlugin
);

export default function PlayerTrend({SelectedDate, player_id, data, teamData}) {

  const player_info = data.find(item => item.session_date === SelectedDate && item.player_id === player_id);
  const playerData = data.filter(item => item.player_id === player_id);
  const toPercent = (val, decimals = 1) => `${(val * 100).toFixed(decimals)}%`;

  const labels = playerData.map(item => item.session_date);
  const values = playerData.map(item => item.injury_predicted_prob);
  const highlightIndex = labels.indexOf(SelectedDate);

  const labels_team = teamData.map(item => item.session_date);
  const values_team = teamData.map(item => item.team_injury_predicted_prob);

  const threshold = playerData.map(item => item.prediction_threshold);

  const chartData = {
    labels,
    datasets: [
      {
        label: `Injury Likelihood (${player_info.player_name})`,
        data: values,
        borderColor: "rgba(44,62,80, 1)",
        backgroundColor: "rgba(44,62,80, 0.2)",
        fill: false,
        tension: 0.1
        // trendlineLinear: {
        //   colorMin: "rgba(26, 188, 156, 1)",
        //   colorMax: "rgba(26, 188, 156, 1)",
        //   lineStyle: "solid",
        //   width: 3
        // }
      },
      {
        label: "Injury Likelihood (Team Average)",
        data: values_team,
        borderColor: "rgba(189, 189, 189, 1)",
        backgroundColor: "rgba(189, 189, 189, 0.3)",
        fill: false,
        tension: 0.1,
      },
      {
        label: `Injury Flag Threshold - ${toPercent(player_info.prediction_threshold)}`,
        data: threshold,
        borderColor: "rgba(248, 113, 113, 1)",
        backgroundColor: "rgba(248, 113, 113, 0.4)",
        fill: false,
        tension: 0.1,
        borderDash: [5,5]
      },
      {
        label: "Current Date",
        data: labels.map((_, i) => i === highlightIndex ? values[i] : null),
        borderColor: "#1ABC9C",
        backgroundColor: "rgba(152, 241, 223, 0.8)",
        pointRadius: 11,
        pointHoverRadius: 11,
        showLine: false,
        tooltip: false
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio:true,
    plugins: {
      legend: { position: "top" },
      title: { 
        display: true, 
        color: "#2c3e50",
        text: "Predicted Likelihood of Overuse Injury",
        font: {size:20, family:"sans-serif",lineHeight:1.15} 
       },
      tooltip: {
        callbacks: {
          label: (context) => `${(context.parsed.y * 100).toFixed(1)}%`
        },
        enabled: true,
        filter: (item) => item.dataset.label !== `Injury Flag Threshold - ${toPercent(player_info.prediction_threshold)}` && item.dataset.label !== "Current Date"
      }
    },
    scales: {
      x: {
        ticks: {
          maxTicksLimit: 8,        // limit x axis labels to 8 dates
          maxRotation: 45,         // rotate labels to prevent overlap
          minRotation: 45,
        }
      },
      y: {
      ticks: {
        callback: (val) => `${(val * 100).toFixed(1)}%`  // format y axis labels too
      }
      }
    }
  };

  return (
    <div style={{ width: '80%', margin: '0 auto' }}>
      <Line data={chartData} options={options} />
    </div>
  );
}


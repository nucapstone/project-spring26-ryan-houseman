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

export default function TeamTrend({SelectedDate, teamData}) {
  const toPercent = (val, decimals = 1) => `${(val * 100).toFixed(decimals)}%`;

  const labels = teamData.map(item => item.session_date);
  const values = teamData.map(item => item.team_freshness);
  const highlightIndex = labels.indexOf(SelectedDate);

  const threshold = teamData.map(item => item.prediction_threshold);
  const high_risk = Array(teamData.length).fill(200);
  const medium_risk = Array(teamData.length).fill(500);

  const chartData = {
    labels,
    datasets: [
      {
        label: `Team Freshness`,
        data: values,
        borderColor: "rgba(44,62,80, 1)",
        backgroundColor: "rgba(44,62,80, 0.2)",
        fill: false,
        tension: 0.1,
        trendlineLinear: {
          colorMin: "rgba(26, 188, 156, 1)",
          colorMax: "rgba(26, 188, 156, 1)",
          lineStyle: "solid",
          borderDash: [5,5],
          width: 3
        }
      },
      {
        label: "Current Date",
        data: labels.map((_, i) => i === highlightIndex ? values[i] : null),
        borderColor: "#1ABC9C",
        backgroundColor: "rgba(152, 241, 223, 0.8)",
        pointRadius: 12,
        pointHoverRadius: 12,
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
        text: "Team Freshness",
        font: {size:20, family:"sans-serif",lineHeight:1.15} 
       },
      tooltip: {
        enabled: true,
        filter: (item) => item.dataset.label !== "High Risk Threshold" && item.dataset.label !== "Medium Risk Threshold" && item.dataset.label !== "Current Date"
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
        stepSize: 100
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


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

export default function PlayerTrend({SelectedDate, player_id, data}) {

  const playerData = data.filter(item => item.player_id === player_id);
  if (!playerData.length) return <p>No trend data found for this player.</p>;
  const toPercent = (val, decimals = 1) => `${(val * 100).toFixed(decimals)}%`;

  const labels = playerData.map(item => item.session_date);
  const values = playerData.map(item => item.injury_predicted_prob);
  const highlightIndex = labels.indexOf(SelectedDate);

  const chartData = {
    labels,
    datasets: [
      {
        label: SelectedDate,
        data: labels.map((_, i) => i === highlightIndex ? values[i] : null),
        borderColor: "#1ABC9C",
        backgroundColor: "rgba(152, 241, 223, 1)",
        pointRadius: 8,
        pointHoverRadius: 8,
        showLine: false
      },
      {
        label: "Likelihood of Injury",
        data: values,
        borderColor: "rgba(44,62,80, 1)",
        backgroundColor: "rgba(44,62,80, 0.2)",
        fill: false,
        tension: 0.1,
        trendlineLinear: {
          colorMin: "rgba(26, 188, 156, 1)",
          colorMax: "rgba(26, 188, 156, 1)",
          lineStyle: "solid",
          width: 3
        }
      },
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio:true,
    plugins: {
      legend: { position: "top" },
      title: { display: true, text: "Predicted Likelihood of Overuse Injury" },
      tooltip: {
        callbacks: {
          label: (context) => `${(context.parsed.y * 100).toFixed(1)}%`
        },
        enabled: true}
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


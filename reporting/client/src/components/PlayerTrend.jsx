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

  const labels = playerData.map(item => item.session_date);
  const values = playerData.map(item => item.injury_predicted_prob);
  const highlightIndex = labels.indexOf(SelectedDate);

  const chartData = {
    labels,
    datasets: [
      {
        label: SelectedDate,
        data: labels.map((_, i) => i === highlightIndex ? values[i] : null),
        borderColor: "rgba(255, 165, 0, 1)",
        backgroundColor: "rgba(255, 165, 0, 0.7)",
        pointRadius: 7,
        pointHoverRadius: 7,
        showLine: false
      },
      {
        label: "Likelihood of Injury",
        data: values,
        borderColor: "rgba(75, 192, 192, 1)",
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        fill: false,
        tension: 0.1,
        trendlineLinear: {
          style: "rgba(255,105,180, 0.8)",
          lineStyle: "solid",
          width: 2
        }
      },
    ]
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: "top" },
      title: { display: true, text: "Predicted Likelihood of Overuse Injury" },
      tooltip: {enabled: true}
    }
  };

  return (
    <div style={{ width: '600px', margin: '0 auto' }}>
      <Line data={chartData} options={options} />
    </div>
  );
}


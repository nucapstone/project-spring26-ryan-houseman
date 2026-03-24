import { useEffect, useState } from "react";

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

export default function PlayerTrend({changeView, player_id}) {
  const [player, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
      const facility_url = `http://127.0.0.1:5000/api/player_trend/${encodeURIComponent(player_id)}`;
      fetch(facility_url)
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
    }, [player_id]);
  
    if (loading) return <p>Loading data...</p>;
    if (error) return <p style={{ color: "red" }}>Error: {error}</p>;

    const labels = player.session_date;
    const dataValues = player.injury_predicted_prob;

    // Chart data configuration
    const data = {
      labels,
      datasets: [
        {
          label: 'Monthly Sales',
          data: dataValues,
          borderColor: 'rgba(75, 192, 192, 1)',
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          fill: true,
          tension: 0.3, // smooth curve
          pointRadius: 5,
          pointHoverRadius: 7,
          // Trendline configuration
          trendlineLinear: {
            style: 'rgba(255,105,180,0.8)',
            lineStyle: 'dotted',
            width: 2
          }
        }
      ]
    };

    // Chart options
    const options = {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: 'Predicted Likelihood of Overuse Injury Trend - {player.player_name}'
        },
        legend: {
          position: 'top'
        }
      },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    };

    return (
      <div style={{ width: '600px', margin: '0 auto' }}>
        <Line data={data} options={options} />
      </div>
    );
}


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

export default function PlayerTrend({SelectedDate, player_id}) {
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const facility_url = `http://127.0.0.1:5000/api/player_trend/${encodeURIComponent(player_id)}`;
    fetch(facility_url)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
        return res.json();
      })
      .then((jsonArray) => {
        if (!Array.isArray(jsonArray)) {
          throw new Error("Expected an array of objects from API");
        }

        // Extract labels and values from array
        const labels = jsonArray.map((item) => item.session_date);
        const values = jsonArray.map((item) => item.injury_predicted_prob);

        const highlightLabel = SelectedDate;
        const highlightIndex = labels.indexOf(highlightLabel);

        setChartData({
          labels,
          datasets: [
            // Highlight Current Date
            {
              label: highlightLabel,
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
        });
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching chart data:", err);
        setError(err.message);
        setLoading(false);
      });
  }, [SelectedDate, player_id]);

  const options = {
    responsive: true,
    plugins: {
      legend: { position: "top" },
      title: { display: true, text: "Predicted Likelihood of Overuse Injury" },
      tooltip: {enabled: true}
    }
  };

  if (loading) return <p>Loading chart...</p>;
  if (error) return <p style={{ color: "red" }}>Error: {error}</p>;

  return (
    <div style={{ width: '600px', margin: '0 auto' }}>
      <Line data={chartData} options={options} />
      {/* Player Detail Line Chart */}
    </div>
  );
}


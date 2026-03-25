import { useEffect, useState } from "react";

export default function Dropdown({curView, onSelect, player_id}) {
  const [options, setData] = useState([]);
  const [selected, setSelected] = useState("2025-11-22");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  let dates_url;
  if (curView === "player_overview") {
    dates_url = "http://127.0.0.1:5000/api/dates";
  } else {
    dates_url = `http://127.0.0.1:5000/api/player_dates/${encodeURIComponent(player_id)}`;
  }

  useEffect(() => {
      fetch(dates_url)
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
    }, []);
  
    if (loading) return <p>Loading data...</p>;
    if (error) return <p style={{ color: "red" }}>Error: {error}</p>;

  return (
    <div>
      <label htmlFor="dropdown">Choose an option: </label>
      <select
        id="dropdown"
        value={selected}
        onChange={(e) => {
          const value = e.target.value;
          setSelected(value);
          onSelect(value);
        }}
      >
        <option value="">-- Select --</option>
        {options.map((opt) => (
          <option key={opt.id} value={opt.id}>
            {opt.session_date}
          </option>
        ))}
      </select>
    </div>
  );
}

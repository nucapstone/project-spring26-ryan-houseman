import { useEffect, useMemo, useState } from "react";

export default function Dropdown({ curView, onSelect, selectedDate, player_id, data }) {

  const options = useMemo(() => {
    const sortedDates = (arr) =>
      [...new Set(arr.map(item => item.session_date))].sort().reverse();

    if (curView === "player_detail" && player_id) {
      const playerData = data.filter(item => String(item.player_id) === String(player_id));
      return sortedDates(playerData);
    }

    return sortedDates(data);
  }, [curView, player_id, data]);

  // If the current selectedDate isn't in the new options list, fall back to latest
  const value = options.includes(selectedDate) ? selectedDate : options.at(0);

  return (
    <div style={{marginBottom:"1.5rem", marginTop:"1.5rem"}}>
      <label htmlFor="dropdown">Select a Date: </label>
      <select
        id="dropdown"
        value={value}
        onChange={(e) => onSelect(e.target.value)}
      >
        {options.map((opt) => (
          <option key={opt} value={opt}>{opt}</option>
        ))}
      </select>
    </div>
  );
}
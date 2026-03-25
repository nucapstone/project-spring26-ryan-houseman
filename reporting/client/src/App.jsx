import React, { useState, useRef, useEffect } from "react";
import Dropdown from "./components/Dropdown";
import PlayerOverview from "./components/PlayerOverview";
import PlayerDetail from "./components/PlayerDetail";
import PlayerTrend from "./components/PlayerTrend";

function App() {
  const [selectedValue, setSelectedValue] = useState("2025-11-22");
  const[selectedPlayer,setSelectedPlayer] = useState("");
  const [view, SetView] = useState("player_overview");

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>BMS Injury Prediction Model</h1>
      {view === "player_overview" && <Dropdown curView={view} onSelect={setSelectedValue} player_id={selectedPlayer}/>}
      {view === "player_overview" && <PlayerOverview SelectedDate={selectedValue} changeView={SetView} selectedPlayer={setSelectedPlayer}/>}
      {view === "player_detail" && <Dropdown curView={view} onSelect={setSelectedValue} player_id={selectedPlayer}/>}
      {view === "player_detail" && <PlayerDetail SelectedDate={selectedValue} changeView={SetView} player_id={selectedPlayer}/>}
      {view === "player_detail" && <PlayerTrend SelectedDate={selectedValue} player_id={selectedPlayer}/>}
    </div>
  );
}

export default App;


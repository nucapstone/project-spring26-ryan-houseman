import React, { useState, useRef, useEffect } from "react";
import Dropdown from "./components/Dropdown";
import PlayerOverview from "./components/PlayerOverview";
// import HospitalDetail from "./components/HospitalDetail";

function App() {
  const [selectedValue, setSelectedValue] = useState("2025-11-22");
  const[selectedPlayer,setSelectedPlayer] = useState("");
  const [view, SetView] = useState("player_overview");

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>BMS Injury Prediction Model</h1>
      {view === "player_overview" && <Dropdown onSelect={setSelectedValue}/>}
      {view === "player_overview" && <PlayerOverview SelectedDate={selectedValue} changeView={SetView} selectedPlayer={setSelectedPlayer}/>}
      {/* {view === "detail" && <HospitalDetail changeView={SetView} facility_id={selectedFacility}/>} */}
    </div>
  );
}

export default App;


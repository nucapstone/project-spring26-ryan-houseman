import { useState, useMemo} from "react";
import Dropdown from "./components/Dropdown";
import PlayerOverview from "./components/PlayerOverview";
import PlayerTrend from "./components/PlayerTrend";
import PlayerKPI from "./components/PlayerKPI";
import TeamOverview from "./components/TeamOverview";
import TeamTrend from "./components/TeamTrend";
import About from "./components/About";

import rpt1_data from './data/rpt1.json';
import rpt2_data from './data/rpt2.json';
import data_dictionary from './data/data_dictionary.json';

import bio_img from "./photos/houseman_about_me_photo.jpg"

function App() {
  const dates = useMemo(() =>
  [...new Set(rpt1_data.map(item => item.session_date))].sort().reverse()
  , []);

  const filtered_date = rpt1_data.filter(item => item.session_date === dates.at(0));
  const defaultPlayer = useMemo(() =>
    filtered_date.map(item => item.player_id).sort((a, b) => a - b)[0]
  , []);

  const[selectedPlayer,setSelectedPlayer] = useState(defaultPlayer);
  const [view, setView] = useState("team_overview");
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [SelectedDate, setSelectedDate] = useState(dates.at(0)); // only runs once on mount


  return (
    <div style={{ display: "flex", fontFamily: "Arial", minHeight: "100vh", margin: 0, padding: 0}}>

      {/* Sidebar */}
      <div style={{
        width: sidebarOpen ? "200px" : "40px",
        minHeight: "100vh",
        background: "#2c3e50",
        color: "white",
        transition: "width 0.3s",
        overflow: "hidden",
        flexShrink: 0,
      }}>
        {/* Toggle button */}
        <button
          onClick={() => setSidebarOpen(o => !o)}
          style={{
            width: "100%",
            background: "none",
            border: "none",
            color: "whitesmoke",
            fontSize: "20px",
            cursor: "pointer",
            padding: "12px",
            textAlign: "right",
          }}
        >
          {sidebarOpen ? "←" : "→"}
        </button>

        {/* Navigation*/}
        {sidebarOpen && (
          <nav style={{ display: "flex", flexDirection: "column", gap: "4px", padding: "8px" }}>
            {[
              { label: "Team Overview", value: "team_overview" },
              { label: "Player Overview", value: "player_overview" },
              { label: "Player Detail", value: "player_detail" },
              { label: "About", value: "about" },
            ].map(({ label, value }) => (
              <button
                key={value}
                onClick={() => setView(value)}
                style={{
                  background: view === value ? "#1abc9c" : "none",
                  border: "none",
                  color: "whitesmoke",
                  padding: "10px 14px",
                  textAlign: "left",
                  cursor: "pointer",
                  borderRadius: "4px",
                  fontFamily: "Arial",
                  fontSize: "14px",
                }}
              >
                {label}
              </button>
            ))}
          </nav>
        )}
      </div>

      {/* Main Pages */}

    <div style={{ flex: 1, minWidth: 0, padding: "20px", fontFamily: "Arial"}}>
      <h1>Overuse Injury Prediction Model</h1>
      {view === "player_overview" && <Dropdown curView={view} onSelect={setSelectedDate} selectedDate={SelectedDate} player_id={selectedPlayer} data={rpt1_data}/>}
      {view === "player_overview" && <PlayerOverview SelectedDate={SelectedDate} changeView={setView} selectedPlayer={setSelectedPlayer} data={rpt1_data}/>}
      {view === "player_detail" && <Dropdown curView={view} onSelect={setSelectedDate} selectedDate={SelectedDate} player_id={selectedPlayer} data={rpt1_data}/>}
      {view === "player_detail" && <PlayerKPI SelectedDate={SelectedDate} player_id={selectedPlayer} playerData={rpt1_data}/>}
      {view === "player_detail" && <PlayerTrend SelectedDate={SelectedDate} player_id={selectedPlayer} data={rpt1_data} teamData={rpt2_data}/>}
      {view === "team_overview" && <Dropdown curView={view} onSelect={setSelectedDate} selectedDate={SelectedDate} player_id={selectedPlayer} data={rpt1_data}/>}
      {view === "team_overview" && <TeamOverview SelectedDate={SelectedDate} teamData={rpt2_data}/>}
      {view === "team_overview" && <TeamTrend SelectedDate={SelectedDate} teamData={rpt2_data}/>}
      {view === "about" && <About data_dictionary={data_dictionary} bio_img={bio_img}/>}
    </div>
  
  </div>
  );
}

export default App;


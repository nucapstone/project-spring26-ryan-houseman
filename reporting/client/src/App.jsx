import { useState, useMemo} from "react";
import Dropdown from "./components/Dropdown";
import PlayerOverview from "./components/PlayerOverview";
import PlayerDetail from "./components/PlayerDetail";
import PlayerTrend from "./components/PlayerTrend";
import rpt1_data from './data/rpt1.json';

function App() {
  const[selectedPlayer,setSelectedPlayer] = useState("");
  const [view, SetView] = useState("player_overview");

  const dates = useMemo(() =>
  [...new Set(rpt1_data.map(item => item.session_date))].sort().reverse()
  , []);
  const [SelectedDate, setSelectedDate] = useState(dates.at(0)); // only runs once on mount


  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>BMS Injury Prediction Model</h1>
      {view === "player_overview" && <Dropdown curView={view} onSelect={setSelectedDate} selectedDate={SelectedDate} player_id={selectedPlayer} data={rpt1_data}/>}
      {view === "player_overview" && <PlayerOverview SelectedDate={SelectedDate} changeView={SetView} selectedPlayer={setSelectedPlayer} data={rpt1_data}/>}
      {view === "player_detail" && <Dropdown curView={view} onSelect={setSelectedDate} selectedDate={SelectedDate} player_id={selectedPlayer} data={rpt1_data}/>}
      {view === "player_detail" && <PlayerDetail SelectedDate={SelectedDate} changeView={SetView} player_id={selectedPlayer} data={rpt1_data}/>}
      {view === "player_detail" && <PlayerTrend SelectedDate={SelectedDate} player_id={selectedPlayer} data={rpt1_data}/>}
    </div>
  );
}

export default App;


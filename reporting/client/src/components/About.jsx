export default function About({data_dictionary, bio_img}) {

  const gps_dictionary = data_dictionary.filter(item => item.table_name === "gps_data");
  const injury_dictionary = data_dictionary.filter(item => item.table_name === "injury_data");


  const getRowStyle = (player_freshness) => {
      return { backgroundColor: "#E9FCF8", color:"#2c3e50"}; 
  };


  return (
    <div style={{width: "100%", textAlign:"left"}}>
      <p style={{ marginTop: "1rem", marginBottom: "1rem" }}>Welcome to the about page of the Overuse Injury Prediction Model.  
        This page includes background information and documentation related to the 
        the injury prediction model, and the associated reporting you see in this webpage.  
      </p>
      <p style={{ marginBottom: "1rem", fontWeight: "bold" }}>
        PLEASE NOTE that all data currently populating the webpage is entirely simulated.  
        There is no connection to any real people, and all results are entirely random.
      </p>
      <p style={{ marginBottom: "1rem" }}>
        If you wish to run this model and reporting on your own GPS and Injury data, 
        please refer to the repository below for more detailed instructions.
      </p>
      <a href="https://github.com/nucapstone/project-spring26-ryan-houseman/tree/main" target="_blank" rel="noopener noreferrer"  style={{ color: "#1abc9c"}}>
        Overuse Injury Prediction Model - Repository
      </a>
      <h3 style={{marginTop:"1.5rem"}}>Project Background</h3>
      <p style={{marginBottom: "1rem" }}>
         In the Fall 2025 Season, the Bowdoin College soccer team began using a GPS tracking sevice through PlayerData 
         to collect GPS data on player movement for practices and games.  Many other collegiate teams across many sports
          are beginning to do the same.  The service provides some reporting on this data, but at the college level,
           small coaching staffs often don't have the resources or time to do their own in depth analysis.
             The purpose of this project is to leverage the GPS data from PlayerData to build a player 
             injury prediction model for overuse injuries.  More specifically, the model aims to predict the likelihood that a player 
             will sustain an overuse injury in the upcoming week.
      </p>
      <h3>Input Data</h3>
      <p style={{marginBottom: "1rem" }}>
         Inputs for the model include both GPS player tracking data as well as player injury data.  This project leverages GPS data from PlayerData, which is available from
         the software's CVS builder page.  The model inputs assume that all columns from PlayerData's output are included, and that yards are used as the unit of measurement.  
         Data dictionaries for the GPS and injury data are below.  The raw GPS data will contain additional columns, but only columns relevant to the injury prediction model are listed.
      </p>
      <a href="https://playerdata.com/en-us" target="_blank" rel="noopener noreferrer"  style={{ color: "#1abc9c"}}>
        PlayerData
      </a>
      <h4 style={{marginTop:"1.5rem"}}>GPS Data Dictionary</h4>
      <table border="1" cellPadding="8" style={{ borderCollapse: "collapse", cursor: "pointer", tableLayout: "fixed", width:"65%", marginBottom:"1.5rem"}}>
        <thead>
          <tr>
            <th style={{wordWrap: "break-word", whiteSpace: "normal", backgroundColor: "#2c3e50", color: "whitesmoke", padding: "10px 14px"}}>Column Name</th>
            <th style={{wordWrap: "break-word", whiteSpace: "normal", backgroundColor: "#2c3e50", color: "whitesmoke", padding: "10px 14px"}}>Column Description</th>
          </tr>
        </thead>
        <tbody>
          {gps_dictionary.map((dp) => (
            <tr key={dp.player_id} style={getRowStyle(dp.player_freshness)}>
              <td style={{wordWrap: "break-word", whiteSpace: "normal", padding: "8px 14px"}}>{dp.column}</td>
              <td style={{wordWrap: "break-word", whiteSpace: "normal", padding: "8px 14px"}}>{dp.description}</td>
            </tr>
          ))}
        </tbody>
      </table>  
      <h4>Injury Data Dictionary</h4>
      <table border="1" cellPadding="8" style={{ borderCollapse: "collapse", cursor: "pointer", tableLayout: "fixed", width:"65%", marginBottom:"1.5rem"}}>
        <thead>
          <tr>
            <th style={{wordWrap: "break-word", whiteSpace: "normal", backgroundColor: "#2c3e50", color: "whitesmoke", padding: "10px 14px"}}>Column Name</th>
            <th style={{wordWrap: "break-word", whiteSpace: "normal", backgroundColor: "#2c3e50", color: "whitesmoke", padding: "10px 14px"}}>Column Description</th>
          </tr>
        </thead>
        <tbody>
          {injury_dictionary.map((dp) => (
            <tr key={dp.player_id} style={getRowStyle(dp.player_freshness)}>
              <td style={{wordWrap: "break-word", whiteSpace: "normal", padding: "8px 14px"}}>{dp.column}</td>
              <td style={{wordWrap: "break-word", whiteSpace: "normal", padding: "8px 14px"}}>{dp.description}</td>
            </tr>
          ))}
        </tbody>
      </table>  
      <h3 style={{marginTop:"1.5rem"}}>Model Information</h3>   
      <p style={{marginBottom: "1rem" }}>
         The implementation of this project includes both a logistic regression model and a random forest model used to predict the likelihood
          of an overuse injury occurring in during an upcoming window of time.  The model currently uses a 7 day window for injury predictions,
           and 10 days was also tested with similar results.  For both models, the model is trained using cross-validation on all available
            training data, and then run on the current season's data for front-end reporting.
      </p> 
      <p style={{marginBottom: "1rem" }}>
         Due to the significant class imbalance in the model's target variable (occurrence of an overuse injury in the upcoming week),
         modeling results were judged based on their precision and recall for accurately predicting injuries.  The random forest model does not currently
         yield reliable results, but there is hope that both models will improve as more data becomes available over time.  The project currently uses
         the logistic regression modeling results for all front-end reporting.    
      </p> 
      <p style={{marginBottom: "1rem" }}>
         Leading up to an injury, a player may have many data points available.  As dictated by the model configurations, each of those data points are a value of 1.
           In reality, it's not expected that the signs of an overuse injury would be present in all of those data points 
           (some practices may be easier, so it's hard to tell if a player is seriously fatigued or susceptible to injury). 
            Because of this, the reporting associated with the model outputs focuses on a higher recall and identifying players who have multiple flags within a short timespan.
             While some players may be incorrectly flagged for injury (lower precision), most injuries do have several data points flagged within a 7 day window leading up to the injury.    
      </p> 
      <h3 style={{marginTop:"1.5rem"}}>Reporting Notes</h3>   
      <p style={{marginBottom: "1rem" }}>
         The model reporting contains several wepages dedicated to different aspect of the model's ouptuts: 
         Team Overview, Player Overview, and Player Detail.  These pages, and the metrics within them are described in more detail below.  
         The pages were designed to help a coaching staff quickly identify players at elevated risk for overuse injury as well as track 
         overall team injury risk.  This could allow coaches to update training and recovery plans for specific players or the entire team. 
      </p>  
      <h4 style={{marginTop:"1.5rem"}}>Team Overview</h4>
      <p style={{marginBottom: "1rem" }}>
         Team Overview highlights various teamwide metrics for a given date.  The purpose of this page is to help a coaching staff identify
         the overall team injury risk.  If the team is very fatigued, coaches could shorten practice or focus on less physically demanding drills.
      </p> 
      <p style={{marginBottom: "1rem" }}>
         Average injury likelihood is displayed here.  On a given day, the GPS data point for each player is assigned an overuse injury likelihood.
         The value on this page is the team average for that day.  This value is highlighted red if the team's injury risk 
         is above the threshold used to flag injuries (more detail below). The percentage of data points flagged for injury risk is also
          displayed.  This is highlighted red if the rate is greater than or equal to 20% 
      </p> 
      <p style={{marginBottom: "1rem" }}>
         Additionally, the page has a "Team Freshness" metric.  This is an average value of "Player Freshness", which is weighted average of
         injury likelihood values from the previous week (more recent data is more important).  The score is standardized and scaled 
         to a range of 0 - 1000. The trend graph in this page illustrates the Team Freshness over the course of the season.
      </p> 
      <h4 style={{marginTop:"1.5rem"}}>Player Overview</h4>
      <p style={{marginBottom: "1rem" }}>
         Player Overview displays a list of all players who participated in a training session or match on a given day. 
         The data is sorted and color coded by the "Player Freshness" score described above.  Players with a Player Freshness below 200 
         are flagged as high risk, while players with a Player Freshness between 200 and 500 are flagged as medium risk.   
      </p> 
      <p style={{marginBottom: "1rem" }}>
         Selecting a row from the table will navigate to the Player Detail page for that player.  
      </p> 
      <h4 style={{marginTop:"1.5rem"}}>Player Detail</h4>
      <p style={{marginBottom: "1rem" }}>
         Player Detail displays the same metrics as Team Overview, but for the selected player only.  The trendline in this chart also 
         shows overuse injury likelihood compared to the team average over the course of the season.  The injury flagging threshold is 
         also included as a dashed red line in the chart.   
      </p> 
      <h4 style={{marginTop:"1.5rem"}}>Overuse Injury Flagging Threshold</h4>
      <p style={{marginBottom: "1rem" }}>
         As mentioned above, the model reporting focuses on a higher prediction recall compared to precision.  This means that some data 
         points will be incorrectly flagged for injuries, but most true injuries will be correctly flagged.  The prediction threshold 
         can be configured within the model, and it is currently set to whichever value correctly flags 50% of all injuries.  From there, 
         the web pages trend line charts and the Player Freshness metric help to identify which players may have several data points flagged 
         for injury within a short time span.      
      </p> 
      <h3 style={{marginTop:"1.5rem"}}>About Me</h3> 
      <p style={{marginBottom: "1rem" }}>
         Ryan Houseman is studying Data Science at Northeastern University's Roux Institute in Portland, Maine and will be graduating in after the Spring 2026 semester. 
          Ryan currently works on the data visualization and reporting team at Onpoint Health Data, and previously obtained an undergraduate degree in Mathematics from Bowdoin College in 2021.
          In his free time, Ryan enjoys surfing, telemark skiing, playing soccer and pond hockey.  Ryan is a former member of the Bowdoin College 
          soccer team and is still kicking it with Thunder FC in Portland Maine's SMUSL league.  
      </p> 
      <p style={{marginBottom: "1rem" }}>
        If you have questions related to this project, or want to implement on your own data connect with Ryan via email at rhouseman37@gmail.com    
      </p> 
      <img src={bio_img} alt="Houseman Photo" 
          style={{ width: "70%", maxWidth: "600px", borderRadius: "8px" }} >
      </img>
    </div>
  );
} 






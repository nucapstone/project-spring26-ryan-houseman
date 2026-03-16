-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS model_results;

CREATE TABLE model_results (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  player_id INTEGER,
  player_name TEXT,
  session_date TEXT,
  overuse_injury_day TEXT,
  injury_predicted_prob REAL,
  injury_prediction TEXT,
  injury_flag TEXT,
  injury_flag_cnt TEXT,
  predicted_injury_flag_rate REAL
);

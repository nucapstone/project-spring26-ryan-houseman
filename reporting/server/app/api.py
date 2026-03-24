from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify
from flask import json
from werkzeug.exceptions import abort

# from .auth import login_required
from .db import get_db

bp = Blueprint("bms_injury_prediction", __name__)

@bp.route("/api/model_results/<session_date>")
def get_model_results(session_date):
    db = get_db()
    results_out = db.execute(
        "SELECT player_id, player_name, session_date, overuse_injury_day, injury_flag, "
        "injury_predicted_prob, injury_prediction, predicted_injury_flag_rate"
            " FROM model_results"
            " WHERE session_date = ?"
            " ORDER BY predicted_injury_flag_rate DESC",
            (session_date,)
    ).fetchall()
    results = []
    for row in results_out:
        results.append(dict(row))    
    return jsonify(results)

@bp.route("/api/player_detail/<player_id>/<session_date>")
def get_player_detail(session_date, player_id):
    db = get_db()
    player_results = db.execute(
        "SELECT player_id, player_name, session_date, overuse_injury_day, injury_flag, "
        "injury_predicted_prob, injury_prediction, predicted_injury_flag_rate"
            " FROM model_results"
            " WHERE session_date = ? AND player_id = ?",
            (session_date,player_id)
    ).fetchone()
    return jsonify(dict(player_results))

@bp.route("/api/player_trend/<player_id>")
def get_player_trend(player_id):
    db = get_db()
    results_out = db.execute(
        "SELECT player_id, player_name, session_date,"
        "injury_predicted_prob, predicted_injury_flag_rate"
            " FROM model_results"
            " WHERE player_id = ?"
            " ORDER BY session_date",
            (player_id,)
    ).fetchall()
    results = []
    for row in results_out:
        results.append(dict(row))    
    return jsonify(results)

@bp.route("/api/dates")
def get_dates():
    db = get_db()
    dates_out = db.execute(
        "SELECT DISTINCT session_date as session_date"
            " FROM model_results"
            " ORDER BY session_date DESC"
    ).fetchall()
    dates =[]
    for row in dates_out:
      dates.append({"session_date":row[0]})
    return jsonify(dates)
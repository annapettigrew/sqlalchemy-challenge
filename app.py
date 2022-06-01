# Importing dependencies 
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from flask import Flask, jsonify
from sqlalchemy import create_engine, func 
from sqlalchemy.orm import Session 

# Setting up the database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect=True)
Base.classes.keys()

# Table References 
Station = Base.classes.station
Measurement = Base.classes.measurement

# Setting up Flask
app = Flask(__name__)

# Getting the Dates
most_recent_date = "2017-08-23"
most_recent_date_dt = dt.datetime.strptime(most_recent_date, "%Y-%m-%d")
time_d = most_recent_date_dt - dt.timedelta(days=366)

# Setting up Flask Routes
@app.route("/")
def welcome():
    return(
        f"Welcome to the Hawaii Climate App!<br>"
        f"Available Routes:<br/>"
        f"-Precipitation Observed<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"-List of Most Active Stations<br/>"
        f"/api/v1.0/stations<br/>"
        f"-Temperature Recordings<br/>"
        f"/api/v1.0/tobs<br/>"
        f"-Temperature Observed in Previous Year<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt"
    )
# Precipitation 
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    prec_output = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').filter(Measurement.date <= '2017-08-23').order_by(Measurement.date).all() 
    session.close()

    prcp_list = []
    for date, prcp in prec_output:
        data = {}
        data[date] = prcp
        prcp_list.append(data)
    return jsonify(prcp_list)

# Stations
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    # Most Active Stations JSON List 
    active_station = session.query(Measurement.station, func.count(Measurement.station)).\
                               group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all() 
    station_list = []
    for station in active_station:
        list = {}
        list['Name'] = station[0]
        list['Station'] = station[1]
        station_list.append(list)
    return jsonify(station_list)

# # Temperature List 
# @app.route("/api/v1.0/tobs")
# def tobs():
#     session = Session(engine)
#     active_temp = session.query(Station.name, Measurement.date, Measurement.tobs).\
#         filter(Measurement.date >= '2016-08-23', Measurement.date <= '2017-08-23').all()
#     temp_list = []
#     for temp in active_temp:
#         tobs = {}
#         tobs['Date'] = temp[1]
#         tobs['Station'] = temp[0]
#         tobs['Temperature'] = int(temp[2])
#         temp_list.append(tobs)
#     return jsonify(temp_list)

@app.route("/api/v1.0/<start>")
def start_date(start): 
    session = Session(engine)
    
    end_d = most_recent_date

    start_day = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date <= end_d ).all()
    start_list = []
    for min,max,avg in start_day:
        start_dict = {}
        start_dict["Min"] = min
        start_dict["Average"] = avg
        start_dict["Max"] = max
        start_list.append(start_dict)
    session.close()
    return jsonify(start_dict)
    
# Start/End Range
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start,end): 
    session = Session(engine)

    end_d = most_recent_date

    start_day = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date <= end_d ).all()
    end_list = []
    for min,max,avg in start_day:
        end_dict = {}
        end_dict["Min"] = min
        end_dict["Average"] = avg
        end_dict["Max"] = max
        end_list.append(end_dict)
    session.close()
    return jsonify(end_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    #getting the dates
    latest_date = session.query(Measurement.date).order_by(Measurement.date()).first()
    last_year = (dt.datetime.strptime(latest_date[0],'%Y-%m-%d') \
                    - dt.timedelta(days=365)).strftime('%Y-%m-%d')

    #query for the dates and temperature values
    results =   session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= last_year).\
                order_by(Measurement.date).all()

    #convert to list of dictionaries to jsonify
    tobs_list = []

    for date, tobs in results:
        list = {}
        list["Date"] = date
        list["Tobs"] = tobs
        tobs_list.append(list)

    session.close()

    return jsonify(tobs_list)

# Running the app
if __name__ == "__main__":
    app.run(debug=True)
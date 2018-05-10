# Import dependencies

from flask import Flask, jsonify
import session_queries as sq

# Flask Setup
app = Flask(__name__)

# Flask routes
@app.route("/", methods=["GET"])
def home():
    """API routes"""

    return  (
            "Available Routes:<br><br>"
            "<a href=/api/v1.0/precipitation>Precipitation observations for the previous year</a><br>"
            "<a href=/api/v1.0/stations>Stations list</a><br>"
            "<a href=/api/v1.0/tobs>Temperature observations (tobs) for the previous year</a><br>"
            "<a href =/api/v1.0/2017-01-01>Min, max and avg temperature as from given start date</a><br>"
            "<a href =/api/v1.0/2017-01-01/2017-07-31>Min, max and avg temperature as from given start and end date<br>"
            )

@app.route("/api/v1.0/precipitation", methods=["GET"])

def Flask_prcp():

    prcp_last_year = []
    for prcp in sq.prcp():
        prcp_dict = {}
        prcp_dict["Station"] = prcp.name
        prcp_dict["Date"] = prcp.date
        prcp_dict["Precipitation"] = prcp.prcp

        prcp_last_year.append(prcp_dict)

    return jsonify(prcp_last_year)
    
@app.route("/api/v1.0/stations", methods=["GET"])

def Flask_stations():

    all_stations = []
    for station in sq.stations():
        station_dict = {}
        station_dict["Station"] = station.station
        station_dict["Station name"] = station.name

        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs", methods=["GET"] )

def Flask_tobs():

    all_tobs = []
    for tob in sq.tobs():
        tobs_dict = {}
        tobs_dict["Station"] = tob.name
        tobs_dict["Date"] = tob.date
        tobs_dict["Temp (°F)"] = tob.tobs

        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/2017-01-01", methods=["GET"])

def Flask_start():

    all_normals = []
    for normal in sq.period_start():
        normals_dict = {}
        normals_dict["Date"] = normal.date
        normals_dict["Minimum temp (°F)"] = normal.min_temp
        normals_dict["Average temp (°F)"] = normal.avg_temp
        normals_dict["Maximum temp (°F)"] = normal.max_temp

        all_normals.append(normals_dict)

    return jsonify(all_normals)

@app.route("/api/v1.0/2017-01-01/2017-07-31", methods=["GET"])

def Flask_start_end():

    all_normals = []
    for normal in sq.period_start_end():
        normals_dict = {}
        normals_dict["Date"] = normal.date
        normals_dict["Minimum temp (°F)"] = normal.min_temp
        normals_dict["Average temp (°F)"] = normal.avg_temp
        normals_dict["Maximum temp (°F)"] = normal.max_temp

        all_normals.append(normals_dict)

    return jsonify(all_normals)

# Define main behavior
if __name__ == "__main__":
    app.run(debug=True)

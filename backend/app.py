import traceback
from flask import request, jsonify
import logging, time
import os
from datetime import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from sqlalchemy import Column, Float, func, Integer
from flask_cors import CORS
from flask_cors import cross_origin
from flask_swagger_ui import get_swaggerui_blueprint
import json 
# Initialize the Flask application
app = Flask(__name__)

# Setup CORS (Cross Origin Resource Sharing) for the application
CORS(app)
cors = CORS(app,origins=["*"])

# Configure and register Swagger UI blueprint for API documentation
SWAGGER_URL = '/swagger'
API_URL = 'http://127.0.0.1:5000/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Weather Station Data"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/swagger.json')
def swagger():  
    with open('swagger.json', 'r') as f:
        return jsonify(json.load(f))

# Configure the SQLAlchemy database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)

# Remove existing log file if exists
if os.path.exists('app.log'):
    os.remove('app.log')

# Setup logging configuration
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s'
)

# Define the WeatherData model to store weather records
class WeatherData(db.Model):
    rowId = db.Column(db.String(30), nullable=False, primary_key=True)
    weatherStation = db.Column(db.String(20), nullable=False)
    dateMMYY = db.Column(db.String(8), nullable=False)
    maxTemp = db.Column(db.Integer, nullable=True)
    minTemp = db.Column(db.Integer, nullable=True)
    precipitation = db.Column(db.Integer, nullable=True)

# Define the Statistics model to store calculated statistics
class statistics(db.Model):
    id = db.Column(db.String(30), primary_key=True, nullable=False)
    weatherStation = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    avgMxTemp = db.Column(db.Float, nullable=True)
    avgMnTemp = db.Column(db.Float, nullable=True)
    precipSum = db.Column(db.Float, nullable=True)


# Function to insert or update data into the User table
def insert_or_update_data(station_name, record_date, max_temp, min_temp, precipitation):
    try:
        # Create a new WeatherData instance
        new_data = WeatherData(rowId=str(station_name) + str(record_date), weatherStation=station_name,
                               dateMMYY=record_date, maxTemp=max_temp, minTemp=min_temp, precipitation=precipitation)
        # Add the new instance to the database session
        db.session.add(new_data)
        db.session.commit()
        return True
    except Exception as e:
        # Rollback the transaction in case of error
        db.session.rollback()
    finally:
        # Close the database session
        db.session.close()
    return False

# This function will run before the first request to setup the database
@app.before_first_request
def before_first_request():
    with app.app_context():
        db.create_all()

# Define the route for the root URL ('/') and allow GET requests
@app.route('/', methods=['GET'])
# Allow cross-origin requests
@cross_origin()
def home():
    try:
        # Record the start time of the process
        starttime = time.time()
        # Get the current working directory path
        directory_path = os.getcwd()
        # Get the parent directory path
        parent_directory = os.path.dirname(directory_path)
        # Formulate the directory path where the text files are located
        directory_path = os.path.join(parent_directory, 'code-challenge-template/wx_data')

        count = 0
        # Iterate through the filenames in the specified directory
        for filename in os.listdir(directory_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(directory_path, filename)
                # Extract the station name from the filename
                station_name = filename.split('.')[0]
                # Open the file for reading
                with open(file_path, 'r') as file:
                    # Read all lines from the file
                    lines = file.readlines()
                    for row in lines:
                        # Split the row into columns and reformat the date
                        row = row.rstrip("\n").split("\t")
                        row[0] = row[0][:4] + '/' + row[0][4:6] + '/' + row[0][6:]
                        date = datetime.strptime(row[0], '%Y/%m/%d').strftime('%Y-%m-%d')
                        max_temp = int(row[1])
                        min_temp = int(row[2])
                        precipitation = int(row[3])
                        # Call a function to insert or update the data in the database
                        if insert_or_update_data(station_name, date, max_temp, min_temp, precipitation):
                            count += 1
        # Record the end time of the process
        endtime = time.time()
        if count != 0:
            logging.error('Insertion starttime - %s', time.strftime("%H:%M:%S", time.localtime(starttime)))
            logging.error('Records Inserted: %s', count)
            logging.error('Insertion endtime - %s', time.strftime("%H:%M:%S", time.localtime(endtime)))

        # Define a nested function to extract the year from a date
        def extract_year(date):
            return func.extract('year', date)

        # Build a SQL query using SQLAlchemy
        query = db.session.query(
            WeatherData.weatherStation.label('station'),
            extract_year(WeatherData.dateMMYY).label('year'),
            func.avg(WeatherData.maxTemp).label('avg_max_temp'),
            func.avg(WeatherData.minTemp).label('avg_min_temp'),
            func.sum(WeatherData.precipitation).label('total_precip')
        ).filter(and_(WeatherData.maxTemp != -9999,WeatherData.minTemp != -9999,WeatherData.precipitation != -9999)
        ).group_by('station', 'year')

        # Execute the query and fetch results
        results = query.all()

        # Iterate through the results and create instances of the Statistics model
        for result in results:
            stats_instance = statistics(id = str(result[0])+str(result[1]),weatherStation=result[0],year=result[1],avgMxTemp=result[2],avgMnTemp=result[3],precipSum=result[4])
            db.session.add(stats_instance)
        db.session.commit()
        return {' ':' '}
    except Exception as e:
        # If an exception occurs, return an error response
        return {"status": "500", "message": str(e)}, 500

# Define a route for handling requests to '/api/weather' with a GET method
@app.route('/api/weather', methods=['GET'])
@cross_origin()# Allow requests from different origins (cross-origin requests)
def index():
    data = request.args # Get the query parameters from the request
    weather_station = data.get('weatherStation')# Get the value of 'weatherStation' parameter
    date_mmyy = data.get('dateMMYY')# Get the value of 'dateMMYY' parameter
    page_num = int(data.get('page')) # Get the value of 'page' parameter and convert to integer
    print(weather_station, date_mmyy)
    offset = page_num * 100 - 100# Calculate the offset for pagination
    # Query the database based on the provided parameters and apply pagination
    if weather_station and date_mmyy:
        # If both weather_station and date_mmyy are provided, filter by both
        weather_data = WeatherData.query.filter_by(weatherStation=weather_station, dateMMYY=date_mmyy).offset(offset).limit(100).all()
    elif weather_station:
        # If only weather_station is provided, filter by weather_station
        weather_data = WeatherData.query.filter_by(weatherStation=weather_station).offset(offset).limit(100).all()
    elif date_mmyy:
        # If only date_mmyy is provided, filter by date_mmyy
        weather_data = WeatherData.query.filter_by(dateMMYY=date_mmyy).offset(offset).limit(100).all()
    else:
        # If no filter is provided, just apply pagination
        weather_data = WeatherData.query.offset(offset).limit(100).all()

    output = []
    for data in weather_data:
        output.append({
            "rowId": data.rowId,
            "weatherStation": data.weatherStation,
            "dateMMYY": data.dateMMYY,
            "maxTemp": data.maxTemp,
            "minTemp": data.minTemp,
            "precipitation": data.precipitation
        })
     # Return the output data as JSON
    return { "weather_data": output }

# Define a route for handling requests to '/api/weather/stats' with a GET method
@app.route('/api/weather/stats', methods=['GET'])
@cross_origin()  # Allow requests from different origins (cross-origin requests)
def stats():
    data = request.args
    weather_station = data.get('weatherStation')
    year = data.get('year')
    page_num = int(data.get('page'))
    print(weather_station, year)
    response_data = {}
    offset = page_num * 100 - 100

    if year and weather_station:
        response_data=statistics.query.filter_by(weatherStation=weather_station,year=year).offset(offset).limit(100).all()
    elif weather_station:
        response_data=statistics.query.filter_by(weatherStation=weather_station).offset(offset).limit(100).all()
    elif year:
        response_data=statistics.query.filter_by(year=year).offset(offset).limit(100).all()
    else:
        response_data = statistics.query.offset(offset).limit(100).all()

    output_2 = []
    for data in response_data:
        output_2.append({"id": data.id,
            "weatherStation": data.weatherStation,
            "year": data.year,
            "avgMxTemp": data.avgMxTemp,
            "avgMnTemp": data.avgMnTemp,
            "precipSum": data.precipSum})
    # Return the output data as JSON
    return {"data": output_2}

    # except Exception as e:
    #     return {"status": "500", "message": str(e)}, 500

if __name__ == '__main__':
    app.run()

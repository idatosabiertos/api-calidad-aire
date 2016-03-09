# -*- coding: utf-8 -*-

from flask import Flask, request, redirect, url_for, Response
from flask.ext.mongoengine import MongoEngine
from flask.ext.mongorest import MongoRest
from flask.ext.mongorest.views import ResourceView
from flask.ext.mongorest.resources import Resource
from flask.ext.mongorest import operators as ops
from flask.ext.mongorest import methods
from werkzeug import secure_filename
from pymongo import MongoClient
import os
import string
import random
import zipfile
import pandas as pd
import numpy as np
import requests
import json
import datetime
import city_twitts
import csv

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['zip'])

class MyServer(Flask):

    def __init__(self, *args, **kwargs):
            super(MyServer, self).__init__(*args, **kwargs)

            #instanciate your variables here
            self.update_twitts_time = datetime.datetime.now()
            self.accounts = [{"city":"MXMEX","account":"RespiraDF"}]
            self.twitts = city_twitts.get_cities_tweets(self.accounts)

app = MyServer(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config.update(
    MONGODB_HOST = 'localhost',
    MONGODB_PORT = '27017',
    MONGODB_DB = 'api_calidad_del_aire',
)

db = MongoEngine(app)
api = MongoRest(app)

client = MongoClient()
db_query = client.api_calidad_del_aire

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response
app.after_request(add_cors_headers)

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class Country(db.Document):
    name = db.StringField()
    country_id = db.StringField()
    longitude = db.StringField()
    latitude = db.StringField()
    timezone = db.StringField()
    level = db.StringField()

class City(db.Document):
    name = db.StringField()
    city_id = db.StringField()
    longitude = db.StringField()
    latitude = db.StringField()
    timezone = db.StringField()
    level = db.StringField()
    country_id = db.StringField()

class Station(db.Document):
    name = db.StringField()
    station_id = db.StringField()
    longitude = db.StringField()
    latitude = db.StringField()
    timezone = db.StringField()
    level = db.StringField()
    country_id = db.StringField()
    city_id = db.StringField()
    local = db.StringField()

class Method(db.Document):
    method_id = db.StringField()
    method_shortdescription = db.StringField()
    method_protocol = db.StringField()
    method_device = db.StringField()

class Pollutant(db.Document):
    feed_id = db.StringField()
    station_id = db.StringField()
    pollutant_id = db.StringField()
    pollutant_unit = db.StringField()
    pollutant_update_time = db.StringField()
    pollutant_averaging = db.StringField()
    pollutant_value = db.StringField()

class Feed(db.Document):
    feed_id = db.StringField()
    feed_finishdate = db.StringField()
    feed_publisherurl = db.StringField()
    feed_publishername = db.StringField()
    feed_startdate= db.StringField()


class CountryResource(Resource):
    document = Country
    filters = {
        'name': [ops.Exact, ops.Startswith]
    }

class CityResource(Resource):
    document = City
    filters = {
        'name': [ops.Exact, ops.Startswith]
    }

class StationResource(Resource):
    document = Station
    filters = {
        'name': [ops.Exact, ops.Startswith],
        'local': [ops.Exact, ops.Startswith]
    }

class MethodResource(Resource):
    document = Method
    filters = {
        'name': [ops.Exact, ops.Startswith]
    }

class PollutantResource(Resource):
    document = Pollutant
    filters = {
        'name': [ops.Exact, ops.Startswith]
    }

class FeedResource(Resource):
    document = Feed
    filters = {
        'name': [ops.Exact, ops.Startswith]
    }



@api.register(name='countries', url='/countries/')
class CountryView(ResourceView):
    resource = CountryResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List]

@api.register(name='cities', url='/cities/')
class CityView(ResourceView):
    resource = CityResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List]

@api.register(name='stations', url='/stations/')
class CityView(ResourceView):
    resource = StationResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List]

@api.register(name='methods', url='/methods/')
class CityView(ResourceView):
    resource = MethodResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List]

@api.register(name='pollutants', url='/pollutants/')
class CityView(ResourceView):
    resource = PollutantResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List]

@api.register(name='feeds', url='/feeds/')
class CityView(ResourceView):
    resource = FeedResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List]

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def extract_files_here(filename,filepath):
    zip_ref = zipfile.ZipFile(filename, 'r')
    zip_ref.extractall(filepath)
    zip_ref.close()
    return os.listdir(filepath + "/output")

def get_data_per_key(endpoint, key):
    r = requests.get(endpoint)
    r_dict = r.json()
    print(r_dict)
    values_in_key = []
    if len(r_dict["data"]) > 0:
        for data_row in r_dict["data"]:
            values_in_key.append(data_row[key])
    return values_in_key

def send_local_dict(endpoint,data_dict):
    headers = {"Content-Type": "application/json", "charset":"UTF-8"}
    response = requests.post(endpoint, data=json.dumps(data_dict), headers=headers)
    return response

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            random_folder = id_generator()
            filepath = app.config['UPLOAD_FOLDER'] + "/" + random_folder
            os.makedirs(filepath)
            filename = filepath + "/" + secure_filename(file.filename)
            file.save(filename)
            files_in_folder = extract_files_here(filename,filepath)
            filepath = filepath + "/output"
            print filepath, files_in_folder


            ## Empieza llenado de bases, empezamos por geograficos
            #Paises
            if "countries.csv" in files_in_folder:
                countries_df =pd.DataFrame.from_csv(filepath+"/countries.csv",index_col=False)
                current_countries = get_data_per_key("http://104.197.214.72:8000/countries/", "country_id")
                for index, row in countries_df.iterrows():
                    if row['country_id'] not in current_countries:
                        local_dict = {
                            "name" : str(row["country_name"]),
                            "country_id" : str(row["country_id"]),
                            "longitude" : str(row["country_long"]),
                            "latitude" : str(row["country_lat"]),
                            "timezone" : str(row["country_timezone"]),
                            "level" : str("country")
                        }
                        send_local_dict("http://104.197.214.72:8000/countries/", local_dict)

            #ciudades
            if "cities.csv" in files_in_folder:
                cities_df =pd.DataFrame.from_csv(filepath+"/cities.csv",index_col=False)
                current_cities = get_data_per_key("http://104.197.214.72:8000/cities/", "city_id")
                for index, row in cities_df.iterrows():
                    if row['city_id'] not in current_cities:
                        local_dict = {
                            "name" : str(row["city_name"]),
                            "city_id" : str(row["city_id"]),
                            "longitude" : str(row["city_long"]),
                            "latitude" : str(row["city_lat"]),
                            "timezone" : str(row["city_timezone"]),
                            "level" : "city",
                            "country_id" : str(row["country_id"])
                        }
                        send_local_dict("http://104.197.214.72:8000/cities/", local_dict)
            #estaciones
            if "stations.csv" in files_in_folder:
                stations_df =pd.DataFrame.from_csv(filepath+"/stations.csv",index_col=False)
                current_stations = get_data_per_key("http://104.197.214.72:8000/stations/", "station_id")
                for index, row in stations_df.iterrows():
                    print(row)
                    if row['station_id'] not in current_stations:
                        local_dict = {
                            "name" : str(row["station_name"]),
                            "station_id" : str(row["station_id"]),
                            "longitude" : str(row["station_long"]),
                            "latitude" : str(row["station_lat"]),
                            "timezone" : str(row["station_timezone"]),
                            "level" : "station",
                            "country_id" : str(row["country_id"]),
                            "city_id" : str(row["city_id"]),
                            "local" : str(row["station_local"])
                        }
                        send_local_dict("http://104.197.214.72:8000/stations/", local_dict)

            #metodos
            if "methods.csv" in files_in_folder:
                methods_df =pd.DataFrame.from_csv(filepath+"/methods.csv",index_col=False)
                current_methods = get_data_per_key("http://104.197.214.72:8000/methods/", "method_id")
                for index, row in methods_df.iterrows():
                    if row['method_id'] not in current_methods:
                        local_dict = {
                            "method_id" : str(row["method_id"]),
                            "method_shortdescription" : str(row["method_short-description"]),
                            "method_protocol" : str(row["method_protocol"]),
                            "method_device" : str(row["method_device"])
                        }
                        send_local_dict("http://104.197.214.72:8000/methods/", local_dict)

            ##Empieza Subida Naive
            #contaminantes
            if "pollutants.csv" in files_in_folder:
                pollutants_df =pd.DataFrame.from_csv(filepath+"/pollutants.csv",index_col=False)
                for index, row in pollutants_df.iterrows():
                    local_dict = {
                        "feed_id"  : str(row["feed_id"]),
                        "station_id" : str(row["station_id"]),
                        "pollutant_id" : str(row["pollutant_id"]),
                        "pollutant_unit" : str(row["pollutant_unit"]),
                        "pollutant_update_time" : str(row["pollutant_update-time"]),
                        "pollutant_averaging" : str(row["pollutant_averaging"]),
                        "pollutant_value" : str(row["pollutant_value"])
                    }
                    send_local_dict("http://104.197.214.72:8000/pollutants/", local_dict)

            #Datos del feed
            if "feed_info.csv" in files_in_folder:
                feeds_df =pd.DataFrame.from_csv(filepath+"/feed_info.csv",index_col=False)
                for index, row in feeds_df.iterrows():
                    local_dict = {
                        "feed_id"  : str(row["feed_id"]),
                        "feed_finishdate" : str(row["feed_finish-date"]),
                        "feed_publisherurl" : str(row["feed_publisher-url"]),
                        "feed_publishername" : str(row["feed_publisher-name"]),
                        "feed_startdate" : str(row["feed_start-date"])
                    }
                    send_local_dict("http://104.197.214.72:8000/feeds/", local_dict)

            return Response(response=json.dumps([{"data":"OK"}]), status=200, mimetype="application/json")



    return '''
    <!doctype html>
    <title>Sube un nuevo archivo comprimido con los datos del estandar</title>
    <h1>Sube un archivo</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

#Extract time from a ISO 3601 string, to just contain the time that matters to the timeline
def extract_time(api_time, time_unit):
    stop_position = {
        "year": 4,
        "month":  7,
        "day": 10,
        "hour": 13,
        "minute": 16
    }
    try:
        return_time = api_time[0:stop_position[time_unit]]
    except:
        return_time = api_time
    if time_unit == "week":
        time_to_work_with = api_time[0:10]
        date_array = time_to_work_with.split("-")
        dt = datetime.date(int(date_array[0]), int(date_array[1]), int(date_array[2]))
        wk = dt.strftime("%V")
        return_time = date_array[0] + "-s"+ wk
    return return_time

    dt = datetime.date(2010, 6, 16)

@app.route('/cities-pollutant-timeline', methods=['GET'])
def indicator():
    greographical_zone = request.args.get('geographical_zone')
    dateUnit = request.args.get('dateUnit')
    now = request.args.get('now')
    filetype = request.args.get('filetype')
    if now is None:
        now = 0
    regex_construction = "^" + greographical_zone
    documents_by_zone = []
    for cursor in db_query.pollutant.find({'station_id':{'$regex': regex_construction}}):
        geo_local_dict = {}
        geo_local_dict['pollutant_id'] = cursor["pollutant_id"]
        geo_local_dict['pollutant_unit'] = cursor["pollutant_unit"]
        geo_local_dict['pollutant_value'] = cursor["pollutant_value"]
        trunc_time = extract_time(cursor["pollutant_update_time"], dateUnit)
        geo_local_dict['pollutant_update_time'] = trunc_time
        geo_local_dict['station_id'] = cursor["station_id"]
        documents_by_zone.append(geo_local_dict)
    geo_data = pd.DataFrame(documents_by_zone)
    geo_data['pollutant_value'] = geo_data['pollutant_value'].astype('float')
    pollutants_df = np.unique(geo_data["pollutant_id"])
    response_dict = {}
    pollutants_timelines = []
    pollutant_normalization = {"PM25": 25.0, "PM10": 50.0, "O3":50.0, "NO2":106.38 , "SO2": 190.83}
    for pollutant in pollutants_df:
        pollutant_dict = {}
        pollutant_dict["pollutant"] = pollutant
        pollutant_data = geo_data[(geo_data["pollutant_id"] == pollutant)]
        try:
            normalizing_value = float(pollutant_normalization[str(pollutant)])
        except:
            normalizing_value = "nan"
        pollutant_dict["unit"] = np.unique(pollutant_data["pollutant_unit"])[0]
        timeline = []
        time_frames = np.unique(geo_data['pollutant_update_time'])
        if int(now) == 0:
            for time_frame in time_frames:
                time_frame_data = pollutant_data[(pollutant_data["pollutant_update_time"] == time_frame)]
                time_frame_data = time_frame_data[np.isfinite(time_frame_data['pollutant_value'])]
                try:
                    mean_time_frame = time_frame_data[["pollutant_value"]].mean()
                    normalized_data = mean_time_frame["pollutant_value"]/normalizing_value
                except:
                    normalized_data = "nan"

                timeframe_dict = {"time": time_frame, "value": str(mean_time_frame["pollutant_value"]), "normalized":str(normalized_data)}
                timeline.append(timeframe_dict)
        else:
            time_frame = time_frames[-1]
            time_frame_data = pollutant_data[(pollutant_data["pollutant_update_time"] == time_frame)]
            mean_time_frame = time_frame_data[["pollutant_value"]].mean()
            try:
                normalized_data = mean_time_frame["pollutant_value"]/normalizing_value
            except:
                normalized_data = "nan"
            timeframe_dict = {"time": time_frame, "value": str(mean_time_frame["pollutant_value"]), "normalized":str(normalized_data)}
            timeline.append(timeframe_dict)

        pollutant_dict["timeline"] = timeline
        pollutants_timelines.append(pollutant_dict)
    response_dict["pollutants"] = pollutants_timelines
    response_dict["geographical_zone"] = greographical_zone
    response_dict["dateUnit"] = dateUnit
    response_out = json.dumps(response_dict)
    mimetype_out = "application/json"
    if filetype == "csv":
        check = 0
        for pollutant in response_dict["pollutants"]:
            df= pd.DataFrame.from_dict(pollutant["timeline"])
            df=df.rename(columns = {'value':pollutant["pollutant"]+"_value",'normalized':pollutant["pollutant"]+"_normalized"})
            if check == 0:
                df_total = df
                check=1
            else:
                df_total = pd.merge(df_total, df, how='outer', on='time')

        cols = df_total.columns.tolist()
        cols.insert(0, cols.pop(cols.index('time')))
        df_total = df_total.reindex(columns= cols)

        response_out = df_total.to_csv(path_or_buf = None, quoting = csv.QUOTE_ALL)
        mimetype_out = 'text/csv'

    return Response(response=response_out, status=200, mimetype=mimetype_out)


@app.route('/twitts', methods=['GET'])
def twitts():
    city = request.args.get('city_id')
    current_time = datetime.datetime.now()
    update_delta = current_time - app.update_twitts_time
    if update_delta > datetime.timedelta(hours=1):
        app.update_twitts_time = datetime.datetime.now()
        app.twitts = city_twitts.get_cities_tweets(app.accounts)
    if city is None:
        content = app.twitts
    else:
        content = app.twitts[city]
    return Response(response=json.dumps(content), status=200, mimetype="application/json")



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug = "true", threaded="true")

from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.mongorest import MongoRest
from flask.ext.mongorest.views import ResourceView
from flask.ext.mongorest.resources import Resource
from flask.ext.mongorest import operators as ops
from flask.ext.mongorest import methods
import os


app = Flask(__name__)

app.config.update(
    MONGODB_HOST = 'localhost',
    MONGODB_PORT = '27017',
    MONGODB_DB = 'calidad_api',
)

db = MongoEngine(app)
api = MongoRest(app)

class Country(db.Document):
    name = db.StringField()
    id_country = db.StringField()
    longitude = db.StringField()
    latitude = db.StringField()
    timezone = db.StringField()
    level = db.StringField()

class City(db.Document):
    name = db.StringField()
    id_city = db.StringField()
    longitude = db.StringField()
    latitude = db.StringField()
    timezone = db.StringField()
    level = db.StringField()
    id_country = db.StringField()

class Station(db.Document):
    name = db.StringField()
    id_station = db.StringField()
    longitude = db.StringField()
    latitude = db.StringField()
    timezone = db.StringField()
    level = db.StringField()
    id_country = db.StringField()
    id_city = db.StringField()

class Method(db.Document):
    method_id = db.StringField()
    method_shortdescription = db.StringField()
    method_protocol = db.StringField()
    method_device = db.StringField()

class Pollutant(db.Document):
    station_id = db.StringField()
    pollutant_id = db.StringField()
    pollutant_unit = db.StringField()
    pollutant_update_time = db.StringField()
    pollutant_average = db.StringField()
    pollutant_value = db.StringField()


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
        'name': [ops.Exact, ops.Startswith]
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

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug = "true")

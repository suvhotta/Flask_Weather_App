import requests
from weather_app import app, db
from flask import render_template, redirect, url_for, flash
from weather_app.weather_models import City
from weather_app.weather_forms import CityForm


@app.route('/', methods=["GET","POST"])
@app.route('/index', methods=["GET","POST"])
@app.route('/weather', methods=["GET","POST"])
def index():
    form = CityForm()
    if(form.validate_on_submit()):
        api_key ='c6193efad4101a4586db678ce038999c'
        weather_api = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'
        req = requests.get(weather_api.format(form.city_name.data,api_key))
        if(req.status_code !=200):
            flash('No such city found!')
            return(redirect(url_for('index')))
        else:
            city = City(city_name=form.city_name.data.lower())
            db.session.add(city)
            db.session.commit()
            return redirect(url_for('index'))

    api_key ='c6193efad4101a4586db678ce038999c'
    weather_api = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'
    cities = City.query.all()

    weather_data = []
    for city in cities:
        req = requests.get(weather_api.format(city.city_name,api_key)).json()
        weather = {
            'city':city.city_name.upper(),
            'temp':{
                'avg': req['main']['temp'],
                'max_temp' : req['main']['temp_max'],
                'min_temp' : req['main']['temp_min']
            },
            'description': req['weather'][0]['description'],
            'icon': req['weather'][0]['icon']
        }
        weather_data.append(weather)

    return render_template('weather.html',form=form,weather_data=weather_data,title="Weather Info")

@app.route('/remove_city/<city_name>', methods=['POST'])
def remove_city(city_name):
    city = City.query.filter_by(city_name=city_name.lower()).first()
    db.session.delete(city)
    db.session.commit()
    return redirect(url_for('index'))
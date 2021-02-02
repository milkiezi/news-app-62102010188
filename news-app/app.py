from flask import Flask
from flask import render_template
from flask import request
from urllib.parse import quote
from urllib.request import urlopen
from urllib.error import HTTPError
import json

app = Flask(__name__)

OPEN_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&APPID={1}"
OPEN_WEATHER_KEY = 'a9d561e19fec4be03a4e22c9e46e6331'

COVID_API_URL = "https://newsapi.org/v2/top-headlines?q=covid&language=en&sortBy=publishedAt&apiKey={}"
NEWS_API_URL = "https://newsapi.org/v2/top-headlines?q={0}&language=en&sortBy=publishedAt&page=1&apiKey={1}"
NEWS_API_KEY = "cc317c6db7c74135ae93cea33c8b3531"

@app.route("/")
def home():
    city = request.args.get('city')
    if not city:
        city = 'bangkok'
    weather = get_weather(city, OPEN_WEATHER_KEY)
    covid =  get_covidNews(NEWS_API_KEY)

    return render_template("home.html", weather=weather, covid=covid)

@app.route("/news")
def news():
    news = request.args.get('search_news')
    if not news:
        news = 'covid'
    search = search_news(news, NEWS_API_KEY)

    return render_template("news.html", search=search)

@app.route('/about')
def about():
   return render_template('about.html')

def search_news(news,API_KEY):
    try:
        query = quote(news)
        url = NEWS_API_URL.format(news, API_KEY)
        data = urlopen(url).read()
        parsed = json.loads(data)
        search = parsed.get('articles')

        return search
    except:
        return 0

def get_covidNews(API_KEY):
    url = COVID_API_URL.format(API_KEY)
    data = urlopen(url).read()
    parsed = json.loads(data)
    covid = list()

    for i in range(0,5):
        covid.append(parsed['articles'][i])
            
    return covid

def get_weather(city,API_KEY):
    try:
        query = quote(city)
        url = OPEN_WEATHER_URL.format(city, API_KEY)
        data = urlopen(url).read()
        parsed = json.loads(data)
        weather = None

        if parsed.get('weather'):

            temperature = parsed['main']['temp']
            description = parsed['weather'][0]['description']
            pressure = parsed['main']['pressure']
            humidity = parsed['main']['humidity']
            speed = parsed['wind']['speed']
            icon = parsed['weather'][0]['icon']
            city = parsed['name']
            country = parsed['sys']['country']

            weather = {'temperature': temperature,
                        'description': description,
                        'pressure' : pressure,
                        'humidity' :  humidity,
                        'speed' : speed,
                        'icon' : icon,
                        'city': city,
                        'country': country
                       }
        return weather
    except:
        return 0

app.run(debug=True,use_reloader=True)
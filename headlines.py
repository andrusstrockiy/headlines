import feedparser
import json
import datetime
# import urllib
from urllib.parse import quote
from urllib.request import urlopen

from flask import render_template
from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)
DEFAULTS = {
    'publication': 'bbc',
    'city': 'London,UK',
    'currency_from': 'GBP',
    'currency_to': 'USD'
}
RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'
             }

CURENCY_URL = 'https://openexchangerates.org//api/latest.json?' \
              'app_id=9fd61bef46b8416f962a25a6ae728781'


@app.route("/", methods=["GET", "POST"])
def home():
    # get customized headlines based on user input or default
    publication = get_value_with_fallback("publication")
    articles = get_news(publication)
    # get customized weather based on user input or default

    city = get_value_with_fallback('city')
    weather = get_weather(city)
    # get customized currency based on user input or default
    currency_from = get_value_with_fallback("currency_from")
    currency_to = get_value_with_fallback("currency_to")
    rate, currencies = get_rate(currency_from, currency_to)
    response = make_response(render_template("home.html",
                                             articles=articles,
                                             weather=weather,
                                             currency_from=currency_from,
                                             currency_to=currency_to,
                                             rate=rate,
                                             currencies=sorted(currencies)))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    print(expires)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)
    return response

    # return render_template("home.html", articles=articles,
    #                        currency_from=currency_from,
    #                        currency_to=currency_to,
    #                        weather=weather, rate=rate,
    #                        currencies=sorted(currencies))


def get_news(query):
    query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = 'bbc'
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']
    # return render_template("home.html",
    #                        title=first_article.get("title"),
    #                        published=first_article.get("published"),
    #                        summary=first_article.get("summary"))

    # return """<html>
    # <body>
    #     <h1>  Headlines </h1>
    #     <b>{0}</b> <br/>
    #     <i>{1}</i> <br/>
    #     <p>{2}</p> <br/>
    # </body>
    # </html>""".format(first_article.get("title"), first_article.get("published"),
    #                   first_article.get("summary"))
    # return "no news is good news"


def get_weather(query):
    api_url = 'http://api.openweathermap.org/data' \
              '/2.5/weather?q={}&units=metric&appid=8380bca05483be0a8802980db7f2953b'
    query = quote(query)
    url = api_url.format(query)
    data = urlopen(url).read()
    print(data)
    parsed = json.loads(data.decode())
    weather = None
    if parsed.get("weather"):
        weather = {
            "description": parsed["weather"][0]['description'],
            "temperature": parsed['main']['temp'],
            'city': parsed['name'],
            'country': parsed['sys']['country']
        }
    return weather


def get_rate(frm, to):
    all_currency = urlopen(CURENCY_URL).read()
    parsed = json.loads(all_currency.decode()).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return (to_rate / frm_rate, parsed.keys())

def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]



if __name__ == '__main__':
    app.run(port=5000, debug=True)

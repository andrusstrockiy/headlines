import feedparser
from flask import render_template
from flask import Flask
from flask import request


app = Flask(__name__)
RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'
             }


# BBC_FEED = "http://feeds.bbci.co.uk/news/rss.xml"


@app.route("/")
# @app.route("/<publication>")
# def bbc():
#     return get_news('bbc')
#
# @app.route("/cnn")
# def cnn():
#     return get_news('cnn')

def get_news():
    query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = 'bbc'
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    # first_article = feed['entries'][0]
    return render_template("home.html",
                           articles=feed['entries'])
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


if __name__ == '__main__':
    app.run(port=5000, debug=True)

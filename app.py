import feedparser
from flask import Flask, render_template, request, make_response
from flask_socketio import SocketIO, emit
from uuid import uuid4

# Setup flask object
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG'] = True
socketio = SocketIO(app)

feed = feedparser.parse('https://www.abc.net.au/news/feed/51120/rss.xml')

articles = dict()


# Index page route
@app.route("/")
def index():
    sid = request.cookies.get('sid')

    if sid is None:
        resp = make_response(render_template('index.html'))
        resp.set_cookie('sid', str(uuid4()), max_age=600)
        return resp

    return render_template('index.html')


# Index page route
@app.route("/about")
def about():
    return render_template('about.html')


# Socket routes
@socketio.on('next_article')
def handle_message():
    sid = request.cookies.get('sid')

    if sid not in articles:
        articles[sid] = iter(feed.entries)

    article = next(articles[sid])
    emit('article', {'data': article})


if __name__ == '__main__':
    socketio.run(app)
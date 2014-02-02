from flask import Flask, render_template

from config import settings


app = Flask(__name__, template_folder='../../templates',
            static_folder='../../static', static_url_path='/static')


@app.route('/', methods=('GET',))
def home():
    return render_template('home.html', inst_id=settings.INSTAGRAM_CLIENT_ID,
                           tumblr_id=settings.TUMBLR_OAUTH_KEY)

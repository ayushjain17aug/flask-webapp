from flask import Flask, render_template


app = Flask(__name__, template_folder='../../templates',
            static_folder='../../static', static_url_path='/static')


@app.route('/', methods=('GET',))
def home():
    return render_template('home.html')

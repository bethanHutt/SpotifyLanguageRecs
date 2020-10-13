from flask import Flask
from flask import jsonify

from spotify import chart_data_handler
from spotify import chart_requester

import settings

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['FLASK_ENV'] = 'development'


@ app.route('/')
def home():
    return 'Welcome to the Spotify Language Finder'


@ app.route('/get_tracks')
def get_tracks():
    cr = chart_requester.ChartRequester(
        url=settings.CHARTS_URL,
        type='regional',
        region='jp',
        frequency='weekly',
        date='latest')
    csv = cr.make_request()

    dh = chart_data_handler.DataHandler()
    dh.append_data(csv)

    return dh.song_data.to_json()


if __name__ == '__main__':
    app.run()

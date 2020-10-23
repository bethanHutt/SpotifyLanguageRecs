import os
import json

from flask import Flask
from flask import jsonify
from flask import url_for
from flask import render_template

from spotify import chart_data_handler
from spotify import chart_requester

import settings

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['FLASK_ENV'] = 'development'


def get_artists(country_code):
    cr = chart_requester.ChartRequester(
        url=settings.CHARTS_URL,
        type='regional',
        region=country_code,
        frequency='weekly',
        date='latest')
    csv = cr.make_request()

    dh = chart_data_handler.DataHandler()
    dh.append_data(csv)

    return dh.song_data['Artist'].to_dict()


@ app.route('/')
@ app.route('/home')
def home():
    script_path = os.path.dirname(__file__)
    json_path = os.path.join(script_path, 'languages.json')
    with open(json_path) as json_file:
        json_data = json.load(json_file)

    countries = list(json_data.keys())
    return render_template('home.html', countries=countries)


@ app.route('/get_tracks/<string:country>')
def get_tracks(country):
    script_path = os.path.dirname(__file__)
    json_path = os.path.join(script_path, 'languages.json')
    with open(json_path) as json_file:
        json_data = json.load(json_file)

    country_code = json_data[country.title()]
    artists = list(set(get_artists(country_code=country_code).values()))

    return render_template('get_tracks.html', artists=artists, title='Tracks')


if __name__ == '__main__':
    app.run()

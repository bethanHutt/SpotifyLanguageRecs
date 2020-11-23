import os
import json

from flask import Flask
from flask import request
from flask import jsonify
from flask import url_for
from flask import redirect
from flask import render_template

from spotify import chart_data_handler
from spotify import chart_requester

import settings
import forms


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['FLASK_ENV'] = 'development'
# to be put in config module
app.config['SECRET_KEY'] = 'TO_BE_REPLACED'


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


@ app.route('/', methods=['GET', 'POST'])
@ app.route('/home', methods=['GET', 'POST'])
def home():
    # generate list of countries
    script_path = os.path.dirname(__file__)
    json_path = os.path.join(script_path, 'languages.json')
    with open(json_path) as json_file:
        countries = json.load(json_file)

    # create form and supply countries
    form = forms.CountryForm()
    form.country.choices = list(countries.keys())

    if form.validate_on_submit():
        chosen_country = form.country.data
        country_code = countries.get(chosen_country)

        return redirect(url_for('get_tracks', country=country_code))

    return render_template('home.html', form=form)


@ app.route('/get_tracks/<string:country>')
def get_tracks(country):

    artists = list(set(get_artists(country_code=country).values()))

    return render_template('get_tracks.html', artists=artists, title='Tracks')


if __name__ == '__main__':
    app.run()

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


def get_artists():
    cr = chart_requester.ChartRequester(
        url=settings.CHARTS_URL,
        type='regional',
        region='jp',
        frequency='weekly',
        date='latest')
    csv = cr.make_request()

    dh = chart_data_handler.DataHandler()
    dh.append_data(csv)

    return dh.song_data['Artist'].to_dict()


@ app.route('/')
@ app.route('/home')
def home():
    return render_template('home.html')


@ app.route('/test')
def test():
    return render_template('basic.html')


@ app.route('/get_tracks')
def get_tracks():
    artists = list(set(get_artists().values()))
    return render_template('get_tracks.html', artists=artists, title='Tracks')


if __name__ == '__main__':
    app.run()

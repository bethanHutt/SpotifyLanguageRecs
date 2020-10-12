import os
import io
import sys
import pytest
import pandas as pd


ROOTDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path = [ROOTDIR] + sys.path

import settings
from spotify import chart_data_handler as cdhandler
from spotify import chart_requester as spotcharts


@pytest.fixture
def chartrequester():
    chart_requester = spotcharts.ChartRequester(
        url=settings.CHARTS_URL,
        type='regional',
        region='jp',
        frequency='weekly',
        date='latest')

    return chart_requester


@pytest.fixture
def songdata(chartrequester):
    song_data = chartrequester.make_request()

    return song_data


@pytest.fixture
def datahandler():
    data_handler = cdhandler.DataHandler()

    return data_handler


def test_can_init_datahandler(datahandler):
    assert isinstance(datahandler, cdhandler.DataHandler)


def test_datahandler_has_song_data_attr(datahandler):
    assert hasattr(datahandler, 'song_data')


def test_datahandler_song_data_is_empty(datahandler):
    assert datahandler.song_data.empty


def test_song_data_is_pandas_dataframe(datahandler):
    assert isinstance(datahandler.song_data, pd.DataFrame)


def test_append_data_adds_csv_to_song_data(
        chartrequester, datahandler, songdata):
    df = pd.read_csv(io.StringIO(songdata.decode('utf-8')), skiprows=1)
    sample_songs = cdhandler.clean_data(df)

    datahandler.append_data(csv=songdata)

    sample_id = sample_songs.iloc[0]['spotify_id']
    class_id = datahandler.song_data.iloc[0]['spotify_id']
    assert sample_id == class_id


@ pytest.mark.parametrize('bad_headers', ['Position', 'URL', 'Streams'])
def test_clean_data_does_not_have_bad_headers(bad_headers, datahandler, songdata):
    datahandler.append_data(csv=songdata)
    first_result = datahandler.song_data.iloc[0]
    assert bad_headers not in first_result


@ pytest.mark.parametrize('required_headers', ['Artist', 'spotify_id', 'Track Name'])
def test_clean_data_has_good_headers(required_headers, datahandler, songdata):
    datahandler.append_data(csv=songdata)
    first_result = datahandler.song_data.iloc[0]
    assert required_headers in first_result


@ pytest.mark.parametrize('test_url, expected', [
    ('https://open.spotify.com/track/3dPtXHP0oXQ4HCWHsOA9js', '3dPtXHP0oXQ4HCWHsOA9js'),
    ('https://open.spotify.com/track/6F0aYmicNttntvth7FXQEx', '6F0aYmicNttntvth7FXQEx'),
    (None, None),
    ('bad_url', None),
    ('small/url', 'url')])
def test_strip_song_id(test_url, expected):
    assert cdhandler.strip_song_id(url=test_url) == expected

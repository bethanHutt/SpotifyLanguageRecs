import os
import sys

ROOTDIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))
sys.path = [ROOTDIR] + sys.path

import settings

import chart_data_handler as cdhandler
import chart_requester as spotcharts

if __name__ == '__main__':
    chart_requester = spotcharts.ChartRequester(
        url=settings.CHARTS_URL,
        type='regional',
        region='jp',
        frequency='weekly',
        date='latest')

    song_data = chart_requester.make_request()

    data_handler = cdhandler.DataHandler()
    data_handler.append_data(song_data)

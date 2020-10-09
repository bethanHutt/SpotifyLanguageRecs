import os
import sys
import pytest
import requests

ROOTDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path = [ROOTDIR] + sys.path

import settings

from spotify import spotify_charts_requests as spotcharts


@pytest.fixture
def chartrequester():
    chart_requester = spotcharts.ChartRequester(
        url=settings.CHARTS_URL,
        type='regional',
        region='jp',
        frequency='weekly',
        date='latest')

    return chart_requester


def test_chart_requester_object(chartrequester):
    assert isinstance(chartrequester, spotcharts.ChartRequester)


def test_chart_requester_has_url_attr(chartrequester):
    assert hasattr(chartrequester, 'url')


@pytest.mark.parametrize('attrs', ['jp', 'weekly', 'latest'])
def test_attrs_embedded_in_url(attrs, chartrequester):
    assert attrs in chartrequester.url


def test_make_request_returns_response_object(chartrequester):
    response = chartrequester.make_request()
    assert isinstance(response, requests.models.Response)
    assert response.status_code == 200


def test_make_request_returns_good_response(chartrequester):
    response = chartrequester.make_request()
    assert response.status_code == 200


if __name__ == '__main__':
    pass

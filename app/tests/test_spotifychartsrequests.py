import os
import sys
import pytest

ROOTDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path = [ROOTDIR] + sys.path

import settings

from spotify import spotify_charts_requests as spotcharts


@pytest.fixture
def chartrequester():
    chart_requester = spotcharts.ChartRequester(
        url=settings.CHARTS_URL,
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


if __name__ == '__main__':
    pass

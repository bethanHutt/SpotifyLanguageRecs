import requests


class ChartRequester(object):
    def __init__(self, url, type, region, frequency, date):
        self.url = url.format(
            type=type,
            region=region,
            frequency=frequency,
            date=date)

    def make_request(self):
        session = requests.session()
        response = session.get(self.url)

        if test_response_validity(response=response):
            return response.content

        return None


def test_response_validity(response):
    if not response.status_code == 200:
        return False

    if not response.content:
        return False

    if response.headers['Content-Type'] == 'text/html; charset=UTF-8':
        return False

    return True



class ChartRequester(object):
    def __init__(self, url, region, frequency, date):
        self.url = url.format(
            region=region,
            frequency=frequency,
            date=date)

    def make_request(self):
        pass

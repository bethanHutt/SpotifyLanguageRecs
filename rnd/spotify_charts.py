import io
import requests
import pandas as pd

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


REGION = 'jp'
URL = 'https://spotifycharts.com/regional/{}/daily/latest/download'.format(
    REGION)


def make_request(url, size=200):
    headers = {
        'Host': 'spotifycharts.com',
        'User-Agent': 'Mozilla/5.0'
    }

    retries = Retry(total=10, backoff_factor=2,
                    status_forcelist=[500, 502, 503, 504, 404])

    s = requests.Session()
    s.mount("https://", HTTPAdapter(max_retries=retries))
    res = s.get(url, headers=headers, timeout=3)

    if not res.status_code == 200:
        print('Error getting info')
        return

    if(res.headers["Content-Type"] == "text/html; charset=UTF-8"):
        return

    data = res.content

    df = pd.read_csv(io.StringIO(
        data.decode("utf-8")), skiprows=1)

    df["spotify_id"] = df["URL"].apply(lambda x: strip_song_id(x))
    df.drop(["Position"], axis=1, inplace=True)
    df.drop(["URL"], axis=1, inplace=True)
    df.drop(["Streams"], axis=1, inplace=True)

    return df


def strip_song_id(url):
    return url.split('/')[-1]


if __name__ == '__main__':
    df = (make_request(url=URL))
    # print(df.columns)
    print(df['Artist'].head(20))

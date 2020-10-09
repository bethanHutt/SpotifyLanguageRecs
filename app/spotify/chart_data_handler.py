import io
import pandas as pd


class DataHandler():
    def __init__(self):
        self.song_data = pd.DataFrame()

    def append_data(self, csv):
        df = pd.read_csv(io.StringIO(csv.decode("utf-8")), skiprows=1)

        df = clean_data(df=df)

        self.song_data.append(df)


def clean_data(df):
    df["spotify_id"] = df["URL"].apply(lambda x: strip_song_id(x))
    df.drop(["Position"], axis=1, inplace=True)
    df.drop(["URL"], axis=1, inplace=True)
    df.drop(["Streams"], axis=1, inplace=True)

    return df


def strip_song_id(url):
    return url.split('/')[-1]

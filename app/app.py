from flask import Flask

app = Flask(__name__)


@ app.route('/')
def home():
    return 'Welcome to the Spotify Language Finder'


if __name__ == '__main__':
    app.run()

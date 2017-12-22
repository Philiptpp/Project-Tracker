import sys
from flask import Flask
import api
import configuration


app = Flask(__name__)
api.init(app)

@app.route('/')
def index():
    return 'Hello world!'


if __name__ == '__main__':
    app.config.from_object(configuration.Production)
    if len(sys.argv) > 1:
        if sys.argv[1].lower() in ['development', 'dev']:
            app.config.from_object(configuration.Development)
    app.run()

import sys
from flask import Flask

import v1
import database
import configuration

app = Flask(__name__)

if __name__ == '__main__':
    app.config.from_object(configuration.Production)
    if len(sys.argv) > 1:
        if sys.argv[1].lower() in ['development', 'dev']:
            app.config.from_object(configuration.Development)
    database.initialize(app)
    v1.initialize(app)
    app.run()

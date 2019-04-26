import os
from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.config.from_object(__name__)

app.config.update(
    dict(
        SECRET_KEY='BFH',
        DATABASE=os.path.join(app.root_path, 'data', 'database', 'business_finance_helper.db'),
        MAX_CONTENT_LENGTH=50 * 1024 * 1024))

bootstrap = Bootstrap(app)

import logging
import os
import uuid

from flask import Flask, render_template, request, session
from werkzeug.utils import send_file
from flask_sqlalchemy import SQLAlchemy

# Flask setup
app = Flask(__name__)
app.config.from_pyfile('config.py')

# SQLite setup
db = SQLAlchemy(app)


class CSSAttribute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    attribute = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"CSSAttribute({self.session_id}, {self.attribute}, {self.value})"


# Logging setup
logging.basicConfig(level=app.config['LOGGING_LEVEL'])
logger = logging.getLogger(__name__)


# todo implementacja wszystkich funkcji https://browserstrangeness.bitbucket.io/css_hacks.html
# zrobie tak że wszystkie te funkcje zaimplementuje i przetestuje wszystkie obecne buildy przegladarek pod to

@app.before_request
def make_session_permanent():
    session.permanent = True
    if 'session_id' not in session:
        session['session_id'] = uuid.uuid4()


def add_attribute(attribute, value):
    if not 'session_id' in session:
        logger.error(f"Could not save attribute {attribute} in database, because there is no session id")
        return

    attribute = CSSAttribute(session_id=str(session['session_id']), attribute=attribute, value=value)
    db.session.add(attribute)
    db.session.commit()


@app.route('/')
def home():
    # save user agent to the sqlite database
    add_attribute('User-Agent', request.headers.get('User-Agent'))
    logger.debug(f"User-Agent: {request.headers.get('User-Agent')}")

    return render_template('index.html')


@app.route('/fingerprint', methods=['GET'])
def fingerprint():
    attributes = {key: value for key, value in request.args.items()}

    for attr_name, attr_value in attributes.items():
        add_attribute(attr_name, attr_value)

    image_path = os.path.join('images', 'green.png')
    return send_file(image_path, mimetype='image/png', environ=request.environ)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", debug=True)

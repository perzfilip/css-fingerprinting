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

def add_attribute(attribute, value):
    if not 'session_id' in session:
        logger.error(f"Could not save attribute {attribute} in database, because there is no session id")
        return

    attribute = CSSAttribute(session_id=str(session['session_id']), attribute=attribute, value=value)
    db.session.add(attribute)
    db.session.commit()

@app.route('/')
def home():
    # generate session cookie
    if 'session_id' not in session:
        session['session_id'] = uuid.uuid4()

    # save user agent to the sqlite database
    add_attribute('User-Agent', request.headers.get('User-Agent'))
    logger.debug(f"User-Agent: {request.headers.get('User-Agent')}")

    return render_template('index.html')


@app.route('/viewport', methods=['GET'])
def viewport():
    param = request.args.get('param', type=str)

    # validation
    if len(param) != 4 or not param.isdigit():
        return 'Invalid parameter', 400

    x = int(param[:2]) * 100
    y = int(param[2:]) * 100

    if 'session_id' in session:
        logger.debug(f"Viewport width: {x}-{y}px, Session cookie: {session['session_id']}")
    else:
        logger.debug("Session cookie not set")

    # save info to the sqlite database
    add_attribute("viewport_width", x)
    add_attribute("viewport_height", y)

        
    image_path = os.path.join('images', 'white.png')
    return send_file(image_path, mimetype='image/png', environ=request.environ)

@app.route('/image-set', methods=['GET'])
def image_set():
    px_per_px = request.args.get('px_per_px', type=int)
    is_safari = request.args.get('is_safari', type=int)

    if px_per_px:
        print(f"Pixels per CSS pixel: {px_per_px}")

    if is_safari is not None:
        if is_safari:
            print("Is Safari")
        else:
            print("Not Safari")

    image_path = os.path.join('images', 'white.png')
    return send_file(image_path, mimetype='image/png', environ=request.environ)

@app.route('/microsoft-office', methods=['GET'])
def microsoft_office():
    param = request.args.get('param', type=int)

    if param is not None:
        if param:
            print("Microsoft Office is installed")
        else:
            print("Microsoft Office is not installed")

    image_path = os.path.join('images', 'white.png')
    return send_file(image_path, mimetype='image/png', environ=request.environ)

@app.route('/os-identification', methods=['GET'])
def os_identification():
    param = request.args.get('param', type=str)

    if param == "ubuntu":
        print("Ubuntu")

    if param == "windows":
        print("Windows")

    image_path = os.path.join('images', 'white.png')
    return send_file(image_path, mimetype='image/png', environ=request.environ)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0",debug=True)

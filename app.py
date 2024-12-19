import os

from flask import Flask, render_template, request
from werkzeug.utils import send_file

app = Flask(__name__)

# todo implementacja wszystkich funkcji https://browserstrangeness.bitbucket.io/css_hacks.html
# zrobie tak że wszystkie te funkcje zaimplementuje i przetestuje wszystkie obecne buildy przegladarek pod to

def decode_param(param):
    x = int(param[:2]) * 100
    y = int(param[2:]) * 100
    print(f"Viewport width: {x}-{y}px")
@app.route('/')
def home():
    # get user agent
    user_agent = request.headers.get('User-Agent')
    print(f"User agent: {user_agent}")

    return render_template('index.html')

@app.route('/viewport', methods=['GET'])
def viewport():
    param = request.args.get('param', type=str)

    # validation
    if len(param) != 4 or not param.isdigit():
        return 'Invalid parameter', 400

    decode_param(param)

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
    app.run(host="0.0.0.0",debug=True)

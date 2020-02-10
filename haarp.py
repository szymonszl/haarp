from flask import (
    Flask,
    request,
    url_for,
    render_template,
    Response,
    abort
)
from io import BytesIO
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def handle_404(e):
    return render_template('404.html'), 404

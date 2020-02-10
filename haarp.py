from flask import (
    Flask,
    request,
    render_template,
    Response,
    abort,
    redirect,
    send_file,
)
import configparser
import os
import glob
import subprocess
app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

HOMEDIR = config['source']['path']
supported = ['mp3', 'flac', 'm4a', 'webm', 'wav', 'wma']
FFMPEGARGS = config['ffmpeg']['args'].split()

def getlisting(path):
    files = []
    for f in os.listdir(path):
        if f[0] != '.':
            if os.path.isdir(os.path.join(path, f)):
                files.append(f)
            s = f.split('.')
            if s[-1] in supported:
                files.append('.'.join(s[:-1]+['mp3']))
    files.append('..')
    files.sort()
    return render_template('index.html', path=path, files=files)

def makemp3(path):
    ffmpeg = subprocess.Popen(
        [
            'ffmpeg',
            '-i',
            path,
            '-c:a',
            'libmp3lame',
            '-f',
            'mp3',
            '-vn',
            *FFMPEGARGS,
            '-'
        ],
        stdout=subprocess.PIPE
    )

    return send_file(ffmpeg.stdout, mimetype='audio/mpeg')
    #return Response(iter(ffmpeg.stdout.read, b''), mimetype='audio/mpeg')

@app.route('/')
@app.route('/<path:path>')
def index(path=''):
    reqpath = os.path.normpath(os.path.join(HOMEDIR, path))
    if os.path.commonprefix([reqpath, HOMEDIR]) != HOMEDIR:
        abort(403)
    if os.path.isdir(reqpath):
        if path and path[-1] != '/':
            return redirect('/' + path + '/')
        return getlisting(reqpath)
    if reqpath.endswith('.mp3'):
        actualreqpath = glob.glob(reqpath[:-3]+'*') # oh god
        if actualreqpath:
            return makemp3(actualreqpath[0])
        abort(404)
    #return send_file(reqpath)
    abort(404)
    raise Exception(f'how p{path!r} r{reqpath!r} h{HOMEDIR!r}')

@app.errorhandler(404)
def handle_404(e):
    return render_template('404.html'), 404

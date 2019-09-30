import os, sys
from flask import Flask, request, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

reload(sys)
sys.setdefaultencoding('utf8')
video_dir = 'static/video/'

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route('/')
@app.route('/home')
def index():
    video_files = [f for f in os.listdir(video_dir)]
    video_files_number = len(video_files)
    return render_template("index.html", title='Home', video_files_number=video_files_number, video_files=video_files)
@app.route('/<filename>')
def video(filename):
    return render_template('play.html', title=filename, video_file=filename)
@app.route('/test')
def test():
    return render_template('test.html')
import models #circular imports


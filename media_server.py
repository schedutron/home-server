import os, sys
from flask import Flask, request, render_template
from config import Config
#from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
from globalimports import *
from models import Video

reload(sys)
sys.setdefaultencoding('utf8')
video_dir = 'static/video/'

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
@app.route('/home')
def index():
    video_files = get_db("filename")
    likes = get_db("likes")
    video_files_number = len(video_files)     
    return render_template("index.html", title='Home', video_files_number=video_files_number, video_files=video_files, likes=likes)

@app.route('/', methods=['POST'])
def update_db():
    video_files = [f for f in os.listdir(video_dir)]
    filenames_in_db = get_db("filename")
    
    #add files-db
    for f in set(video_files)-set(filenames_in_db):
        vid = Video(filename=f)
        db.session.add(vid)       
    #remove db-files    
    for f in set(filenames_in_db)-set(video_files):
        vid = Video.query.filter_by(filename=f).first()
        db.session.delete(vid)
    
    db.session.commit()
    return index()   

@app.route('/<filename>')
def video(filename):
    return render_template('play.html', title=filename, video_file=filename)

@app.route('/<filename>', methods=['POST'])
def update_likes(filename):
    if request.form['data'] == 'plus':
        incrementlike(filename)
    elif request.form['data'] == 'minus':
        decrementlike(filename)
    return video(filename)

@app.route('/test')
def test():
    print_db()
    return render_template('test.html')

def changelike(f):
    def inner(filename):   
        vid = Video.query.filter_by(filename=filename).first()
        vid.likes += f(filename)
        db.session.commit() #possibly this can be done when returning in homepage
        return video(filename)
    return inner

@changelike
def incrementlike(filename):
    return +1;

@changelike    
def decrementlike(filename): 
    return -1;

def get_db(attr):
    vidobj = Video.query.order_by(Video.filename).all()
    attrlist = [str(getattr(o, attr)) for o in vidobj]
    return attrlist

def print_db():
    obj_in_db = Video.query.order_by(Video.filename).all()
    for f in obj_in_db:
        print(f.likes)    


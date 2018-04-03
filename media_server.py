import os, sys
# from importlib import reload
from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit, send

debug = True
video_dir = 'static/video/'
app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
@app.route('/home')
def index():
    video_files = [f for f in os.listdir(video_dir)]
    # video_files_number = len(video_files)
    return render_template("index.html", title='Home', video_files=video_files, video_dir=video_dir)
    
@app.route('/<filename>')
def video(filename):
    return render_template('play.html', title=filename[:-4], video_file=filename, video_dir=video_dir)

@app.route('/lazy')
def lazy():
    video_files = [f for f in os.listdir(video_dir)]
    return render_template('lazy.html', video_files=video_files)

@app.route('/test')
def test():
    return render_template('test.html')

# When remote/lazy mode connects to server
@socketio.on('connect')
def connect():
    print("Client connected")

# When remote sends a command, handle them here.
@socketio.on('remote')
def remote(data):
    cmd = data['cmd']

    # show in browser console that command was received
    emit('cmdlog', {'data': cmd}, broadcast=True)

    if cmd == "fullscreen":
        # show in terminal that command was received
        print("you clicked fullscreen")
        # finally send actual command to browser
        emit(cmd, broadcast=True)
    elif cmd == "browser_back":
        emit(cmd, broadcast=True)
    elif cmd == "browser_forward":
        emit(cmd, broadcast=True)
    elif cmd == "play_movie":
        # data["movie"]="test"
        # movie={"filename":"atest"}
        # print(data['movie'])
        movie = data['movie']
        emit(cmd, movie, broadcast=True)
    elif cmd == "night_mode":
        emit(cmd, broadcast=True)
    else:
        print("I don't know this command!")

if __name__ == '__main__':
    if debug:
        socketio.run(app, debug=True)
    else:
        socketio.run(app, host="0.0.0.0", port=5000)
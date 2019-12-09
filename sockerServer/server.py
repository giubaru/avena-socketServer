import flask, flask_socketio

app =  flask.Flask(__name__)

app.config['SECRET_KEY'] = 'ch0c0c0c0'
sio = flask_socketio.SocketIO(app)

sio.init_app(app, cors_allowed_origins="*")


@sio.on('connect')
def client_connect():
    print('Client connected !')
    sio.emit('chuleta', '')

@sio.on('file')
def handle_file(file):
    with open(file['name'], 'wb') as file_b:
        file_b.write(file['data'])
    sio.emit('file-server', {'resp':'done'})


@sio.on('add2Queue')
def handle_queue(file_name):
    
    print('Adding to queue:', file_name)
    sio.emit('chuleta', file_name)

if __name__ == '__main__':
    sio.run(app, host='0.0.0.0')

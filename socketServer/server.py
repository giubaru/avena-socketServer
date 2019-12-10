import flask, flask_socketio, pymongo, datetime
 

myclient = pymongo.MongoClient("mongodb://mongoadmin:secret@localhost:27017/")

mydb = myclient["mydatabase"]

mycol = mydb["squeuesass"]



# print([i for i in mycol.find({'state':'running'}).sort('date', -1)])

app =  flask.Flask(__name__)

app.config['SECRET_KEY'] = 'ch0c0c0c0'
sio = flask_socketio.SocketIO(app)

sio.init_app(app, cors_allowed_origins="*")


@sio.on('connect')
def client_connect():
    print('Client connected !')
    cache = [i for i in mycol.find({'state':'ready'})]
    if cache == []:
        noti = ''
    else:
        noti = cache[0]['script']

    sio.emit('chuleta', noti)

@sio.on('file')
def handle_file(file):
    with open(f'./storage/{file["name"]}', 'wb') as file_b:
        file_b.write(file['data'])
    sio.emit('file-server', {'resp':'done'})


@sio.on('add2Queue')
def handle_queue(file_name):
    state = 'pending'
    if [i for i in mycol.find({'state':'running'}).sort('date', -1)] == []:
        state = 'ready'
    
    data = {'script':file_name, 'date':datetime.datetime.now().timestamp(), 'state':state}
    mycol.insert_one(data)
    print('Adding to queue:', file_name)
    sio.emit('chuleta', file_name)

if __name__ == '__main__':
    sio.run(app, host='0.0.0.0', debug=True)

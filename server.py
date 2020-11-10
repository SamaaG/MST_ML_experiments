import socket
import pickle
import pickledb

def process(op, db):
    if type(op) == type(dict()):
        return write(op, db)
    elif type(op) == type(str()):
        return read(op, db)
    else:
      return 'error'

def read(op, db):
    return db[op]

def write(op, db):
    for k in op:
        db.set(k, op[k])
    return 'done writing'

def server(db):

  port = 65008
  host = '172.31.34.93'

  s = socket.socket()
  s.bind((host, port))

  print(f'Listening on port {port}..')
  s.listen(1)
  print('Waiting..')

  client_socket, adress = s.accept()
  print("Connection from: " + str(adress))


  while True:
    try:
        data = pickle.loads(client_socket.recv(1024))
    except:
        print('no more data to recieve')
        break
    print('From online user: ', data)
    print("working on it...")
    reply = process(data, db)
    print('this is my reply to the user:', reply)
    d = pickle.dumps(reply)
    client_socket.send(d)
    print("done")
  client_socket.close()

if __name__ == '__main__':
  db = pickledb.load('MyDB.db', True)
  server(db)
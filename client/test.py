from comm import Comm

print('preinit')
comm = Comm()
comm.conn.connect()
print('postinit')
comm.conn.data_ready()
print('dataready')
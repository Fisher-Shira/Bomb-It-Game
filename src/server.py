from socket import socket
from select import select

ENCODING = 'utf-8'
IP = '0.0.0.0'
PORT = 1729


def send_waiting_messages(wlist):
    for message in messages_to_send:
        (client_socket, data) = message
        if client_socket in wlist:
            client_socket.send(str(data).encode(ENCODING))
            messages_to_send.remove(message)


def main():
    server_socket = socket()
    server_socket.bind((IP, PORT))
    server_socket.listen(4)
    players_sockets = {}  # socket : player_color
    global messages_to_send
    messages_to_send = []
    act = ''
    while True:
        rlist, wlist, xlist = select([server_socket]
                                     + list(players_sockets.keys()),
                                     list(players_sockets.keys()), [])
        for current_socket in rlist:
            # add the new socket
            if current_socket is server_socket:
                (new_socket, address) = server_socket.accept()
                players_sockets[new_socket] = ""
            else:
                send = True
                data = current_socket.recv(1024).decode(ENCODING)
                if data != '':
                    list_data = data.split()
                    if list_data[0] == "color":
                        # someone chose color
                        players_sockets[current_socket] = list_data[1]
                        act = '0' + str(len(list_data[1])) + list_data[1]
                    elif list_data[0] == "move" or list_data[0] == "heart" \
                            or list_data[0] == "bomb":
                        # someone move/ someone get heart/ someone put bomb
                        if len(data) < 10:
                            act = '0' + str(len(data)) + data
                        else:
                            act = str(len(data)) + data
                        messages_to_send.append((current_socket, act))
                    elif list_data[0] == "quit":
                        # someone left
                        if data == "quit":
                            send = False
                        else:
                            if len(data) < 10:
                                act = '0' + str(len(data)) + data
                            else:
                                act = str(len(data)) + data
                        players_sockets.pop(current_socket)
                    if send:
                        for this_socket in wlist:
                            if this_socket is not current_socket:
                                messages_to_send.append((this_socket, act))

        send_waiting_messages(wlist)


if __name__ == '__main__':
    main()

# from gameGrid import BoardGame
import uuid
import socket
import player
from _thread import *
import threading
import time
import json

# dictionary of all users
# key = playerID
# value = player object, socket (addr)
Users = {}

# dictionary of all of the game IDs to game objects
# key = gameID
# value = [player1_id, player2_id]
OngoingGames = {}

# dictionary of all of the games with only one person there
# key = gameID
# value = playerID
WaitingGames = {}


def handle_client_thread(c):
    while True:
        client_msg = c.recv(1024).decode('utf-8', 'ignore')
        if client_msg == "NEW":
            print(client_msg)
            new_player = uuid.uuid1()
            new_player = str(new_player)
            print("New player: " + new_player)
            c.send(new_player.encode())
            Users[new_player] = c
            print()
        elif "CREATE" in client_msg:
            print(client_msg)
            new_game_id = str(uuid.uuid1())
            player_id = client_msg.split()[1]
            WaitingGames[new_game_id] = player_id
            print(new_game_id + " created for " + player_id)
            print(WaitingGames)
            print()
        elif "JOIN" in client_msg:
            print(client_msg)
            split_msg = client_msg.split()
            requested_game_id = split_msg[2]
            if requested_game_id in WaitingGames:
                other_player_id = WaitingGames[requested_game_id]
                OngoingGames[requested_game_id] = [other_player_id, split_msg[1]]
                del WaitingGames[requested_game_id]
                print(OngoingGames)
                create_msg = "JOINED " + requested_game_id
                c.send(create_msg.encode())

                Users[other_player_id].send(create_msg.encode())
            else:
                c.send("FAIL".encode())
            print("jointastic")
            print()
        elif "LIST" in client_msg:
            print(client_msg)
            c.send(json.dumps(WaitingGames).encode('utf-8', 'ignore'))
            print()
        elif "MSG" in client_msg:
            print(client_msg)
            split_msg = client_msg.split()
            sender_id = split_msg[1]
            game = OngoingGames[split_msg[2]]
            opponent_id = ""
            if game[0] == sender_id:
                opponent_id = game[1]
            else:
                opponent_id = game[0]

            Users[opponent_id].send(client_msg.encode())
            print()

        client_msg = ""
    c.close()


# doesn't do anything right now except set up server
s = socket.socket()
host = socket.gethostname()
port = 14123
s.bind((host, port))
s.listen(10)
print("Server is on!")
while True:
    c, addr = s.accept()
    print(c)
    print("Connection made with ", end="")
    print(addr)
    start_new_thread(handle_client_thread, (c,))
s.close()


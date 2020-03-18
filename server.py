# from gameGrid import BoardGame
import uuid
import socket
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
    c_player_id = ""
    c_game_id = ""
    while True:
        try:
            client_msg = c.recv(1024).decode('utf-8', 'ignore')
        except:
            client_msg = ""
        if "NEW" in client_msg:
            print(client_msg)
            split_new = client_msg.split()
            req_name = split_new[1]

            if req_name in Users:
                c.send("FAIL".encode())
            else:
                new_player = split_new[1]
                confirm_msg = "CONFIRMED " + new_player
                print("New player: " + new_player)
                c.send(confirm_msg.encode())
                Users[new_player] = c
                c_player_id = new_player
                print()
        elif "CREATE" in client_msg:
            print(client_msg)
            new_game_id = str(uuid.uuid1())
            player_id = client_msg.split()[1]
            WaitingGames[new_game_id] = player_id
            print(new_game_id + " created for " + player_id)
            c_game_id = new_game_id
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
                c_game_id = requested_game_id
                Users[other_player_id].send(create_msg.encode())
            else:
                c.send("FAIL".encode())
            print("jointastic")
            print()
        elif "LIST" in client_msg:
            print(client_msg)
            c.send(json.dumps(WaitingGames).encode('utf-8', 'ignore'))
            print()
        elif client_msg == "":
            if c_game_id == "" and c_player_id == "":
                c.close()
                break
            elif c_game_id == "":
                del Users[c_player_id]
                c.close()
                break
            else:
                if c_game_id in WaitingGames:
                    del WaitingGames[c_game_id]
                    del Users[c_player_id]
                    c.close()
                    break
                else:
                    game = OngoingGames[c_game_id]
                    opponent_id = ""
                    if game[0] == c_player_id:
                        opponent_id = game[1]
                    else:
                        opponent_id = game[0]
                    end_msg = "END SERVER " + c_game_id
                    Users[opponent_id].send(end_msg.encode())
                    del OngoingGames[c_game_id]
                    del Users[c_player_id]
                    del Users[opponent_id]
                    c.close()
                    break
        else:
            print("================")
            print(client_msg)
            split_msg = client_msg.split()
            sender_id = split_msg[1]
            print("SENDER: " + sender_id)
            game = OngoingGames[split_msg[2]]
            print("GAME: " + str(game))
            opponent_id = ""
            if game[0] == sender_id:
                opponent_id = game[1]
            else:
                opponent_id = game[0]
            print("OPPONENT: " + opponent_id)

            Users[opponent_id].send(client_msg.encode())
            if "END" in client_msg:
                Users[sender_id].send(client_msg.encode())
                del Users[sender_id]
                del Users[opponent_id]
                del OngoingGames[split_msg[2]]
            print()

        client_msg = ""
    c.close()


# doesn't do anything right now except set up server
s = socket.socket()
host = socket.gethostname()
port = 6010
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


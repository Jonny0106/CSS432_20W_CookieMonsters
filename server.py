from gameGrid import BoardGame
import uuid
import socket
import player

# dictionary of all users
# key = playerID
# value = player object
Users = {}

# dictionary of all of the game IDs to game objects
# key = gameID
# value = gameGrid object
OngoingGames = {}

# dictionary of all of the games with only one person there
# key = gameID
# value = playerID
WaitingGames = {}

def add_new_user():
    player_id = uuid.uuid1()
    new_player = player.Player(player_id)
    Users[player_id] = new_player
    return player_id

def create_new_game(player_id):
    player = Users[player_id]
    game_id = uuid.uuid1()
    if player is not None:
        player.gameID = game_id
        player.firstTurn = True
        WaitingGames[game_id] = player_id
        return True
    return False

def join_game(player_id, game_id):
    first_player_id = WaitingGames[game_id]
    incoming_player = Users[player_id]
    if first_player_id is not None and incoming_player is not None:
        first_player = Users[first_player_id]
        incoming_player.gameID = game_id
        incoming_player.firstTurn = False

        # need to signal to each to player to make the grid
        # will need the IP address to send just to the one that needs to do it
        # first_player.makeGrid(AMOUNT)
        # incoming_player.makeGrid(AMOUNT)
        return True
    return False

# doesn't do anything right now except set up server
s = socket.socket()
host = socket.gethostname()
port = 14123
s.bind((host, port))
s.listen(5)
while True:
    c, addr = s.accept()
    print("Connection made with " + addr)
    c.send("Connected")
    c.close()


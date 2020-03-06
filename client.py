import socket

s = socket.socket()
host = socket.gethostname()
port = 14123

s.connect((host, port))
# upon connecting to server, get the player_id
player_id = "0-0"

print("Welcome to Team Cookie Monsters' Battleship Game!")

def ask_for_choice():
    print("Please enter a 'j' to list all of the possible games to join or a 'c' to create a new game: " , end="")
    choice = input()

    while choice != 'j' or choice != 'c':
        print("'j' or 'c' was not entered. Enter 'j' to join a game or 'c' to create a game: ", end="")
        choice = input()

    act_on_choice(choice)

def act_on_choice(choice):
    if choice == 'j':
        print("Here are a list of games you can join:")
        # request dictionary of WaitingGames from server
        # print out each game_id and player_id

        print("Please enter in the game_id of the game you would like to join.")
        print("If there are no games you would like to join, enter 'c' to create a new game: ", end="")
        choice = input()

    if choice == 'c':
        print("Starting new game!")
        # tell server to create a new game (send player_id)
    else:
        print("Joining game")
        # tell server to join a new game (send game_id and player_id)
        # open the gamegrid and send back and forth the coordinates of hits and misses

s.close()
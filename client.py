import socket
import json

print("Welcome to Team Cookie Monsters' Battleship Game!")
s = socket.socket()
host = socket.gethostname()
port = 14123
s.connect((host, port))

# upon connecting to server, get the player_id
request_player_id = "NEW"
s.send(request_player_id.encode())
rec = s.recv(1024)
player_id = str(rec.decode('utf-8', 'ignore'))

print("Connection established with server!")
print("Your player ID is: " + player_id)


def ask_for_choice():
    print("Please enter a 'j' to list all of the possible games to join or a 'c' to create a new game: " , end="")
    choice = input()

    while True:
        if choice == "j" or choice == "c":
            act_on_choice(choice)
            break;
        else:
            print("'j' or 'c' was not entered. Enter 'j' to join a game or 'c' to create a game: ", end="")
            choice = input()


def print_waiting_games(string_of_dict):
    dict_of_waiting_games = json.loads(string_of_dict)
    if not dict_of_waiting_games:
        print("No one is waiting. Please create a new game.")
    else:
        for game_id in dict_of_waiting_games:
            print("Game ID: " + game_id + " Player ID: " + dict_of_waiting_games[game_id])


def act_on_choice(choice):
    if choice == "j":
        print()
        print("Here are a list of games you can join:")
        # request dictionary of WaitingGames from server
        create_msg = "LIST " + player_id
        s.send(create_msg.encode())

        # print out each game_id and player_id
        string_of_dict = s.recv(1024).decode('utf-8', 'ignore')
        print_waiting_games(string_of_dict)

        print("Please enter in the game_id of the game you would like to join.")
        print("If there are no games you would like to join, enter 'c' to create a new game: ", end="")
        act_on_choice(input())
    elif choice == "c":
        print()
        print("Creating new game...")
        # tell server to create a new game (send player_id)
        create_msg = "CREATE " + player_id
        s.send(create_msg.encode())
        print("Game has been created. Please wait for another player to join...")
        create_start_response = s.recv(1024).decode('utf-8', 'ignore')
        if create_start_response == "JOINED":
            print("Successfully joined game!")
            # open the gamegrid and send back and forth the coordinates of hits and misses
    elif choice != "":
        print("Joining game...")
        # tell server to join a new game (send game_id and player_id)
        # in this case, choice is the game_id
        create_msg = "JOIN " + player_id + " " + choice
        s.send(create_msg.encode())
        join_response = s.recv(1024).decode('utf-8', 'ignore')
        if join_response == "JOINED":
            print("Successfully joined game!")
            # open the gamegrid and send back and forth the coordinates of hits and misses
        else:
            print("Could not join game. Please make sure to enter in the correct game ID (no quotes).")
            print()
            ask_for_choice()
    else:
        print()
        print("You have not entered anything. Let's start over.")
        ask_for_choice()


ask_for_choice()

s.close()

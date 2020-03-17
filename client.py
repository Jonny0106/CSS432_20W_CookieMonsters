import socket
import json


class Client:
    def __init__(self):
        print("Welcome to Team Cookie Monsters' Battleship Game!")
        self.s = socket.socket()
        # self.host = "10.155.176.29"
        self.host = socket.gethostname()
        self.port = 6010
        self.s.connect((self.host, self.port))
        self.goFirst = False

        # upon connecting to server, get the player_id
        self.request_player_id = "NEW"
        self.s.send(self.request_player_id.encode())
        self.rec = self.s.recv(1024)
        self.player_id = str(self.rec.decode('utf-8', 'ignore'))
        self.game_id = ""
        print("Connection established with server!")
        print("Your player ID is: " + self.player_id)
        self.ask_for_choice()

    def ask_for_choice(self):
        print("Please enter a 'j' to list all of the possible games to join or a 'c' to create a new game: ", end="")
        choice = input()

        while True:
            if choice == "j" or choice == "c":
                self.act_on_choice(choice)
                break
            else:
                print("'j' or 'c' was not entered. Enter 'j' to join a game or 'c' to create a game: ", end="")
                choice = input()

    def print_waiting_games(self, string_of_dict):
        dict_of_waiting_games = json.loads(string_of_dict)
        if not dict_of_waiting_games:
            print("No one is waiting. Please create a new game.")
        else:
            for game_id in dict_of_waiting_games:
                print("Game ID: " + game_id + " Player ID: " + dict_of_waiting_games[game_id])

    # start game once both players have joined
    def start_game(self, given_game_id):
        hello_msg = "MSG " + self.player_id + " " + given_game_id + " Hello this is your opponent, " + self.player_id + " on game " + given_game_id
        print("-sending-" + hello_msg)
        self.s.send(hello_msg.encode())
        hello_response = self.s.recv(1024).decode('utf-8', 'ignore')
        print(hello_response)

    def act_on_choice(self, choice):
        if choice == "j":
            print()
            print("Here are a list of games you can join:")
            # request dictionary of WaitingGames from server
            create_msg = "LIST " + self.player_id
            self.s.send(create_msg.encode())

            # print out each game_id and player_id
            string_of_dict = self.s.recv(1024).decode('utf-8', 'ignore')
            self.print_waiting_games(string_of_dict)

            print("Please enter in the Game ID of the game you would like to join.")
            print("If there are no games you would like to join, enter 'c' to create a new game: ", end="")
            self.act_on_choice(input())
        elif choice == "c":
            print()
            print("Creating new game...")
            # tell server to create a new game (send player_id)
            create_msg = "CREATE " + self.player_id
            self.s.send(create_msg.encode())
            print("Game has been created. Please wait for another player to join...")
            self.goFirst = True
            create_start_response = self.s.recv(1024).decode('utf-8', 'ignore')
            if "JOINED" in create_start_response:
                print("Successfully joined game!")
                self.game_id = create_start_response.split()[1]
                print(self.game_id)
                # open the gamegrid and send back and forth the coordinates of hits and misses
                self.start_game(self.game_id)
        elif choice != "":
            print("Joining game...")
            # tell server to join a new game (send game_id and player_id)
            # in this case, choice is the game_id
            create_msg = "JOIN " + self.player_id + " " + choice
            self.s.send(create_msg.encode())
            join_response = self.s.recv(1024).decode('utf-8', 'ignore')
            if "JOINED" in join_response:
                print("Successfully joined game!")
                self.game_id = join_response.split()[1]
                print(self.game_id)

                # open the gamegrid and send back and forth the coordinates of hits and misses
                self.start_game(self.game_id)
            else:
                print("Could not join game. Please make sure to enter in the correct game ID (no quotes).")
                print()
                self.ask_for_choice()
        else:
            print()
            print("You have not entered anything. Let's start over.")
            self.ask_for_choice()

    def sendMessage(self, message):
        print("sending Guess: " + message)
        # send message out
        self.s.send(message.encode())
        # after sending, wait for the response
        return self.receiveMessage()

    def receiveMessage(self):
        print("recieving Meesage")
        # wait until opponent sends a guess
        message = self.s.recv(1024).decode('utf-8', 'ignore')
        print("MESSAGE: " + message)
        return message

    def end(self):
        self.s.close()

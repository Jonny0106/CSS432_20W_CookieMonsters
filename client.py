import socket
import json
import gameBoard
import pygame


class Client:
    def __init__(self, p1):
        self.p1 = p1
        self.printDisplay("Welcome to Team Cookie Monsters' Battleship Game!")
        self.s = socket.socket()
        # self.host = "10.155.176.29"
        self.host = socket.gethostname()
        self.port = 6010
        self.s.connect((self.host, self.port))
        self.goFirst = False

        # upon connecting to server, get the player_id
        first_ask = True
        rec = ""
        while "CONFIRMED" not in rec:
            if not first_ask:
                self.printDisplay("That name looks to be taken already. Please try another name.")
            request_player_id = "NEW " + self.ask_for_name()
            self.s.send(request_player_id.encode())
            rec = str(self.s.recv(1024).decode('utf-8', 'ignore'))
            first_ask = False
        self.player_id = rec.split()[1]
        self.game_id = ""
        self.printDisplay("Connection established with server!",)
        self.printDisplay("Your player ID is: " + self.player_id, end="keep")
        self.ask_for_choice()

    def ask_for_name(self):
        self.printDisplay("Enter your name: ", end="keep")
        req_name = input()
        while req_name == "":
            self.printDisplay("Invalid name. Please enter your name: ")
            req_name = input()
        return self.change_spaces_to_underscores(req_name)

    def change_spaces_to_underscores(self, name):
        split_name = name.split()
        ret_str = ""
        if len(split_name) == 1:
            return name
        else:
            for x in split_name:
                ret_str += x + "_"
        return ret_str[:-1]

    def ask_for_choice(self):
        self.printDisplay("Please enter a 'j' to list all of the possible games to join or a 'c' to create a new game: ", end="keep")
        choice = input()

        while True:
            if choice == "j" or choice == "c":
                self.act_on_choice(choice)
                break
            else:
                self.printDisplay("'j' or 'c' was not entered. Enter 'j' to join a game or 'c' to create a game: ", end="keep")
                choice = input()

    def print_waiting_games(self, string_of_dict):
        dict_of_waiting_games = json.loads(string_of_dict)
        if not dict_of_waiting_games:
            self.printDisplay("No one is waiting. Please create a new game.")
        else:
            for game_id in dict_of_waiting_games:
                self.printDisplay("Game ID: " + game_id + " Player ID: " + dict_of_waiting_games[game_id],end="keep")

    # start game once both players have joined
    def start_game(self, given_game_id):
        hello_msg = "MSG " + self.player_id + " " + given_game_id + " Hello this is your opponent, " + self.player_id + " on game " + given_game_id
        self.printDisplay("-sending-" + hello_msg)
        self.s.send(hello_msg.encode())
        hello_response = self.s.recv(1024).decode('utf-8', 'ignore')
        self.printDisplay(hello_response, end="keep")

    def act_on_choice(self, choice):
        if choice == "j":
            self.printDisplay("Here are a list of games you can join:")
            # request dictionary of WaitingGames from server
            create_msg = "LIST " + self.player_id
            self.s.send(create_msg.encode())

            # print out each game_id and player_id
            string_of_dict = self.s.recv(1024).decode('utf-8', 'ignore')
            self.print_waiting_games(string_of_dict)

            self.printDisplay("Please enter in the Game ID of the game you would like to join.", end="keep")
            self.printDisplay("If there are no games you would like to join, enter 'c' to create a new game: ", end="keep")
            self.act_on_choice(input())
        elif choice == "c":
            self.printDisplay("")
            self.printDisplay("Creating new game...")
            # tell server to create a new game (send player_id)
            create_msg = "CREATE " + self.player_id
            self.s.send(create_msg.encode())
            self.printDisplay("Game has been created. Please wait for another player to join...", end="keep")
            self.goFirst = True
            create_start_response = self.s.recv(1024).decode('utf-8', 'ignore')
            if "JOINED" in create_start_response:
                self.printDisplay("Successfully joined game!")
                self.game_id = create_start_response.split()[1]
                self.printDisplay(self.game_id, end="keep")
                # open the gamegrid and send back and forth the coordinates of hits and misses
                self.start_game(self.game_id)
        elif choice != "":
            self.printDisplay("Joining game...")
            # tell server to join a new game (send game_id and player_id)
            # in this case, choice is the game_id
            create_msg = "JOIN " + self.player_id + " " + choice
            self.s.send(create_msg.encode())
            join_response = self.s.recv(1024).decode('utf-8', 'ignore')
            if "JOINED" in join_response:
                self.printDisplay("Successfully joined game!")
                self.game_id = join_response.split()[1]
                self.printDisplay(self.game_id)

                # open the gamegrid and send back and forth the coordinates of hits and misses
                self.start_game(self.game_id)
            else:
                self.printDisplay("Could not join game. Please make sure to enter in the correct game ID (no quotes).", end="keep")
                self.ask_for_choice()
        else:
            self.printDisplay("You have not entered anything. Let's start over.")
            self.ask_for_choice("")

    def sendMessage(self, message):
        # send message out
        self.s.send(message.encode())
        # after sending, wait for the response
        return self.receiveMessage()

    def sendMessageResponse(self, message):
        self.s.send(message.encode())

    def receiveMessage(self):
        # wait until opponent sends a guess
        message = self.s.recv(1024).decode('utf-8', 'ignore')
        return message

    def end(self):
        self.s.close()
    
    def printDisplay(self, Dstr, end=""):
        if "keep" not in end:
            self.p1.dispayText = []
        while len(Dstr) >= 50:
            str1 = Dstr[:50]
            Dstr = "-" + Dstr[50:]
            self.p1.dispayText.append(str1)
        
        self.p1.dispayText.append(Dstr)
        self.p1.game_Coloring()
        self.p1.textChange(self.p1.dispayText)
        
        self.p1.game_Coloring()
        self.p1.game_Event()

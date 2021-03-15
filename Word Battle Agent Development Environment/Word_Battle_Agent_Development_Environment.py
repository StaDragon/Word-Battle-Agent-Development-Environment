#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) Jordan Memphis Leef. All Rights Reserved.
# View the LICENSE.md on GitHub

__all__ = ["__title__", "__version__", "__author__", "__license__", "__copyright__"]
__title__ = "Word Battle Agent Development Environment"
__version__ = "1.1"
__author__ = "Jordan Memphis Leef"
__license__ = "Freeware"
__copyright__ = "Copyright (C) Jordan Memphis Leef"

from typing import Union, List, Dict, Tuple, Generator, Optional, Any
from pyspin.spin import Spin1, Spinner
from colorama import Fore, Style
import itertools as it
import numpy as np
import subprocess
import os.path
import random
import msvcrt
import ctypes
import errno
import json
import time
import copy
import sys
import ast
import re

# Global constant declaration
PY_VERSION = 3.8 # The Python version that the game is programmed on
SW_MAXIMISE = 3 # Set the command prompt to open in maximized window
LOWER_LIMIT = 3 # The min board length
UPPER_LIMIT = 15 # The max board length
CHAR_LIMIT = 20 # Character limit
COMPUTER_PLAYER_NAME = "Computer" # To distinguish itself from human players
LOCAL_DIR_VOCABULARY = "./Vocabulary/" # The path to the "Vocabulary" folder
LOCAL_DIR_RECORDS = "./Records/" # The path to the "Records" folder
LOCAL_DIR_REPLAYS = "./Replays/" # The path to the "Replays" folder
REPLAY_FILE_FORMAT = ".wbr" # The format for the replay files
LETTER_VALUE = {"A": 3, "B": 9, "C": 8, "D": 7, "E": 1, "F": 8, "G": 8, "H": 5, "I": 5, "J": 10, "K": 10, "L": 7, "M": 8, "N": 5, "O": 4, "P": 9, "Q": 10, "R": 6, "S": 5, "T": 2, "U": 8, "V": 10, "W": 8, "X": 10, "Y": 9, "Z": 10} # The strength of each letter

CUSTOM_COMPUTER_PLAYER_NAME = "" # To distinguish itself from official computer players and human players

# Global variable declaration
game_word_list = {}
vocab_1 = {}
vocab_2 = {}

def clear_screen(time_set=1) -> None:
    """Clear the screen."""
    time.sleep(time_set)
    os.system('cls')


def input_integer(label: str) -> int:
    """Convert an string and output as integer."""
    while True:
        try:
            return int(input(label))
        except ValueError:
            pass


def check_if_file_exists(file_name: str, open_in_other_folder=False) -> None:
    try:
        if open_in_other_folder:
            with open(f"{LOCAL_DIR_VOCABULARY}{file_name}") as f:
                f.close()
        else:
            f = open(file_name)
            f.close()
    except FileNotFoundError:
        clear_screen(0)
        print(Fore.WHITE + Style.BRIGHT + f"{__title__} v{__version__} System Event")
        print(Fore.RED + Style.BRIGHT + f"Error: File not found!\nPlease add the file {file_name} before continuing")
        print(Fore.WHITE + Style.BRIGHT + "Press any key to continue...")
        msvcrt.getch()
        check_if_file_exists(file_name, open_in_other_folder)


def categorise_word_by_length(raw_word_list: List[str]) -> Dict:
    """Categorised each word according to their lengths, this is to improve the computer player in searching for a word."""
    words_categorised = {}

    for word in raw_word_list:
        if len(word) not in words_categorised.keys():
            words_categorised[len(word)] = []
        words_categorised[len(word)].append(word.upper())

    return words_categorised


def get_board_length() -> int:
    """Get the length of the board."""
    try:
        user_input = int(input(Fore.WHITE + Style.BRIGHT + f"Board Length (between {LOWER_LIMIT} and {UPPER_LIMIT}, type 0 to go back): "))

        if LOWER_LIMIT <= user_input <= UPPER_LIMIT:
            return user_input
        elif user_input == 0:
            main()
        else:
            clear_screen(0)
            print(Fore.WHITE + Style.BRIGHT + f"Board Length (between {LOWER_LIMIT} and {UPPER_LIMIT}, type 0 to go back): " + Fore.RED + Style.BRIGHT + "Invalid board length!")
            clear_screen()
            return get_board_length()
    except ValueError:
        clear_screen(0)
        print(Fore.WHITE + Style.BRIGHT + f"Board Length (between {LOWER_LIMIT} and {UPPER_LIMIT}, type 0 to go back): " + Fore.RED + Style.BRIGHT + "Invalid board length!")
        clear_screen()
        return get_board_length()


def get_how_many_games() -> int:
    """Get how many simulations being ran."""
    clear_screen(0)

    try:
        user_input = int(input(Fore.WHITE + Style.BRIGHT + "How many games? (type 0 to go back): "))

        if user_input >= 1:
            return user_input
        elif user_input == 0:
            main()
        else:
            return get_how_many_games()
    except ValueError:
        return get_how_many_games()


def open_replay() -> None:
    """Open .wbr files to watch them."""
    def run_replay(replay_info: dict, replay_speed: float) -> None:
        """Run the replay file."""
        board = Board()
        board.create_board(replay_info['wbr_game_info'][0]['board_length'])
        game_duration = replay_info['wbr_game_info'][0]['game_duration']
        board.game_duration = game_duration
        players = []

        for player in replay_info['wbr_game_info'][1:]:
            if player['player_name'] not in players:
                players.append({"name": player['player_name'], "type": player['type'], "difficulty": player['difficulty']})

        board.players = [dict(t) for t in {tuple(d.items()) for d in players}]
        board.player = players[0]['name']

        if players[0]['difficulty'] is not None:
            board.player = f"{players[0]['name']} ({players[0]['difficulty']})"

        board.game_counter = replay_info['wbr_game_info'][0]['game_number']
        clear_screen(0)
        board.display_game_title()
        board.display_board()
        print(f"Replay speed: {replay_speed}\nReplay file: {file}{REPLAY_FILE_FORMAT}\n")

        for player in replay_info['wbr_game_info'][1:]:
            event = player['event']
            player_name = player['player_name']
            player_type = player['type']
            board.player = player_name

            if player_type == "computer":
                player_name = f"{player['player_name']} ({player['difficulty']})"

            if event == 'RESIGNED':
                clear_screen(1.5) # Do not delete!
                board.display_game_title(False, False, True) # Do not delete!
                board.display_board() # Do not delete!
                print(f"Replay speed: {replay_speed}\nReplay file: {file}{REPLAY_FILE_FORMAT}\n") # Do not delete!
                clear_screen(1.5)
                board.display_game_title(False, False, True)
            elif event == 'WON':
                board.winner = player_name
                clear_screen(0)
                board.display_game_title(False, True)
            elif event == 'PLAYING':
                board.turn_counter += 1
                board.selected_path = [tuple(i) for i in player['selected_path']]
                board.place_word(player['word'])
                board.previous_player = player_name
                clear_screen(replay_speed)
                board.display_game_title()
            elif event == 'DRAW':
                board.draw = True
                clear_screen(1)
                board.display_game_title(True)

            board.display_board()
            print(f"Replay speed: {replay_speed}\nReplay file: {file}{REPLAY_FILE_FORMAT}\n")

        print("Replay finished, press any key to continue...")
        msvcrt.getch()

        while True:
            clear_screen(0)
            print(Fore.WHITE + Style.BRIGHT + "Replay menu\n[1] Watch again\n[2] Change speed and watch again\n[3] Open another file\n[4] Go back to main menu\n")

            try:
                selection = int(input((Fore.WHITE + Style.BRIGHT + "Selection: ")))
                if selection == 1:
                    run_replay(replay_info, replay_speed)
                elif selection == 2:
                    clear_screen(0)
                    get_replay_speed(replay_info)
                elif selection == 3:
                    clear_screen(0)
                    open_replay()
                elif selection == 4:
                    main()
                else:
                    pass
            except ValueError:
                pass

    def get_replay_speed(replay_info: dict) -> None:
        """Set how fast each turn cycles."""
        try:
            replay_speed = float(input("Replay speed. Type 0 to go back to main menu: "))
            if replay_speed > 0:
                run_replay(replay_info, replay_speed)
            elif replay_speed == 0:
                main()
            else:
                clear_screen(0)
                get_replay_speed(replay_info)
        except ValueError:
            clear_screen(0)
            get_replay_speed(replay_info)

    while True:
        file = input(Fore.WHITE + Style.BRIGHT + "Filename (Type 0 to go back to main menu): ")

        if file == "0":
            main()
        elif file == "":
            clear_screen(0)
            print(Fore.WHITE + Style.BRIGHT + "Filename (Type 0 to go back to main menu): " + Fore.RED + Style.BRIGHT + "filename cannot be empty!")
            print(Fore.WHITE + Style.BRIGHT + "Press any key to continue...")
            msvcrt.getch()
            clear_screen(0)
        else:
            # Create the folder if it does not exist
            try:
                os.makedirs('Replays')
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

            if os.path.isfile(f"{LOCAL_DIR_REPLAYS}{file}{REPLAY_FILE_FORMAT}"):
                try:
                    with open(f"{LOCAL_DIR_REPLAYS}{file}{REPLAY_FILE_FORMAT}") as f:
                        bytes_data = f.read().splitlines()
                        data = ast.literal_eval("".join(map(chr, [int(i) for i in bytes_data])))
                        wbr_content = {"wbr_game_info": data}
                        replay_info = json.dumps(wbr_content, indent=7)
                        replay_info = json.loads(replay_info)

                        if replay_info['wbr_game_info'][0]['game_number'] > 0 and replay_info['wbr_game_info'][0]['board_length'] > 0:
                            clear_screen(0)
                            get_replay_speed(replay_info)
                        else:
                            clear_screen(0)
                            print(Fore.WHITE + Style.BRIGHT + "Filename (Type 0 to go back to main menu): " + Fore.RED + Style.BRIGHT + "File not found or file extension not supported! Only .wbr (Word Battle Replay) files are supported.")
                            print(Fore.WHITE + Style.BRIGHT + "Press any key to continue...")
                            msvcrt.getch()
                            clear_screen(0)
                except (KeyError, ValueError, SyntaxError, OverflowError):
                    clear_screen(0)
                    print(Fore.WHITE + Style.BRIGHT + "Filename (Type 0 to go back to main menu): " + Fore.RED + Style.BRIGHT + "File is corrupted or outdated and cannot be opened!")
                    print(Fore.WHITE + Style.BRIGHT + "Press any key to continue...")
                    msvcrt.getch()
                    clear_screen(0)
            else:
                clear_screen(0)
                print(Fore.WHITE + Style.BRIGHT + "Filename (Type 0 to go back to main menu): " + Fore.RED + Style.BRIGHT + "File not found or file extension not supported! Only .wbr (Word Battle Replay) files are supported.")
                print(Fore.WHITE + Style.BRIGHT + "Press any key to continue...")
                msvcrt.getch()
                clear_screen(0)


class Custom_Agent:
    """Create an agent object."""
    # Write your custom agent program here

class Board:
    """Create an board object."""
    def __init__(self) -> None:
        self.length = None # The length of the board
        self.matrix = None # The 2D array of the board
        self.colour_map = None # The colours for each cell
        self.starting_position = None # The current starting position
        self.paths = None # A collection of paths
        self.paths_full = None # A collection of full paths
        self.selected_path = None # The current selected path
        self.players = None # The current player list
        self.player = None # The current player
        self.previous_player = None # the previous player in the previous turn
        self.previous_selected_path = None # the previous path selected by the player
        self.word = None # The current player's word
        self.used_words = None # Record every words used
        self.winner = None # The winner of the current game
        self.draw = False # Draw state
        self.game_counter = 0 # Game counter for each game
        self.turn_counter = 0 # Game counter for each game
        self.game_duration = 0 # Game Duration of the whole game

    def create_board(self, length: int) -> None:
        """Create the game board."""
        self.length = length
        self.matrix = np.full((self.length, self.length), " ", dtype='U1')
        self.colour_map = self.set_colour_map()

    def set_colour_map(self) -> Dict[Tuple[Any], Any]:
        """Ini the colours for the board."""
        cells = [coord for coord in it.product(*[range(r[0], r[1]) for r in zip([0, 0], [self.length, self.length])])]
        colour = ["WHITE"] * self.length ** 2
        return dict(zip(cells, colour))

    def check_draw(self) -> None:
        """Check for a draw."""
        if " " not in self.matrix:
            self.draw = True

    def get_starting_position(self) -> int:
        """Get the starting position of the player."""
        self.display_game_title()
        self.display_board()
        self.check_draw()

        if self.draw:
            return 2

        try:
            # Split the input to get the coordinates
            user_input = [int(n) for n in input(Fore.WHITE + Style.BRIGHT + "Starting Position: ").split(" ")]

            if len(user_input) == 1:
                if 0 not in user_input:
                    clear_screen(0)
                    self.display_game_title()
                    self.display_board()
                    print(Fore.WHITE + Style.BRIGHT + "Starting Position: " + Fore.RED + Style.BRIGHT + "Invalid coordinates!")
                    clear_screen()
                    return self.get_starting_position()
                else:
                    return 0
            else:
                if 0 in user_input:
                    clear_screen(0)
                    self.display_game_title()
                    self.display_board()
                    print(Fore.WHITE + Style.BRIGHT + "Starting Position: " + Fore.RED + Style.BRIGHT + "Invalid coordinates!")
                    clear_screen()
                    return self.get_starting_position()
                else:
                    if 0 < user_input[0] <= self.length and 0 < user_input[1] <= self.length:
                        if user_input[0] == 1 and user_input[1] == user_input[0] or user_input[0] == 1 and user_input[1] > user_input[0] or user_input[1] == 1 and user_input[1] < user_input[0] or user_input[0] == self.length and user_input[1] == user_input[0] or user_input[0] == self.length and user_input[0] > user_input[1] or user_input[1] == self.length and user_input[1] > user_input[0]:
                            self.starting_position = tuple([n - 1 for n in user_input])
                            return 1
                        else:
                            clear_screen(0)
                            self.display_game_title()
                            self.display_board()
                            print(Fore.WHITE + Style.BRIGHT + "Starting Position: " + Fore.RED + Style.BRIGHT + "Invalid coordinates!")
                            clear_screen()
                            return self.get_starting_position()
                    else:
                        clear_screen(0)
                        self.display_game_title()
                        self.display_board()
                        print(Fore.WHITE + Style.BRIGHT + "Starting Position: " + Fore.RED + Style.BRIGHT + "Invalid coordinates!")
                        clear_screen()
                        return self.get_starting_position()
        except (IndexError, ValueError):
            clear_screen(0)
            self.display_game_title()
            self.display_board()
            print(Fore.WHITE + Style.BRIGHT + "Starting Position: " + Fore.RED + Style.BRIGHT + "Invalid coordinates!")
            clear_screen()
            return self.get_starting_position()

    def create_valid_paths(self) -> None:
        """Generate paths based on the starting position. Check the list for paths that are full. Remove them if they are."""
        # Convert the coordinates of the starting position to zero-based numbering
        x = self.starting_position[0]
        y = self.starting_position[1]

        # Create a list of three paths
        path1 = []
        path2 = []
        path3 = []

        # Get coordinates for each path starting at corners
        # Starting position at top left corner
        if (x, y) == (0, 0):
            for i in range(self.length):
                # Path to top right corner
                path1 += [(0, i)]

                # Path to bottom right corner
                path2 += [(i, i)]

                # Path to bottom left corner
                path3 += [(i, 0)]

        # Starting position at top right corner
        elif (x, y) == (0, self.length - 1):
            for i in range(self.length):
                # Path to top left corner
                path1 += [(0, self.length - 1 - i)]

                # Path to bottom left corner
                path2 += [(i, self.length - 1 - i)]

                # Path to bottom right corner
                path3 += [(i, self.length - 1)]

        # Starting position at bottom left corner
        elif (x, y) == (self.length - 1, 0):
            for i in range(self.length):
                # Path to top left corner
                path1 += [(self.length - 1 - i, 0)]

                # Path to top right corner
                path2 += [(self.length - 1 - i, i)]

                # Path to bottom right corner
                path3 += [(self.length - 1, i)]

        # Starting position at bottom right corner
        elif (x, y) == (self.length - 1, self.length - 1):
            for i in range(self.length):

                # Path to top right corner
                path1 += [(i, self.length - 1)]

                # Path to top left corner
                path2 += [(i, i)]

                # Path to bottom left corner
                path3 += [(self.length - 1, i)]

            # Reverse any path that may needs be
            path1.reverse()
            path2.reverse()
            path3.reverse()

        # Get coordinates for each path starting at edges
        else:
            # Starting position at top edge
            if x == 0:
                # Path to left edge
                temp_x = x
                temp_y = y

                while temp_y >= 0:
                    path1 += [(temp_x, temp_y)]
                    temp_x += 1
                    temp_y -= 1

                # Path to bottom edge
                for i in range(self.length):
                    path2 += [(i, y)]

                # Path to right edge
                temp_x = x
                temp_y = y

                while temp_y < self.length:
                    path3 += [(temp_x, temp_y)]
                    temp_x += 1
                    temp_y += 1

            # Starting position at left edge
            elif y == 0:
                # Path to top edge
                temp_x = x
                temp_y = y

                while temp_x >= 0:
                    path1 += [(temp_x, temp_y)]
                    temp_x -= 1
                    temp_y += 1

                # Path to right edge
                for i in range(self.length):
                    path2 += [(x, i)]

                # Path to bottom edge
                temp_x = x
                temp_y = y

                while temp_x < self.length:
                    path3 += [(temp_x, temp_y)]
                    temp_x += 1
                    temp_y += 1

            # Starting position at right edge
            elif y == self.length - 1:
                # Path to top edge
                temp_x = x
                temp_y = y

                while temp_x >= 0:
                    path1 += [(temp_x, temp_y)]
                    temp_x -= 1
                    temp_y -= 1

                # Path to left edge
                for i in range(self.length):
                    path2 += [(x, i)]

                # Path to bottom edge
                temp_x = x
                temp_y = y

                while temp_x < self.length:
                    path3 += [(temp_x, temp_y)]
                    temp_x += 1
                    temp_y -= 1

                # Reverse any path that may needs be
                path2.reverse()

            # case of starting point on the bottom edge
            elif x == self.length - 1:
                # Path to left edge
                temp_x = x
                temp_y = y

                while temp_y >= 0:
                    path1 += [(temp_x, temp_y)]
                    temp_x -= 1
                    temp_y -= 1

                # Path to top edge
                for i in range(self.length):
                    path2 += [(i, y)]

                # Path to right edge
                temp_x = x
                temp_y = y

                while temp_y < self.length:
                    path3 += [(temp_x, temp_y)]
                    temp_x -= 1
                    temp_y += 1

                # Reverse any path that may needs be
                path2.reverse()

        self.paths = [path1, path2, path3]
        self.paths_full = [path1, path2, path3]

        # Create a list of strings for each path
        path1_res = []
        path2_res = []
        path3_res = []

        # Checking if the paths are full if they do not contain an empty string
        for coord in self.paths[0]:
            if " " in self.matrix[coord]:
                path1_res.append(self.matrix[coord])
        for coord in self.paths[1]:
            if " " in self.matrix[coord]:
                path2_res.append(self.matrix[coord])
        for coord in self.paths[2]:
            if " " in self.matrix[coord]:
                path3_res.append(self.matrix[coord])

        try:
            if not path1_res:
                self.paths.pop(0)
            if not path2_res:
                self.paths.pop(-2)
            if not path3_res:
                self.paths.pop(1)
        except IndexError:
            self.paths = []

    def get_selected_path(self) -> int:
        """Get selected path from player"""
        temp_board = np.full((self.length, self.length), " ", dtype='U1')
        temp_colour_map = self.set_colour_map()

        # Labelling each path with its corresponding character and assign each coordinate with its colour
        end_path_numbering = 1

        if not self.paths:
            for path in self.paths_full:
                for coord in path:
                    temp_colour_map[coord] = "RED"
        else:
            for path in self.paths:
                for coord in path:
                    temp_colour_map[coord] = "GREEN"

                    # Labelling the succeeding position with an dot
                    temp_board[coord] = "•"

                # Labelling the end positions with an integer to indicate selection number
                temp_board[path[-1]] = str(end_path_numbering)
                end_path_numbering += 1

        # Assign the first cell with its colour
        temp_colour_map[self.starting_position] = "YELLOW"

        if not self.paths:
            self.display_game_title()
            self.display_board(None, temp_colour_map)
            print(Fore.WHITE + Style.BRIGHT + "Starting Position: " + Fore.RED + Style.BRIGHT + "All available paths are full! Select another starting position!")
            return 2
        else:
            self.display_game_title()
            self.display_board(temp_board, temp_colour_map)

            try:
                # Note: inputs are based on zero-based numbering due to the coordinate system of using zero-based numbering
                user_input = int(input(Fore.WHITE + Style.BRIGHT + "Type path number: "))

                if user_input == 0:
                    return 0
                elif user_input == 4:
                    return 1
                elif 0 < user_input <= len(self.paths):
                    self.selected_path = self.paths[user_input - 1]
                    self.display_selected_path()
                else:
                    clear_screen(0)
                    self.display_game_title()
                    self.display_board(temp_board, temp_colour_map)
                    print(Fore.WHITE + Style.BRIGHT + "Type path number: " + Fore.RED + Style.BRIGHT + "Invalid path number!")
                    clear_screen()
                    return self.get_selected_path()
            except ValueError:
                clear_screen(0)
                self.display_game_title()
                self.display_board(temp_board, temp_colour_map)
                print(Fore.WHITE + Style.BRIGHT + "Type path number: " + Fore.RED + Style.BRIGHT + "Invalid path number!")
                clear_screen()
                return self.get_selected_path()

    def display_selected_path(self, time=0) -> None:
        """Display the selected path."""
        temp_board = np.full((self.length, self.length), " ", dtype='U1')
        temp_colour_map = self.set_colour_map()

        # Labelling each path with its corresponding character and assign each coordinate with its colour
        for coord in self.selected_path:
            if self.matrix[coord] == " ":
                temp_board[coord] = "•"
            else:
                temp_board[coord] = self.matrix[coord]

            temp_colour_map[coord] = "GREEN"

        # Assign the first cell with its colour
        temp_colour_map[self.starting_position] = "YELLOW"

        # Print the board
        clear_screen(time)
        self.display_game_title(False, False, False, True)
        self.display_board(temp_board, temp_colour_map)

    def display_game_title(self, is_draw=False, there_is_winner=False, has_resigned=False, display_used_words=False) -> None:
        """Display the game title."""
        if is_draw:
            print(Fore.WHITE + Style.BRIGHT + " VS ".join([f"{i['name']} ({i['difficulty']})" if i['difficulty'] is not None else f"{i['name']}" for i in self.players]), sep='', end='')
            print(f"\nGame: {self.game_counter} | Turn: {self.turn_counter} | Draw!\nGame {self.game_counter} has ended! | Game Duration: {self.game_duration}")
        elif there_is_winner:
            print(Fore.WHITE + Style.BRIGHT + " VS ".join([f"{i['name']} ({i['difficulty']})" if i['difficulty'] is not None else f"{i['name']}" for i in self.players]), sep='', end='')
            print(f"\nGame: {self.game_counter} | Turn: {self.turn_counter} | {self.winner} won!\nGame {self.game_counter} has ended! | Game Duration: {self.game_duration}")
        elif has_resigned:
            print(Fore.WHITE + Style.BRIGHT + " VS ".join([f"{i['name']} ({i['difficulty']})" if i['difficulty'] is not None else f"{i['name']}" for i in self.players]), sep='', end='')
            print(f"\nGame: {self.game_counter} | Turn: {self.turn_counter} | {self.player}'s Turn")
            print(f"{self.player} has resigned!")
        elif display_used_words:
            print(Fore.WHITE + Style.BRIGHT + " VS ".join([f"{i['name']} ({i['difficulty']})" if i['difficulty'] is not None else f"{i['name']}" for i in self.players]), sep='', end='')
            print(f"\nGame: {self.game_counter} | Turn: {self.turn_counter} | {self.player}'s Turn")

            if self.used_words is not None:
                print(Fore.WHITE + Style.BRIGHT + "Word(s) used: " + Fore.RED + Style.BRIGHT + ', '.join(self.used_words))
            else:
                print(Fore.WHITE + Style.BRIGHT + "Word(s) used:")
        else:
            print(Fore.WHITE + Style.BRIGHT + " VS ".join([f"{i['name']} ({i['difficulty']})" if i['difficulty'] is not None else f"{i['name']}" for i in self.players]), sep='', end='')
            print(f"\nGame: {self.game_counter} | Turn: {self.turn_counter} | {self.player}'s Turn")

            if self.turn_counter == 0:
                print(f"Game {self.game_counter} has started!")
            else:
                print(f"{self.previous_player} placed down {self.word}")

    def display_board(self, board=None, colour_map=None, get_str_board=False, computer_player=False) -> int:
        """Display the board."""
        def chunks(data: Dict[Tuple[int, int], str], SIZE=10000) -> Generator[Dict[Tuple[int, int], str], any, None]:
            """Divide the data into chunks."""
            itt = iter(data)

            for i in range(0, len(data), SIZE):
                yield {k: data[k] for k in it.islice(itt, SIZE)}

        if colour_map is None:
            colour_map = self.colour_map

        if board is None:
            board = self.matrix

        # Colour the previous word placed by the player
        if self.previous_selected_path is not None:
            for key in self.colour_map:
                self.colour_map[key] = "WHITE"

            for coord in self.previous_selected_path:
                self.colour_map[coord] = "CYAN"

                if computer_player:
                    self.colour_map[coord] = "GREEN"

            if computer_player:
                self.colour_map[self.previous_selected_path[0]] = "YELLOW"

        # Create a list of chunks
        chunks_list = []

        # Create chunks of the colour map and store them in the chunks list
        for item in chunks(colour_map, self.length):
            chunks_list.append(item)

        # Display the game board
        if board is None:
            board = self.matrix

        # Create representation of the board
        str_board = Fore.WHITE + Style.BRIGHT + " "
        str_board += " "

        # Labelling top columns
        for column_number in range(self.length):
            if column_number < 9:
                str_board += f"   {column_number + 1}"
            else:
                str_board += f"  {column_number + 1}"

        str_board +="\n   ┌───┬─"

        for _ in range(self.length - 2):
            str_board+= "──┬─"

        str_board += "──┐\n"

        # Labelling left rows
        lines = 0

        for chunk in chunks_list:
            if chunks_list.index(chunk) < 9:
                str_board += f"  {str(chunks_list.index(chunk) + 1)}"
            else:
                str_board += f" {str(chunks_list.index(chunk) + 1)}"


            # Assign each string to its corresponding colour depending on the coordinates
            for coord, colour in chunk.items():
                set_colour = getattr(Fore, colour)
                str_board += Fore.WHITE + "│" + set_colour + f" {board[coord]} " + Fore.WHITE


            # Labelling right rows
            str_board += f"│{str(chunks_list.index(chunk) + 1)}\n   ├─"
            for _ in range(self.length - 1):
                str_board += "──┼─"

            if lines < self.length - 1:
                str_board += "──┤\n"
                lines += 1
            else:
                str_board += "\r"

        # Labelling bottom columns
        str_board +="   └───┴─"

        for _ in range(self.length - 2):
            str_board+= "──┴─"

        str_board += "──┘\n  "

        for column_number in range(self.length):
            if column_number < 9:
                str_board += f"   {column_number + 1}"
            else:
                str_board += f"  {column_number + 1}"

        if get_str_board:
            return str_board
        else:
            print(f"\n{str_board}\n")

    def place_word(self, word: str) -> None:
        """Place the word onto the game board."""
        self.word = word
        self.previous_selected_path = self.selected_path

        for coord in self.previous_selected_path:
            self.matrix[coord] = self.word[self.previous_selected_path.index(coord)]

class Official_Agent:
    """Create an agent object."""
    def __init__(self) -> None:
        self.agent_name = None # The name of the agent
        self.difficulty = None # The difficulty of the agent
        self.vocabulary = None # The vocabulary of the agent
        self.analyse_board = None # The current board to be analysed
        self.analyse_used_words = None # The used words to be analysed
        self.used_words = None # The used words for a simulated game
        self.board_length = None # The length of the board
        self.options = [] # A collection of options
        self.players_list = [{"name": f"agent {player + 1}", "path_selected": None, "word_selected": None} for player in range(2)] # A list of players for an simulated game
        self.final_selected_path = None # The agent's selected path for the real game
        self.final_selected_word = None # The agent's selected word for the real game
        self.considered_starting_position = None # The considered starting position from the current board
        self.considered_paths = None # The considered paths from the current board
        self.draw_detected = False # Check if the real game has been drawn

    @staticmethod
    def calculate_word_strength(word: str) -> int:
        """Calculate the strength of the word."""
        total = 0

        try:
            for letter in word:
                total += LETTER_VALUE[letter]
        except KeyError:
            return 0

        return total

    def get_word(self, board: np.array, path_length: int, path_selected: List[Tuple[int, int]]) -> Optional[Any]:
        """Get a word based on the selected path."""
        common_letters = []

        for coord in path_selected:
            common_letters.append(board[coord])

        word_required_to_match = [word.replace(" ", ".") for word in common_letters]

        if "." not in word_required_to_match:
            return 0
        else:
            try:
                words_found = [word for word in self.vocabulary[path_length] if re.match(re.compile(''.join(word_required_to_match)), word)]
            except KeyError:
                return 0

        try:
            word_selected = random.choice(words_found)
        except IndexError:
            return 0

        if len(word_selected) == path_length and word_selected not in self.used_words:
            self.used_words.append(word_selected)
            return word_selected
        else:
            return 0

    def generate_starting_positions(self) -> None:
        """Generate starting positions with those without resulting with full paths."""
        self.considered_starting_position = []

        for x in range(self.board_length):
            for y in range(self.board_length):
                if x == 0 and y == x or x == 0 and y > x or y == 0 and y < x or x == self.board_length - 1 and y == x or x == self.board_length - 1 and x > y or y == self.board_length - 1 and y > x:
                    self.analyse_board.starting_position = x, y
                    self.analyse_board.create_valid_paths()

                    if self.analyse_board.paths:
                        self.considered_starting_position.append(self.analyse_board.starting_position)

    def generate_paths(self) -> None:
        """Generate paths based on the starting positions."""
        self.considered_paths = []

        for coord in self.considered_starting_position:
            self.analyse_board.starting_position = coord
            self.analyse_board.create_valid_paths()

            for path in self.analyse_board.paths:
                self.analyse_board.selected_path = path
                self.considered_paths.append(path)

    def make_turn(self, board: np.array, path_list=None) -> Union[Tuple[Any, Any], int]:
        """Make a turn."""
        if path_list is None:
            considered_paths = self.considered_paths.copy()
        else:
            considered_paths = path_list

        try:
            path_selected = random.sample(considered_paths, len(considered_paths))[0]
        except IndexError:
            return 0

        word_selected = self.get_word(board.matrix, len(path_selected), path_selected)

        if word_selected != 0:
            return word_selected, path_selected
        elif considered_paths:
            considered_paths.remove(path_selected)
            return self.make_turn(board, considered_paths)
        elif not considered_paths:
            return 0

    def get_result(self) -> None:
        """Get the results from this simulated game."""
        board = Board()
        board.matrix = self.analyse_board.matrix.copy()
        current_players_list = self.players_list.copy()
        first_selected_path = None
        first_selected_word = None
        run = True
        draw = False

        # The thinking animation
        spin = Spinner(Spin1)

        while run:
            # Display that the computer player is thinking to give an indication that the program did not respond or whatever
            print(f"\r{self.agent_name} ({self.difficulty}) is thinking {spin.next()}", end="")
            time.sleep(0.4)

            if len(current_players_list) < 2:
                run = False
            elif draw:
                outcome = 0
                self.options.append({"outcome": outcome, "turn_number": board.turn_counter, "path": first_selected_path, "word": first_selected_word})
                run = False
            else:
                for player in current_players_list:
                    player_turn = self.make_turn(board)

                    if " " not in board.matrix:
                        draw = True
                    elif player_turn == 0:
                        current_players_list.remove(player)

                        if first_selected_path is None and first_selected_word is None:
                            try:
                                first_selected_word = player_turn[0]
                                first_selected_path = player_turn[1]
                            except TypeError:
                                first_selected_path = None
                                first_selected_word = None

                            player['path_selected'] = first_selected_path
                            player['word_selected'] = first_selected_word

                        if player['name'] == "agent 1":
                            outcome = -1
                            self.options.append({"outcome": outcome, "turn_number": board.turn_counter, "path": first_selected_path, "word": first_selected_word})
                        else:
                            outcome = 1
                            self.options.append({"outcome": outcome, "turn_number": board.turn_counter, "path": first_selected_path, "word": first_selected_word})

                        run = False
                    else:
                        try:
                            selected_word = player_turn[0]
                            selected_path = player_turn[1]
                        except TypeError:
                            selected_word = None
                            selected_path = None

                        for coord in selected_path:
                            board.matrix[coord] = selected_word[selected_path.index(coord)]

                        if first_selected_path is None and first_selected_word is None:
                            first_selected_path = selected_path
                            first_selected_word = selected_word
                            player['path_selected'] = first_selected_path
                            player['word_selected'] = first_selected_word

                        board.turn_counter += 1

    def make_decision(self) -> int:
        """Agent forms decision making presented with current options to determine the best possible strategy."""
        options = [option for option in self.options if option['path'] is not None]
        option_length = len(options)

        # If any of the outcomes is not a lost, then proceed to select the best possible strategy
        if not option_length:
            return 0
        else:
            options.sort(key=lambda e: e['outcome'], reverse=True)
            temp_outcome = -1

            for option in list(options):
                outcome = option['outcome']

                if outcome >= temp_outcome:
                    temp_outcome = outcome

                if outcome < temp_outcome:
                    options.pop(options.index(option))

            temp_confidence = -185 # This is the sum of all the letters in the letter value
            temp_word_strength = 0

            for option in options:
                outcome = option['outcome']
                confidence = option['turn_number']
                path = option['path']
                word = option['word']
                word_strength = self.calculate_word_strength(word)

                if outcome == 1:
                    confidence = confidence * -1

                if confidence > temp_confidence:
                    temp_confidence = confidence
                    temp_word_strength = word_strength
                    self.final_selected_path = path
                    self.final_selected_word = word
                elif confidence == temp_confidence:
                    if word_strength >= temp_word_strength:
                        temp_confidence = confidence
                        temp_word_strength = word_strength
                        self.final_selected_path = path
                        self.final_selected_word = word

    def play(self) -> None:
        """Make the agent play the game."""
        self.used_words = self.analyse_used_words.copy()
        self.generate_starting_positions()
        self.generate_paths()
        # self.debugger()

        if " " not in self.analyse_board.matrix:
            self.draw_detected = True
        elif not self.draw_detected:
            # Determine the runs by difficulty, the higher the runs, the longer it takes for the agent to make a turn
            if self.difficulty == "EASY":
                self.vocabulary = vocab_1
                run = 3

                while run > 0:
                    self.get_result()
                    self.used_words = self.analyse_used_words.copy()
                    run -= 1
            elif self.difficulty == "MEDIUM":
                self.vocabulary = vocab_2
                run = 8

                while run > 0:
                    self.get_result()
                    self.used_words = self.analyse_used_words.copy()
                    run -= 1
            elif self.difficulty == "HARD":
                self.vocabulary = game_word_list
                run = 8

                while run > 0:
                    self.get_result()
                    self.used_words = self.analyse_used_words.copy()
                    run -= 1

            self.make_decision()

        # self.turn_visualisation()

    def debugger(self) -> None:
        """View the values contained within the agent."""
        clear_screen(0)
        title = "Agent Debugger:"
        print(Fore.WHITE + Style.BRIGHT + f"{title}\n", "-" * len(title), "\n", sep='')
        print(f"self.considered_starting_position =\n{self.considered_starting_position}\n")
        print(f"self.board_length =\n{self.board_length}\n")
        print(f"self.analyse_board =\n{self.analyse_board.matrix}\n")
        print(f"self.analyse_used_words =\n{self.analyse_used_words}\n")
        print("Press any key to continue...")
        msvcrt.getch()

    def turn_visualisation(self) -> None:
        """Display the visualisation of the agent."""
        clear_screen(0)
        title = "Agent Visualisation:"
        print(Fore.WHITE + Style.BRIGHT + f"{title}\n", "-" * len(title), "\n", sep='')
        print("Raw Observations:", end='')
        self.analyse_board.display_board()
        temp_colour_map = self.analyse_board.set_colour_map()

        for coord in self.considered_starting_position:
            self.analyse_board.starting_position = coord

            if self.analyse_board.matrix[coord] == " ":
                self.analyse_board.matrix[coord] = "•"

            temp_colour_map[coord] = "YELLOW"

        print("Considered Starting Positions:", end='')
        self.analyse_board.display_board(None, temp_colour_map)

        for coord in self.considered_starting_position:
            if self.analyse_board.matrix[coord] == "•":
                self.analyse_board.matrix[coord] = " "

        print("Word(s) Used: " + Fore.RED + Style.BRIGHT + ', '.join(self.analyse_used_words))

        if self.draw_detected:
            starting_position = None
            word = None
        else:
            try:
                starting_position = tuple([x + 1 for x in list(self.final_selected_path[0])])
                word = self.final_selected_word
            except TypeError:
                starting_position = None
                word = None

        print(Fore.WHITE + Style.BRIGHT + f"\nPlacing Word At {starting_position}: {word}")

        try:
            self.analyse_board.selected_path = self.final_selected_path
            self.analyse_board.place_word(self.final_selected_word)
        except TypeError:
            pass

        self.analyse_board.display_board(None, None, False, True)
        print("Press any key to continue...")
        msvcrt.getch()

class Game:
    """Create an game object."""
    def __init__(self, starting_counter: int, length: int, players: List[Dict[str, str]], total_game_number=0, sim=False) -> None:
        self.total_game_number = total_game_number # The number of games to be simulated
        self.sim = sim # Simulated state
        self.players_list = players # Current list of players accessed
        self.removed_players = [] # Record every removed players
        self.used_words = [] # Record every words used
        self.board_length = length # Current length of the board
        self.board = Board() # Ini the game board
        self.board.create_board(length) # Create the game board
        self.board.game_counter = starting_counter # Initialize the game counter
        self.board.players = players.copy() # Copy of current list of players accessed
        self.first_turn = False # Check for the first turn
        self.paths_full = False # Check for full paths
        self.winner = None # Winner of the current game
        self.draw = False # Draw state
        self.replay_info = [{"game_number": starting_counter, "board_length": length}] # The contents of the replay

    def end_game_summary(self) -> None:
        """Display summary of a recently finished game."""
        title = "End Game Summary"
        heading = f"{title}\n{'-' * len(title)}"
        players = " VS ".join([f"{i['name']} ({i['difficulty']})" if i['difficulty'] is not None else f"{i['name']}" for i in self.players_list])
        description = f"\nPlayed {self.board.game_counter} game(s) on an {self.board_length}x{self.board_length} board."

        # Display summary
        clear_screen(0)
        print(heading)
        print(players, sep='', end='')
        print(description)

        for player in self.players_list:
            if player['difficulty'] is None:
                print(f"\n{player['name']}\nWINS: {player['stats']['wins']} LOSES: {player['stats']['loses']} DRAWS: {player['stats']['draws']}")
            else:
                print(f"\n{player['name']} ({player['difficulty']})\nWINS: {player['stats']['wins']} LOSES: {player['stats']['loses']} DRAWS: {player['stats']['draws']}")

        # Display options
        while True:
            user_input = input("\nSave record of game? Y/N: ").upper()

            if user_input == "Y":
                # Create the folder if it does not exist
                try:
                    os.makedirs('Records')
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise

                # Create the file
                game_title = " VS ".join([f"{i['name']} ({i['difficulty']})" if i['difficulty'] is not None else f"{i['name']}" for i in self.players_list]) + f" Game Summary"
                i = 1
                file_name = f"{LOCAL_DIR_RECORDS}{game_title} {i}.txt"

                while os.path.exists(file_name):
                    file_name = f"{LOCAL_DIR_RECORDS}{game_title} {i}.txt"
                    i += 1

                heading = f"{__title__} v{__version__} {title}"
                f = open(file_name, 'w')
                f.write(f"{heading}\n{'-' * len(heading)}\n")
                f.write(players)
                f.write(description)

                for player in self.players_list:
                    if player['difficulty'] is None:
                        f.write(f"\n\n{player['name']}\nWINS: {player['stats']['wins']} LOSES: {player['stats']['loses']} DRAWS: {player['stats']['draws']}")
                    else:
                        f.write(f"\n\n{player['name']} ({player['difficulty']})\nWINS: {player['stats']['wins']} LOSES: {player['stats']['loses']} DRAWS: {player['stats']['draws']}")

                f.close()
                main()
            elif user_input == "N":
                main()
            else:
                self.end_game_summary()

    def end_game_display(self, time=1) -> None:
        """Display title and board of a recently finished game."""
        if self.draw:
            clear_screen(time)
            self.board.display_game_title(True)
            self.board.display_board()
        elif not self.draw:
            clear_screen(time)
            self.board.display_game_title(False, True)
            self.board.display_board()

    def ask_play_again(self) -> None:
        """Ask the player to play again."""
        self.end_game_display(0)
        user_input = input("Play again? Y/N: ").upper()

        if user_input == "Y":
            if len(self.players_list) == 2:
                Game(self.board.game_counter + 1, self.board_length, list(reversed(self.players_list))).run()
            elif len(self.players_list) > 2:
                shifted_player = self.players_list.pop()
                self.players_list.insert(0, shifted_player)
                Game(self.board.game_counter + 1, self.board_length, self.players_list).run()
        elif user_input == "N":
            self.end_game_summary()
        else:
            self.ask_play_again()

    def save_replay(self, time=0) -> None:
        """Save a recently finished game."""
        self.end_game_display(time)
        filename = input(Fore.WHITE + Style.BRIGHT + "Filename: ")

        if filename == "":
            self.end_game_display(time)
            print(Fore.WHITE + Style.BRIGHT + "Filename: " + Fore.RED + Style.BRIGHT + "filename cannot be empty!")
            self.save_replay(1)
        else:
            # Create the folder if it does not exist
            try:
                os.makedirs('Replays')
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

            # Create the file
            file = open(f"{LOCAL_DIR_REPLAYS}{filename}{REPLAY_FILE_FORMAT}", 'w')
            file_content = bytes(str(self.replay_info), 'utf-8')

            for byte in file_content:
                file.write(f"{byte}\n")

            file.close()
            self.ask_play_again()

    def write_replay_file(self) -> None:
        """Write the replay files for the agent's simulated games."""
        # Create the folder if it does not exist
        try:
            os.makedirs('Replays')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        # Create the file
        file_title = " VS ".join([f"{i['name']} ({i['difficulty']})" if i['difficulty'] is not None else f"{i['name']}" for i in self.players_list]) + f" [{self.board_length}x{self.board_length}]"
        i = 1
        file_name = f"{LOCAL_DIR_REPLAYS}{file_title} {i}{REPLAY_FILE_FORMAT}"

        while os.path.exists(file_name):
            file_name = f"{LOCAL_DIR_REPLAYS}{file_title} {i}{REPLAY_FILE_FORMAT}"
            i += 1

        file = open(file_name, 'w')
        file_content = bytes(str(self.replay_info), 'utf-8')

        for byte in file_content:
            file.write(f"{byte}\n")

        file.close()

        if self.total_game_number > 1:
            Game(self.board.game_counter + 1, self.board_length, self.players_list, self.total_game_number - 1, True).run()
        else:
            self.end_game_summary()

    def end_game_event(self, time=1) -> None:
        """Trigger the end game event."""
        if self.sim:
            self.write_replay_file()
        else:
            self.end_game_display(time)

            user_input = input("Save replay? Y/N: ").upper()

            if user_input == "Y":
                self.save_replay()
            elif user_input == "N":
                self.ask_play_again()
            else:
                self.end_game_event(0)

    def win_event(self) -> None:
        """Trigger the win event."""
        self.board.winner = self.winner
        self.end_game_event()

    def draw_event(self) -> None:
        """Trigger the draw event."""
        self.draw = True

        for player in self.players_list:
            if player not in self.removed_players:
                player['stats']['draws'] += 1
                if player['type'] == 'human':
                    self.replay_info.append({"player_name": player['name'], "type": player['type'], "difficulty": None, "event": "DRAW", "starting_position": None, "selected_path": None, "word": None})
                else:
                    self.replay_info.append({"player_name": player['name'], "type": player['type'], "difficulty": player['difficulty'], "event": "DRAW", "starting_position": None,"selected_path": None, "word": None})

        self.end_game_event()

    def get_word(self) -> int:
        """Get word from the player."""
        path_length = len(self.board.selected_path)

        # Set valid characters
        regexp = re.compile('[^2-9a-zA-Z]+')

        # Get common letters
        common_letters = []

        for coord in self.board.selected_path:
            common_letters.append(self.board.matrix[coord])

        # Get word from player
        word = input(Fore.WHITE + Style.BRIGHT + f"Enter word with length of {path_length}: ").upper()

        # Check if the player resigns
        if word == "0":
            return 0
        # Check if the player wants to select another starting position
        elif word == "1":
            return 1
        else:
            # Check for numeric and special characters
            if regexp.search(word) or word.isnumeric() or word == "":
                self.board.display_selected_path()
                return self.get_word()
            # Compare the word length to the path length
            elif len(word) < path_length:
                self.board.display_selected_path()
                print(Fore.WHITE + Style.BRIGHT + f"Enter word with length of {path_length}: " + Fore.RED + Style.BRIGHT + "Word is too short!")
                self.board.display_selected_path(1)
                return self.get_word()
            elif len(word) > path_length:
                self.board.display_selected_path()
                print(Fore.WHITE + Style.BRIGHT + f"Enter word with length of {path_length}: " + Fore.RED + Style.BRIGHT + "Word is too long!")
                self.board.display_selected_path(1)
                return self.get_word()
            elif len(word) == path_length:
                # Check if word exist in game word list
                if word not in game_word_list[len(word)]:
                    self.board.display_selected_path()
                    print(Fore.WHITE + Style.BRIGHT + f"Enter word with length of {path_length}: " + Fore.RED + Style.BRIGHT + "That's not a word!")
                    self.board.display_selected_path(1)
                    return self.get_word()
                # Check if word exist in word list is used
                elif word in self.used_words:
                    self.board.display_selected_path()
                    print(Fore.WHITE + Style.BRIGHT + f"Enter word with length of {path_length}: " + Fore.RED + Style.BRIGHT + "That word has already been used!")
                    self.board.display_selected_path(1)
                    return self.get_word()
                else:
                    # Scan the path to get the letters
                    scanned_common_letters = common_letters

                    for i in range(len(scanned_common_letters)):
                        if scanned_common_letters[i] == " ":
                            scanned_common_letters.remove(scanned_common_letters[i])
                            scanned_common_letters.insert(i, word[i])

                    # Form the scanned word
                    scanned_word = ''.join(scanned_common_letters)

                    # If the letters of the player's word is in the scanned word
                    if word in scanned_word:
                        # If the scanned word is in the game word list
                        if scanned_word in game_word_list[path_length]:
                            self.board.place_word(word)
                            self.used_words.append(word)
                            self.board.used_words = self.used_words
                        else:
                            self.board.display_selected_path()
                            print(Fore.WHITE + Style.BRIGHT + f"Enter word with length of {path_length}: " + Fore.RED + Style.BRIGHT + "word not in order with the selected path!")
                            self.board.display_selected_path(1)
                            return self.get_word()
                    elif word in game_word_list[path_length]:
                        self.board.display_selected_path()
                        print(Fore.WHITE + Style.BRIGHT + f"Enter word with length of {path_length}: " + Fore.RED + Style.BRIGHT + "word not in order with the selected path!")
                        self.board.display_selected_path(1)
                        return self.get_word()

    def turn_handler(self, computer_player=None) -> int:
        """Handle the turns for each player."""
        # This is to make sure it does print the game twice on the same screen
        if self.first_turn or self.paths_full:
            clear_screen()
        else:
            clear_screen(0)

        # Check the type of player and direct them to their appropriate options
        if computer_player is None:
            player_starting_position = self.board.get_starting_position()

            if player_starting_position == 2:
                self.draw_event()
            elif player_starting_position == 0:
                return 0
            elif player_starting_position == 1:
                self.board.create_valid_paths()
                clear_screen(0)
                player_selected_path = self.board.get_selected_path()

                if player_selected_path == 0:
                    self.paths_full = False
                    return 0
                elif player_selected_path == 1:
                    self.paths_full = False
                    return self.turn_handler()
                elif player_selected_path == 2:
                    self.paths_full = True
                    return self.turn_handler()
                else:
                    self.paths_full = False
                    turn = self.get_word()

                    if turn == 0:
                        return 0
                    elif turn == 1:
                        return self.turn_handler()
            else:
                return self.turn_handler()
        else:
            self.board.display_game_title()
            self.board.display_board()
            computer_player.play()

            if computer_player.draw_detected:
                self.draw_event()
            else:
                if computer_player.final_selected_path is not None and computer_player.final_selected_word is not None:
                    self.board.selected_path = computer_player.final_selected_path
                    self.board.place_word(computer_player.final_selected_word)
                    self.used_words.append(computer_player.final_selected_word)
                else:
                    return 0

    def run(self) -> None:
        """Run the game."""
        current_players = self.players_list.copy()
        start_time = time.time()

        while True:
            # Check for a winner
            if len(current_players) < 2:
                if current_players[0]['type'] == "human":
                    self.winner = current_players[0]['name']
                else:
                    self.winner = f"{current_players[0]['name']} ({current_players[0]['difficulty']})"

                winner = current_players[0]
                winner['stats']['wins'] += 1

                if winner['type'] == 'human':
                    self.replay_info.append({"player_name": winner['name'], "type": winner['type'], "difficulty": None, "event": "WON", "selected_path": None, "word": None})
                else:
                    self.replay_info.append({"player_name": winner['name'], "type": winner['type'], "difficulty": winner['difficulty'], "event": "WON", "selected_path": None, "word": None})

                self.win_event()

            # Handle the turns for each player
            for player in current_players:
                if player['type'] == "human":
                    # Setup the human player
                    self.board.player = f"{player['name']}"
                    player_turn = self.turn_handler()

                    if player_turn == 0: # Do not add this statement to the computer player as the computer player never resigns on the first turn
                        if not self.first_turn:
                            self.first_turn = True
                        self.removed_players.append(player)
                        current_players.pop(current_players.index(player))
                        player['stats']['loses'] += 1
                        self.replay_info.append({"player_name": player['name'], "type": player['type'], "difficulty": None, "event": "RESIGNED", "selected_path": None, "word": None})
                        clear_screen(0)
                        self.board.display_game_title(False, False, True)
                        self.board.display_board()
                        break # Do not delete this as it handles the skips of indexing when iterating an modified list
                    else:
                        self.board.previous_player = player['name']
                        self.replay_info.append({"player_name": player['name'], "type": player['type'], "difficulty": None, "event": "PLAYING", "selected_path": self.board.selected_path, "word": self.board.word})
                        self.board.turn_counter += 1
                else:
                    if player['make'] == "official":
                        # Setup the computer player
                        self.board.player = f"{player['name']} ({player['difficulty']})"
                        computer_player = Official_Agent()
                        computer_player.agent_name = player['name']
                        computer_player.difficulty = player['difficulty']
                        computer_player.board_length = self.board_length
                        computer_player.analyse_board = copy.deepcopy(self.board)
                        computer_player.analyse_used_words = self.used_words.copy()
                        player_turn = self.turn_handler(computer_player)

                        if player_turn == 0:
                            self.removed_players.append(player)
                            current_players.pop(current_players.index(player))
                            player['stats']['loses'] += 1
                            self.replay_info.append({"player_name": player['name'], "type": player['type'], "difficulty": player['difficulty'], "event": "RESIGNED", "selected_path": None, "word": None})
                            clear_screen(0) # Do not delete!
                            self.board.display_game_title(False, False, True) # Do not delete!
                            self.board.display_board() # Do not delete!
                            clear_screen(1.5)
                            self.board.display_game_title(False, False, True)
                            self.board.display_board()
                            break # Do not delete this as it handles the skips of indexing when iterating an modified list
                        else:
                            self.board.previous_player = f"{player['name']} ({player['difficulty']})"
                            self.replay_info.append({"player_name": player['name'], "type": player['type'], "difficulty": player['difficulty'], "event": "PLAYING", "selected_path": self.board.selected_path, "word": self.board.word})
                            self.board.turn_counter += 1
                    else:
                        # Ini the custom agent here
                        pass

            elapsed_time = int(time.time() - start_time)
            game_duration = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
            self.board.game_duration = game_duration
            self.replay_info[0]['game_duration'] = game_duration

class Player:
    """Create an player object."""
    def __init__(self) -> None:
        self.players = []

    def get_difficulty(self, name: str) -> str:
        """Set difficulty of the computer player."""
        clear_screen(0)
        print(Fore.WHITE + Style.BRIGHT + f"Set difficulty for {name}\n[1] Easy\n[2] Medium\n[3] Hard\n[4] Go back to main menu\n")

        try:
            selection = int(input((Fore.WHITE + Style.BRIGHT + "Selection: ")))
            if selection == 1:
                return "EASY"
            elif selection == 2:
                return "MEDIUM"
            elif selection == 3:
                return "HARD"
            elif selection == 4:
                main()
            else:
                return self.get_difficulty(name)
        except ValueError:
            return self.get_difficulty(name)

    def get_player_name(self) -> str:
        """Get name from human players."""
        player_name = input(Fore.WHITE + Style.BRIGHT + f"Enter your name (max characters is {CHAR_LIMIT}): ")

        if player_name == "":
            clear_screen(0)
            print(Fore.WHITE + Style.BRIGHT + f"Enter your name (max characters is {CHAR_LIMIT}): " + Fore.RED + Style.BRIGHT + "Name cannot be empty!")
            clear_screen()
            return self.get_player_name()
        elif [i for i in self.players if i['name'] == player_name]:
            clear_screen(0)
            print(Fore.WHITE + Style.BRIGHT + f"Enter your name (max characters is {CHAR_LIMIT}): " + Fore.RED + Style.BRIGHT + "Name taken!")
            clear_screen()
            return self.get_player_name()
        elif len(player_name) > CHAR_LIMIT:
            clear_screen(0)
            print(Fore.WHITE + Style.BRIGHT + f"Enter your name (max characters is {CHAR_LIMIT}): " + Fore.RED + Style.BRIGHT + f"Name cannot exceed {CHAR_LIMIT} characters!")
            clear_screen()
            return self.get_player_name()
        else:
            return player_name

    def ask_if_custom_agent(self, n=None) -> None:
        """Ask if its an custom agent."""
        clear_screen(0)
        user_input = input("Playing against an custom agent? Y / N: ").upper()

        if user_input == "Y":
            if n is None:
                self.players.append({"name": f"{CUSTOM_COMPUTER_PLAYER_NAME}", "type": "computer","difficulty": self.get_difficulty(f"{CUSTOM_COMPUTER_PLAYER_NAME}"), "stats": {"wins": 0, "loses": 0, "draws": 0}, "make": "unofficial"})
            else:
                self.players.append({"name": f"{CUSTOM_COMPUTER_PLAYER_NAME} {n}", "type": "computer", "difficulty": self.get_difficulty(f"{CUSTOM_COMPUTER_PLAYER_NAME} {n}"), "stats": {"wins": 0, "loses": 0, "draws": 0}, "make": "unofficial"})
        elif user_input == "N":
            if n is None:
                self.players.append({"name": f"{COMPUTER_PLAYER_NAME}", "type": "computer","difficulty": self.get_difficulty(f"{COMPUTER_PLAYER_NAME}"),"stats": {"wins": 0, "loses": 0, "draws": 0}, "make": "official"})
            else:
                self.players.append({"name": f"{COMPUTER_PLAYER_NAME} {n}", "type": "computer", "difficulty": self.get_difficulty(f"{COMPUTER_PLAYER_NAME} {n}"), "stats": {"wins": 0, "loses": 0, "draws": 0}, "make": "official"})
        else:
            self.ask_if_custom_agent(n)

    def get_players(self, vs_computer=False, self_play=False) -> list:
        """"Create a list of players."""
        try:
            num_of_players = int(input((Fore.WHITE + Style.BRIGHT + "Number of players (Type 0 to go back to main menu): ")))

            if num_of_players == 0:
                main()
            elif num_of_players <= 1:
                clear_screen(0)
                print(Fore.WHITE + Style.BRIGHT + "Number of players (Type 0 to go back to main menu): " + Fore.RED + Style.BRIGHT + "Must have at least two players!")
                clear_screen()
                return self.get_players(vs_computer, self_play)
            else:
                if self_play:
                    for i in range(num_of_players):
                        self.ask_if_custom_agent(i + 1)
                else:
                    clear_screen(0)
                    player = {"name": self.get_player_name(), "type": "human", "difficulty": None, "stats": {"wins": 0, "loses": 0, "draws": 0}}
                    self.players.append(player)

                    if vs_computer:
                        if num_of_players > 2:
                            for i in range(num_of_players - 1):
                                self.ask_if_custom_agent(i + 1)
                        else:
                            self.ask_if_custom_agent()
                return self.players
        except ValueError:
            clear_screen(0)
            print(Fore.WHITE + Style.BRIGHT + "Number of players (Type 0 to go back to main menu): " + Fore.RED + Style.BRIGHT + "Must have at least two players!")
            clear_screen()
            return self.get_players(vs_computer, self_play)

def main():
    """The program."""
    # Create title bar
    ctypes.windll.kernel32.SetConsoleTitleW(f"{__title__} v{__version__}")

    # Cause the command prompt to open in maximize window by default
    user32 = ctypes.WinDLL('user32')
    hWnd = user32.GetForegroundWindow()
    user32.ShowWindow(hWnd, SW_MAXIMISE)

    # Disable QuickEdit and Insert mode by default
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128)

    # Run main menu
    while True:
        global game_word_list, vocab_1, vocab_2
        clear_screen(0)
        print(Fore.WHITE + Style.BRIGHT + f"{'-' * 32}\n{__title__} v{__version__}\nWritten in Python {PY_VERSION}\nDeveloped by {__author__}\n{'-' * 32}")
        menu_item = ["Play against agent", "Simulate agents", "Watch replays", "View README file", "Exit"]

        for i in menu_item:
            print([menu_item.index(i) + 1], i)

        selection = input("\nSelection: ")

        if selection == "1":
            check_if_file_exists('English.txt')
            check_if_file_exists('vocab_1.txt', True)
            check_if_file_exists('vocab_2.txt', True)
            game_word_list = categorise_word_by_length(open('English.txt').read().splitlines())
            vocab_1 = categorise_word_by_length(open(f'{LOCAL_DIR_VOCABULARY}vocab_1.txt').read().splitlines())
            vocab_2 = categorise_word_by_length(open(f'{LOCAL_DIR_VOCABULARY}vocab_2.txt').read().splitlines())
            clear_screen(0)
            board_length = get_board_length()
            clear_screen(0)
            players = Player().get_players(True, False)
            Game(1, board_length, players).run()
        elif selection == "2":
            check_if_file_exists('English.txt')
            check_if_file_exists('vocab_1.txt', True)
            check_if_file_exists('vocab_2.txt', True)
            game_word_list = categorise_word_by_length(open('English.txt').read().splitlines())
            vocab_1 = categorise_word_by_length(open(f'{LOCAL_DIR_VOCABULARY}vocab_1.txt').read().splitlines())
            vocab_2 = categorise_word_by_length(open(f'{LOCAL_DIR_VOCABULARY}vocab_2.txt').read().splitlines())
            clear_screen(0)
            board_length = get_board_length()
            clear_screen(0)
            players = Player().get_players(False, True)
            total_game_number = get_how_many_games()
            Game(1, board_length, players, total_game_number, True).run()
        elif selection == "3":
            clear_screen(0)
            open_replay()
        elif selection == "4":
            check_if_file_exists('README.txt')
            subprocess.call(['cmd', '/c', 'start', '/max', 'README.txt'])
        elif selection == "5":
            sys.exit(0)


if __name__ == "__main__":
    main()

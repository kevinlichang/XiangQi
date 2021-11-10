# Author: Kevin Chang
# Description: Creates a game call XiangQi. The game is played on a 9x10 board, with 7 different types of pieces
#  that have their own individual behaviors and rulesets. The goal of the game is to capture the enemy's general piece.
#  The game is over when a player's general piece has no spaces to move without being in check.

import pygame
from player import Player
from piece import General, Advisor, Elephant, Horse, Chariot, Cannon, Soldier


class XiangqiGame:
    """Represents the entire board for the XiangQi game."""

    def __init__(self):
        """Creates an instance of the 9x10 board."""
        self._board = [["_______" for column in range(9)] for row in range(10)]  # Initialize board
        self._row_dimensions = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        self._col_dimensions = (0, 1, 2, 3, 4, 5, 6, 7, 8)
        self._game_state = "UNFINISHED"

        # Initialize with red and black player. Game starts on red players turn.
        red_player = Player("red")
        blk_player = Player("black")

        self._red_player = red_player
        self._blk_player = blk_player
        self._current_player = self._red_player
        self._opp_player = self._blk_player

        # Initialize starting positions of pieces
        # Initialize General positions
        red_gen = General("GENERAL", [0, 4], "red", red_player, self._board)
        self._board[0][4] = red_gen
        blk_gen = General("GENERAL", [9, 4], "black", blk_player, self._board)
        self._board[9][4] = blk_gen

        # Initialize Advisor pieces
        red_advisor1 = Advisor("ADVISOR", [0, 3], "red", red_player, self._board)
        self._board[0][3] = red_advisor1
        red_advisor2 = Advisor("ADVISOR", [0, 5], "red", red_player, self._board)
        self._board[0][5] = red_advisor2
        blk_advisor1 = Advisor("ADVISOR", [9, 3], "black", blk_player, self._board)
        self._board[9][3] = blk_advisor1
        blk_advisor2 = Advisor("ADVISOR", [9, 5], "black", blk_player, self._board)
        self._board[9][5] = blk_advisor2

        # Initialize Elephant pieces
        red_elephant1 = Elephant("ELEPHNT", [0, 2], "red", red_player, self._board)
        self._board[0][2] = red_elephant1
        red_elephant2 = Elephant("ELEPHNT", [0, 6], "red", red_player, self._board)
        self._board[0][6] = red_elephant2
        blk_elephant1 = Elephant("ELEPHNT", [9, 2], "black", blk_player, self._board)
        self._board[9][2] = blk_elephant1
        blk_elephant2 = Elephant("ELEPHNT", [9, 6], "black", blk_player, self._board)
        self._board[9][6] = blk_elephant2

        # Initialize Horse pieces
        red_horse1 = Horse("HORSE", [0, 1], "red", red_player, self._board)
        self._board[0][1] = red_horse1
        red_horse2 = Horse("HORSE", [0, 7], "red", red_player, self._board)
        self._board[0][7] = red_horse2
        blk_horse1 = Horse("HORSE", [9, 1], "black", blk_player, self._board)
        self._board[9][1] = blk_horse1
        blk_horse2 = Horse("HORSE", [9, 7], "black", blk_player, self._board)
        self._board[9][7] = blk_horse2

        # Initialize Chariot pieces
        red_chariot1 = Chariot("CHARIOT", [0, 0], "red", red_player, self._board)
        self._board[0][0] = red_chariot1
        red_chariot2 = Chariot("CHARIOT", [0, 8], "red", red_player, self._board)
        self._board[0][8] = red_chariot2
        blk_chariot1 = Chariot("CHARIOT", [9, 8], "black", blk_player, self._board)
        self._board[9][0] = blk_chariot1
        blk_chariot2 = Chariot("CHARIOT", [9, 8], "black", blk_player, self._board)
        self._board[9][8] = blk_chariot2

        # Initialize Cannon pieces
        red_cannon1 = Cannon("CANNON", [2, 1], "red", red_player, self._board)
        self._board[2][1] = red_cannon1
        red_cannon2 = Cannon("CANNON", [2, 7], "red", red_player, self._board)
        self._board[2][7] = red_cannon2
        blk_cannon1 = Cannon("CANNON", [7, 1], "black", blk_player, self._board)
        self._board[7][1] = blk_cannon1
        blk_cannon2 = Cannon("CANNON", [7, 7], "black", blk_player, self._board)
        self._board[7][7] = blk_cannon2

        # Initialize Soldier pieces
        red_soldier1 = Soldier("SOLDIER", [3, 0], "red", red_player, self._board)
        self._board[3][0] = red_soldier1
        red_soldier2 = Soldier("SOLDIER", [3, 2], "red", red_player, self._board)
        self._board[3][2] = red_soldier2
        red_soldier3 = Soldier("SOLDIER", [3, 4], "red", red_player, self._board)
        self._board[3][4] = red_soldier3
        red_soldier4 = Soldier("SOLDIER", [3, 6], "red", red_player, self._board)
        self._board[3][6] = red_soldier4
        red_soldier5 = Soldier("SOLDIER", [3, 8], "red", red_player, self._board)
        self._board[3][8] = red_soldier5
        blk_soldier1 = Soldier("SOLDIER", [6, 0], "black", blk_player, self._board)
        self._board[6][0] = blk_soldier1
        blk_soldier2 = Soldier("SOLDIER", [6, 2], "black", blk_player, self._board)
        self._board[6][2] = blk_soldier2
        blk_soldier3 = Soldier("SOLDIER", [6, 4], "black", blk_player, self._board)
        self._board[6][4] = blk_soldier3
        blk_soldier4 = Soldier("SOLDIER", [6, 6], "black", blk_player, self._board)
        self._board[6][6] = blk_soldier4
        blk_soldier5 = Soldier("SOLDIER", [6, 8], "black", blk_player, self._board)
        self._board[6][8] = blk_soldier5

        # Add starting pieces to respective player active pieces lists
        red_player.set_active_pieces([red_gen,
                                      red_advisor1, red_advisor2,
                                      red_elephant1, red_elephant2,
                                      red_horse1, red_horse2,
                                      red_chariot1, red_chariot2,
                                      red_cannon1, red_cannon2,
                                      red_soldier1, red_soldier2, red_soldier3, red_soldier4, red_soldier5])
        blk_player.set_active_pieces([blk_gen,
                                      blk_advisor1, blk_advisor2,
                                      blk_elephant1, blk_elephant2,
                                      blk_horse1, blk_horse2,
                                      blk_chariot1, blk_chariot2,
                                      blk_cannon1, blk_cannon2,
                                      blk_soldier1, blk_soldier2, blk_soldier3, blk_soldier4, blk_soldier5])

        self._red_general = red_gen
        self._blk_general = blk_gen

    def get_game_state(self):
        """Returns the game state."""
        return self._game_state

    def set_game_state(self, red_or_black):
        """Sets the game state depending on color specified."""
        if red_or_black == "red":
            self._game_state = "RED_WON"
        elif red_or_black == "black":
            self._game_state = "BLACK_WON"

    def is_in_check(self, red_or_black):
        """Returns True if a player is in check, else False."""
        if self._current_player.get_player_color() == red_or_black:
            return self._current_player.get_check_status()
        else:
            return self._opp_player.get_check_status()

    def get_board(self):
        """Returns the current board."""
        return self._board

    def print_board(self):
        """Prints out the current board instance."""
        for row in range(10):
            for col in range(9):
                if row == 9 and col == 8:
                    if self._board[row][col] != "_______":
                        print(self._board[row][col].get_name())
                    else:
                        print(self._board[row][col])
                else:
                    if self._board[row][col] != "_______":
                        print(self._board[row][col].get_name(), end=" ")
                    else:
                        print(self._board[row][col], end=" ")
            if row != 9:
                print(" ")
                print(" ")
            if row == 4:
                print(" ")
                print(" ")

    def change_turn(self):
        """Changes the current player turn to the other player."""
        if self._current_player == self._red_player:
            self._current_player = self._blk_player
        else:
            self._current_player = self._red_player

        if self._opp_player == self._red_player:
            self._opp_player = self._blk_player
        else:
            self._opp_player = self._red_player


    def general_sight_test(self, num=1):
        """
        Checks that the generals do not 'see' each other (no blocking pieces between generals), which is illegal.
        :param num: used to keep track of spot being checked during recursion.
        :return: True if generals 'see' each other. Else False
        """
        # Get red and black General Current Positions (gcp)
        red_gcp = self._red_general.get_position()
        blk_gcp = self._blk_general.get_position()

        if red_gcp[1] == blk_gcp[1]:  # If the generals are in same column
            spaces = blk_gcp[0] - red_gcp[0]

            if num == spaces:  # Base case: if no blocking pieces, Generals see each other.
                debug("Illegal move. Generals see each other.")
                return True

            if self._board[red_gcp[0] + num][red_gcp[1]] == "_______":
                return self.general_sight_test(num + 1)
        # debug("Generals do not see each other")
        return False

    def all_pieces_move_test(self, player, pos):
        """
        Checks to see if any of a Player's active pieces can move to a specified position.
        :param player: the player whose pieces are being tested
        :param pos: the specified position
        :return: True if at least one piece can move to specified spot. False if no pieces can.
        """
        pieces_list = player.get_active_pieces()  # List of all active pieces of the Player

        for piece in pieces_list:
            if piece.legal_move_test(pos) == True:
                debug(piece.get_name(), "can move there.")
                return True

        return False

    def in_check_test(self, testing_player, enemy):
        """
        Tests if a General piece is in check.
        :param testing_player: Player whose general is being tested for being in check or not.
        :param enemy: The opponent of the tested player
        :return: True if general is in check. Else False.
        """
        if self._red_general.get_piece_color() == testing_player.get_player_color():
            gen = self._red_general
        elif self._blk_general.get_piece_color() == testing_player.get_player_color():
            gen = self._blk_general

        gp = gen.get_position()  # get current player General's position

        return self.all_pieces_move_test(enemy, gp)

    def end_game_test(self, testing_player, enemy):
        """
        Tests to see if a player is in checkmate or in a stalemate
        :param in_check_player: The player that is in check that is being tested
        :param enemy: the opponent of the tested player
        :return: True if player is checkmated or in stalemate and ending the game. Else False
        """
        # Get the correct player color and corresponding general piece and palace coordinates
        if self._red_general.get_piece_color() == testing_player.get_player_color():
            gen = self._red_general
            palace = ([0, 3], [0, 4], [0, 5], [1, 3], [1, 4], [1, 5], [2, 3], [2, 4], [2, 5])

        elif self._blk_general.get_piece_color() == testing_player.get_player_color():
            gen = self._blk_general
            palace = ([7, 3], [7, 4], [7, 5], [8, 3], [8, 4], [8, 5], [9, 3], [9, 4], [9, 5])

        board = self._board
        color = testing_player.get_player_color()
        pieces_list = testing_player.get_active_pieces()

        # Test each spot in the palace to see if the general can move there.
        # If the general can move there, test to see if it would still be in check in that spot
        # If there is a spot that is not in check, return False
        for spot in palace:
            if gen.legal_move_test(spot) == True and spot != gen.get_position():
                if board[spot[0]][spot[1]] == "_______" or board[spot[0]][spot[1]].get_piece_color() != color:
                    if self.all_pieces_move_test(enemy, spot) == False:
                        return False

        # If the in-check player has more pieces besides just the general, check all other active pieces for
        # potential moves that can get the player out of check.
        if len(pieces_list) > 1:
            for num in range(1, len(pieces_list)):
                for row in self._row_dimensions:
                    for col in self._col_dimensions:
                        piece = pieces_list[num]
                        if piece.legal_move_test([row, col]) == True:
                            if board[row][col] == "_______" or board[row][col].get_piece_color() != color:
                                o_pos = piece.get_position()  # Original Position of the current piece
                                holder = board[row][col]  # Holding onto the test spot's original state

                                board[o_pos[0]][
                                    o_pos[1]] = "_______"  # Temporarily move the testing piece to do a in check test
                                board[row][col] = piece

                                check_test = self.in_check_test(testing_player, enemy)

                                board[row][col] = holder  # Return the board to original state
                                board[o_pos[0]][o_pos[1]] = piece

                                if check_test == False:  # If the move places general out of check, return False
                                    return False

        debug("Checkmate!", enemy.get_player_color(), "wins.")
        return True

    def make_move(self, curr_pos, new_pos):
        """
        Makes a move for current player on a piece
        :param curr_pos: the current position of piece to be moved
        :param new_pos: the new position the piece is moving to
        :return: True if move is legal. Else return False
        """
        if self.get_game_state() != "UNFINISHED":
            debug("Game Over", self.get_game_state())
            return False

        board = self._board

        # Convert input strings into coordinates on the board
        cp = curr_pos  # current position coordinates as a list
        np = new_pos   # intended new position coordinates as a list

        # Check if inputted positions are inside board dimensions
        if cp[0] not in self._row_dimensions or cp[1] not in self._col_dimensions:
            debug("Selection is outside of board")
            return False
        if np[0] not in self._row_dimensions or np[1] not in self._col_dimensions:
            debug("Move is outside of the board")
            return False

        # Check if there is even a piece at current position selected
        if board[cp[0]][cp[1]] == "_______":
            debug("There is no piece selected")
            return False

        if cp == np:  # Return False if new_pos is same as curr_pos
            debug("No new move made")
            return False

        piece = board[cp[0]][cp[1]]  # Get the piece that is selected
        move_spot = board[np[0]][np[1]]  # The spot the player intends to move to

        # Check if piece selected belongs to the current player
        if piece.get_player() != self._current_player:
            debug("Player can only move their own pieces.")
            return False

        if move_spot != "_______" and move_spot.get_player() == piece.get_player():
            debug("Player cannot eat their own piece.")
            return False

        if piece.legal_move_test(np) is False:  # Check if new_pos is legal to the piece
            debug("Illegal move")
            return False

        # Make the move and change piece position. Then test for check status, checkmates, or generals' sightlines.
        board[cp[0]][cp[1]] = "_______"
        board[np[0]][np[1]] = piece
        piece.set_position(np)

        # Check if generals "see" each other
        if self.general_sight_test() == True:
            board[cp[0]][cp[1]] = piece  # Reset original positions
            piece.set_position(cp)
            board[np[0]][np[1]] = "_______"
            return False

        # Check if current player's own General would be in check
        if self.in_check_test(self._current_player, self._opp_player) == True:
            board[cp[0]][cp[1]] = piece  # Reset original positions
            piece.set_position(cp)
            board[np[0]][np[1]] = "_______"
            debug("Cannot move there. You're General would be in check.")
            return False

        # Check if opponent player's general is in check
        if self.in_check_test(self._opp_player, self._current_player) == True:
            self._opp_player.set_check_status(True)
            debug(self._opp_player.get_player_color(), "player in check.")

        # If there is a piece to be taken on the new position
        if move_spot != "_______":
            enemy = move_spot.get_player()
            enemy.piece_taken(move_spot)

        # If the current player was in check, reset in check status to False after the current move.
        if self._current_player.get_check_status() == True:
            self._current_player.set_check_status(False)
            debug(self._current_player.get_player_color(), "player no longer in check.")

        debug(piece.get_name(), " moved to ", piece.get_position())

        self.change_turn()  # Swap the current and opponent player slots.

        # Test to see if next player is checkmated or in stalemate. If True, then game is over.
        if self.end_game_test(self._current_player, self._opp_player) == True:
            self.set_game_state(self._opp_player.get_player_color())

        return True

    def show_turns(self):
        debug("Current", self._current_player.get_player_color())
        debug("Opponent", self._opp_player.get_player_color())


def debug(msg1, msg2="", msg3="", msg4=""):
    DEBUG = True
    if DEBUG == True:
        print(msg1, msg2, msg3, msg4)


# Define some colors
BGC = (0, 0, 0)
BLACK = (50, 50, 50)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 70
HEIGHT = 70

# This sets the margin between each cell
MARGIN = 5


# Initialize pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [680, 755]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("XiangQi Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

game = XiangqiGame()
grid = game.get_board()
pos_holder = []
board_coord = []
# -------- Main Program Loop -----------
while not done:

    font = pygame.font.SysFont('Calibri', 18, False, False)

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            pos_holder = [pos[0], pos[1]]
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            # Set that location to one
            if not board_coord:
                board_coord = [row, column]
            else:
                game.make_move(board_coord, [row, column])
                board_coord = []
            print("Click ", pos, "Grid coordinates: ", row, column)

    # Set the screen background
    screen.fill(BGC)

    # Draw the grid
    for row in range(10):
        for column in range(9):
            color = WHITE
            piece = grid[row][column]
            piece_name = ""
            if piece != "_______":
                piece_name = piece.get_name()
                if piece.get_piece_color() == "red":
                    color = RED
                else:
                    color = BLACK
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

            text = font.render(piece_name, True, WHITE)

            screen.blit(text, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN])

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
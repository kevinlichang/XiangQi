# Author: Kevin Chang
# Description: Creates a game call XiangQi. The game is played on a 9x10 board, with 7 different types of pieces
#  that have their own individual behaviors and rulesets. The goal of the game is to capture the enemy's general piece.
#  The game is over when a player's general piece has no spaces to move without being in check.

import pygame

class Player:
    """Represents a player of the XiangQi game."""

    def __init__(self, red_or_black):
        """Creates one of the Players of the game."""
        self._color = red_or_black
        self._active_pieces = []
        self._inactive_pieces = []
        self._in_check_status = False

    def set_active_pieces(self, pieces):
        """Sets the active pieces list of the player. Used during initialization."""
        self._active_pieces = pieces

    def get_player_color(self):
        """Returns the player's color."""
        return self._color

    def get_check_status(self):
        """Returns True if player is in check, otherwise returns False."""
        return self._in_check_status

    def set_check_status(self, status):
        """Sets the status of in check of the player."""
        self._in_check_status = status

    def piece_taken(self, piece):
        """Removes a piece from active to inactive lists when taken by opponent."""
        self._inactive_pieces.append(piece)
        self._active_pieces.remove(piece)
        debug(piece.get_name() + " taken.")
        return True

    def get_active_pieces(self):
        """Returns the list of active pieces of the Player."""
        return self._active_pieces

    def print_active_pieces(self):
        for p in self._active_pieces:
            debug(p.get_name())

    def get_inactive_pieces(self):
        for p in self._inactive_pieces:
            debug(p.get_name())


class Piece:
    """Represents a piece on the game board."""

    def __init__(self, name, pos, red_or_black, player, board):
        """Creates a new Piece on the board."""
        self._name = name
        self._position = pos
        self._color = red_or_black
        self._player = player
        self._board = board

    def get_name(self):
        """Returns the name of the piece."""
        return self._name

    def get_position(self):
        """Returns the current position of the piece."""
        return self._position

    def set_position(self, pos):
        """Sets the new position of current piece if moved."""
        self._position = pos

    def get_piece_color(self):
        """Returns the color of the current piece."""
        return self._color

    def get_player(self):
        """Returns the Player that owns the piece."""
        return self._player


class General(Piece):
    """Represents the General piece on the board."""

    def __init__(self, name, pos, red_or_black, player, board):
        """Creates a new General piece."""
        super().__init__(name, pos, red_or_black, player, board)

    def legal_move_test(self, new_pos):
        """Tests if an intended move is legal for the piece. Return True if legal, else False."""

        red_palace = ([0, 3], [0, 4], [0, 5], [1, 3], [1, 4], [1, 5], [2, 3], [2, 4], [2, 5])
        black_palace = ([7, 3], [7, 4], [7, 5], [8, 3], [8, 4], [8, 5], [9, 3], [9, 4], [9, 5])

        cp = self._position  # Holds the current position of the piece before move

        # Check to make sure move is inside the palace
        if self._color == "red":
            if new_pos not in red_palace:
                # debug("The GENERAL must stay in the palace")
                return False
        elif self._color == "black":
            if new_pos not in black_palace:
                # debug("The GENERAL must stay in the palace")
                return False

        # check if the move is orthogonal
        if new_pos != [cp[0] + 1, cp[1]] and new_pos != [cp[0] - 1, cp[1]] and new_pos != [cp[0],
                                                                                           cp[1] + 1] and new_pos != [
            cp[0], cp[1] - 1]:
            # debug("The GENERAL can only move one space orthogonally")
            return False

        return True


class Advisor(Piece):
    """Represents the Advisor Piece on the board."""

    def __init__(self, name, pos, red_or_black, player, board):
        """Creates a new Advisor piece."""
        super().__init__(name, pos, red_or_black, player, board)

    def legal_move_test(self, new_pos):
        """Tests if an intended move is legal for the piece. Return True if legal, else False."""
        red_palace = ([0, 3], [0, 4], [0, 5], [1, 3], [1, 4], [1, 5], [2, 3], [2, 4], [2, 5])
        black_palace = ([7, 3], [7, 4], [7, 5], [8, 3], [8, 4], [8, 5], [9, 3], [9, 4], [9, 5])

        cp = self._position  # Holds the current position of the piece before move

        # Check to make sure move is inside the palace
        if self._color == "red":
            if new_pos not in red_palace:
                # debug("ADVISORS must stay in the palace")
                return False
        elif self._color == "black":
            if new_pos not in black_palace:
                # debug("ADVISORS must stay in the palace")
                return False

        # Check if move is diagonal
        if new_pos == [cp[0] + 1, cp[1] + 1] or new_pos == [cp[0] - 1, cp[1] + 1] or new_pos == [cp[0] + 1, cp[
                                                                                                                1] + 1] or new_pos == [
            cp[0] + 1, cp[1] - 1]:
            return True

        # debug("Advisors can only move one space diagonally")
        return False


class Elephant(Piece):
    """Represents the Elephant Piece on the board."""

    def __init__(self, name, pos, red_or_black, player, board):
        """Creates a new Elephant piece."""
        super().__init__(name, pos, red_or_black, player, board)

    def legal_move_test(self, new_pos):
        """Tests if an intended move is legal for the piece. Return True if legal, else False."""
        cp = self._position  # Holds the current position of the piece before move

        # Check if new_pos is past the river. Elephant cannot cross river
        if self._color == "red":
            if new_pos[0] > 4:
                # debug("ELEPHANTS cannot cross the River")
                return False
        elif self._color == "black":
            if new_pos[0] < 5:
                # debug("ELEPHANTS cannot cross the River")
                return False

        # list of legal possible moves for Elephant
        new_pos_test_list = [[cp[0] + 2, cp[1] + 2], [cp[0] + 2, cp[1] - 2], [cp[0] - 2, cp[1] + 2],
                             [cp[0] - 2, cp[1] - 2]]
        # List of positions that need to be checked for blocking pieces
        coord = [[cp[0] + 1, cp[1] + 1], [cp[0] + 1, cp[1] - 1], [cp[0] - 1, cp[1] + 1], [cp[0] - 1, cp[1] - 1]]

        # Check if move is 2 spaces diagonal. CANNOT JUMP OVER BLOCKING PIECE (One space diagonal would be blocking)
        for num in range(4):
            if new_pos == new_pos_test_list[num]:
                if self._board[coord[num][0]][coord[num][1]] != "_______":
                    # debug("ELEPHANT IS BLOCKED")
                    return False
                else:
                    return True

        # debug("ELEPHANTS only move 2 spaces diagonally.")
        return False


class Horse(Piece):
    """Represents the Horse Piece on the board."""

    def __init__(self, name, pos, red_or_black, player, board):
        """Creates a new Horse piece."""
        super().__init__(name, pos, red_or_black, player, board)

    def legal_move_test(self, new_pos):
        """Tests if an intended move is legal for the piece. Return True if legal, else False."""
        cp = self._position  # Holds the current position of the piece before move

        # list of legal possible moves for Horse
        new_pos_test_list = [[cp[0] + 2, cp[1] + 1], [cp[0] + 2, cp[1] - 1], [cp[0] - 2, cp[1] + 1],
                             [cp[0] - 2, cp[1] - 1],
                             [cp[0] + 1, cp[1] + 2], [cp[0] - 1, cp[1] + 2], [cp[0] + 1, cp[1] - 2],
                             [cp[0] - 1, cp[1] - 2]]

        # List of positions that need to be checked for blocking pieces
        coord = [[cp[0] + 1, cp[1]], [cp[0] - 1, cp[1]], [cp[0], cp[1] + 1], [cp[0], cp[1] - 1]]
        tracker = 0
        for num in range(8):
            if new_pos == new_pos_test_list[num]:
                if self._board[coord[tracker][0]][coord[tracker][1]] != "_______":
                    # debug("HORSE IS BLOCKED")
                    return False
                else:
                    return True

            if num % 2 != 0:
                tracker += 1

        # debug("Horse cannot move there")
        return False


class Chariot(Piece):
    """Represents the Chariot Piece on the board."""

    def __init__(self, name, pos, red_or_black, player, board):
        """Creates a new Chariot piece."""
        super().__init__(name, pos, red_or_black, player, board)

    def legal_move_test(self, new_pos, num=1):
        """
        Tests if an intended move is legal for the piece.
        :param new_pos: Intended new position.
        :param num: used to track space being checked in recursion.
        :return: True if move is legal. Else, returns False.
        """
        cp = self._position  # Holds the current position of the piece before move

        if cp[0] == new_pos[0]:  # When moving horizontal
            spaces = cp[1] - new_pos[1]  # Get the amount of spaces the chariot is moving
            if spaces < 0:
                spaces *= -1

            if num == spaces:  # Base Case when reach final check
                return True

            # Check if there is any blocking pieces in between new_pos and current pos
            if cp[1] > new_pos[1]:  # Leftward movement
                if self._board[cp[0]][cp[1] - num] == "_______":
                    return self.legal_move_test(new_pos, num + 1)
                else:
                    # debug("CHARIOT IS BLOCKED FROM MOVING LEFT")
                    return False
            elif cp[1] < new_pos[1]:  # Rightward movement
                if self._board[cp[0]][cp[1] + num] == "_______":
                    return self.legal_move_test(new_pos, num + 1)
                else:
                    # debug("CHARIOT IS BLOCKED FROM MOVING RIGHT")
                    return False
        elif cp[1] == new_pos[1]:  # When moving vertical
            spaces = cp[0] - new_pos[0]  # Get the amount of spaces the chariot is moving
            if spaces < 0:
                spaces *= -1

            if num == spaces:  # Base case when reach final check
                return True

            # Check if there is any blocking pieces in between new_pos and current pos
            if cp[0] > new_pos[0]:  # Upward movement
                if self._board[cp[0] - num][cp[1]] == "_______":
                    return self.legal_move_test(new_pos, num + 1)
                else:
                    # debug("CHARIOT IS BLOCKED FROM MOVING UP")
                    return False
            elif cp[0] < new_pos[0]:  # Downward movement
                if self._board[cp[0] + num][cp[1]] == "_______":
                    return self.legal_move_test(new_pos, num + 1)
                else:
                    # debug("CHARIOT IS BLOCKED FROM MOVING DOWN")
                    return False
        # debug("CHARIOT CAN ONLY MOVE ORTHOGONALLY")
        return False


class Cannon(Piece):
    """Represents the Cannon Piece on the board."""

    def __init__(self, name, pos, red_or_black, player, board):
        """Creates a new Cannon piece."""
        super().__init__(name, pos, red_or_black, player, board)

    def legal_move_test(self, new_pos, num=1, tracker=0):
        """
        Tests if an intended move is legal for the piece.
        :param new_pos: Intended new position.
        :param num: used to track space being checked in recursion.
        :param tracker: used to track if there is one piece to jump over in order to take opposing piece.
        :return: True if move is legal. Else, returns False.
        """
        cp = self._position  # Holds the current position of the piece before move
        if self._board[new_pos[0]][new_pos[1]] != "_______":  # When trying to take an enemy piece
            if cp[0] == new_pos[0]:  # When moving horizontal
                spaces = cp[1] - new_pos[1]  # Get the amount of spaces the chariot is moving
                if spaces < 0:
                    spaces *= -1

                if num == spaces:
                    if tracker == 1:  # Base case
                        return True
                    else:
                        # debug("Cannon must jump over a piece to take pieces.")
                        return False

                # Check for a piece to jump over
                if cp[1] > new_pos[1]:  # Leftward movement
                    if self._board[cp[0]][cp[1] - num] == "_______":  # If space being checked is empty
                        return self.legal_move_test(new_pos, num + 1, tracker)
                    else:
                        if tracker < 1:  # If there is a piece in space being checked
                            tracker += 1
                            return self.legal_move_test(new_pos, num + 1, tracker)
                        else:
                            # debug("Cannon cannot jump over 2 pieces.")
                            return False
                elif cp[1] < new_pos[1]:  # Rightward movement
                    if self._board[cp[0]][cp[1] + num] == "_______":  # If space being checked is empty
                        return self.legal_move_test(new_pos, num + 1, tracker)
                    else:
                        if tracker < 1:  # If there is a piece in space being checked
                            tracker += 1
                            return self.legal_move_test(new_pos, num + 1, tracker)
                        else:
                            # debug("Cannon cannot jump over 2 pieces.")
                            return False
            elif cp[1] == new_pos[1]:  # When moving vertical
                spaces = cp[0] - new_pos[0]  # Get the amount of spaces the chariot is moving
                if spaces < 0:
                    spaces *= -1

                if num == spaces:
                    if tracker == 1:  # Base case
                        return True
                    else:
                        # debug("Cannon must jump over a piece to take pieces.")
                        return False

                # Check for a piece to jump over
                if cp[0] > new_pos[0]:  # Leftward movement
                    if self._board[cp[0] - num][cp[1]] == "_______":  # If space being checked is empty
                        return self.legal_move_test(new_pos, num + 1, tracker)
                    else:
                        if tracker < 1:  # If there is a piece in space being checked
                            tracker += 1
                            return self.legal_move_test(new_pos, num + 1, tracker)
                        else:
                            # debug("Cannon cannot jump over 2 pieces.")
                            return False
                elif cp[0] < new_pos[0]:  # Rightward movement
                    if self._board[cp[0] + num][cp[1]] == "_______":  # If space being checked is empty
                        return self.legal_move_test(new_pos, num + 1, tracker)
                    else:
                        if tracker < 1:  # If there is a piece in space being checked
                            tracker += 1
                            return self.legal_move_test(new_pos, num + 1, tracker)
                        else:
                            # debug("Cannon cannot jump over 2 pieces.")
                            return False

        elif self._board[new_pos[0]][new_pos[1]] == "_______":  # When new_pos is clear
            if cp[0] == new_pos[0]:  # When moving horizontal
                spaces = cp[1] - new_pos[1]  # Get the amount of spaces the chariot is moving
                if spaces < 0:
                    spaces *= -1

                if num == spaces:  # Base Case when reach final check
                    return True

                # Check if there is any blocking pieces in between new_pos and current pos
                if cp[1] > new_pos[1]:  # Leftward movement
                    if self._board[cp[0]][cp[1] - num] == "_______":
                        return self.legal_move_test(new_pos, num + 1)
                    else:
                        # debug("CANNON IS BLOCKED FROM MOVING LEFT")
                        return False
                elif cp[1] < new_pos[1]:  # Rightward movement
                    if self._board[cp[0]][cp[1] + num] == "_______":
                        return self.legal_move_test(new_pos, num + 1)
                    else:
                        # debug("CANNON IS BLOCKED FROM MOVING RIGHT")
                        return False
            elif cp[1] == new_pos[1]:  # When moving vertical
                spaces = cp[0] - new_pos[0]  # Get the amount of spaces the chariot is moving
                if spaces < 0:
                    spaces *= -1

                if num == spaces:  # Base case when reach final check
                    return True

                # Check if there is any blocking pieces in between new_pos and current pos
                if cp[0] > new_pos[0]:  # Upward movement
                    if self._board[cp[0] - num][cp[1]] == "_______":
                        return self.legal_move_test(new_pos, num + 1)
                    else:
                        # debug("CANNON IS BLOCKED FROM MOVING UP")
                        return False
                elif cp[0] < new_pos[0]:  # Downward movement
                    if self._board[cp[0] + num][cp[1]] == "_______":
                        return self.legal_move_test(new_pos, num + 1)
                    else:
                        # debug("CANNON IS BLOCKED FROM MOVING DOWN")
                        return False
        # debug("CANNON CAN ONLY MOVE ORTHOGONALLY")
        return False


class Soldier(Piece):
    """Represents a Soldier Piece on the board."""

    def __init__(self, name, pos, red_or_black, player, board):
        """Creates a new General piece."""
        super().__init__(name, pos, red_or_black, player, board)
        self._past_river = False

    def past_river_check(self):
        """Checks if the soldier is past the river."""
        if self._color == "red":
            if self._position[0] > 4:
                self._past_river = True
        elif self._color == "black":
            if self._position[0] < 5:
                self._past_river = True

    def legal_move_test(self, new_pos):
        """Tests if an intended move is legal for the piece. Return True if legal, else False."""
        cp = self._position  # Holds current soldier position

        # If the new move is one space horizontal, check if Soldier is past river to be a legal move
        if self._past_river == False:
            self.past_river_check()
        elif self._past_river == True:
            if new_pos == [cp[0], cp[1] + 1] or new_pos == [cp[0], cp[1] - 1]:
                return True

        if self._color == "red":
            if new_pos == [cp[0] + 1, cp[1]]:
                return True
        elif self._color == "black":
            if new_pos == [cp[0] - 1, cp[1]]:
                return True

        # debug("The soldier cannot move there")
        return False


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
        red_gen = General("RED_GEN", [0, 4], "red", red_player, self._board)
        self._board[0][4] = red_gen
        blk_gen = General("BLK_GEN", [9, 4], "black", blk_player, self._board)
        self._board[9][4] = blk_gen

        # Initialize Advisor pieces
        red_advisor1 = Advisor("RED_ADV", [0, 3], "red", red_player, self._board)
        self._board[0][3] = red_advisor1
        red_advisor2 = Advisor("RED_ADV", [0, 5], "red", red_player, self._board)
        self._board[0][5] = red_advisor2
        blk_advisor1 = Advisor("BLK_ADV", [9, 3], "black", blk_player, self._board)
        self._board[9][3] = blk_advisor1
        blk_advisor2 = Advisor("BLK_ADV", [9, 5], "black", blk_player, self._board)
        self._board[9][5] = blk_advisor2

        # Initialize Elephant pieces
        red_elephant1 = Elephant("RED_ELE", [0, 2], "red", red_player, self._board)
        self._board[0][2] = red_elephant1
        red_elephant2 = Elephant("RED_ELE", [0, 6], "red", red_player, self._board)
        self._board[0][6] = red_elephant2
        blk_elephant1 = Elephant("BLK_ELE", [9, 2], "black", blk_player, self._board)
        self._board[9][2] = blk_elephant1
        blk_elephant2 = Elephant("BLK_ELE", [9, 6], "black", blk_player, self._board)
        self._board[9][6] = blk_elephant2

        # Initialize Horse pieces
        red_horse1 = Horse("RED_HOR", [0, 1], "red", red_player, self._board)
        self._board[0][1] = red_horse1
        red_horse2 = Horse("RED_HOR", [0, 7], "red", red_player, self._board)
        self._board[0][7] = red_horse2
        blk_horse1 = Horse("BLK_HOR", [9, 1], "black", blk_player, self._board)
        self._board[9][1] = blk_horse1
        blk_horse2 = Horse("BLK_HOR", [9, 7], "black", blk_player, self._board)
        self._board[9][7] = blk_horse2

        # Initialize Chariot pieces
        red_chariot1 = Chariot("RED_CHA", [0, 0], "red", red_player, self._board)
        self._board[0][0] = red_chariot1
        red_chariot2 = Chariot("RED_CHA", [0, 8], "red", red_player, self._board)
        self._board[0][8] = red_chariot2
        blk_chariot1 = Chariot("BLK_CHA", [9, 8], "black", blk_player, self._board)
        self._board[9][0] = blk_chariot1
        blk_chariot2 = Chariot("BLK_CHA", [9, 8], "black", blk_player, self._board)
        self._board[9][8] = blk_chariot2

        # Initialize Cannon pieces
        red_cannon1 = Cannon("RED_CAN", [2, 1], "red", red_player, self._board)
        self._board[2][1] = red_cannon1
        red_cannon2 = Cannon("RED_CAN", [2, 7], "red", red_player, self._board)
        self._board[2][7] = red_cannon2
        blk_cannon1 = Cannon("BLK_CAN", [7, 1], "black", blk_player, self._board)
        self._board[7][1] = blk_cannon1
        blk_cannon2 = Cannon("BLK_CAN", [7, 7], "black", blk_player, self._board)
        self._board[7][7] = blk_cannon2

        # Initialize Soldier pieces
        red_soldier1 = Soldier("REDSLDR", [3, 0], "red", red_player, self._board)
        self._board[3][0] = red_soldier1
        red_soldier2 = Soldier("REDSLDR", [3, 2], "red", red_player, self._board)
        self._board[3][2] = red_soldier2
        red_soldier3 = Soldier("REDSLDR", [3, 4], "red", red_player, self._board)
        self._board[3][4] = red_soldier3
        red_soldier4 = Soldier("REDSLDR", [3, 6], "red", red_player, self._board)
        self._board[3][6] = red_soldier4
        red_soldier5 = Soldier("REDSLDR", [3, 8], "red", red_player, self._board)
        self._board[3][8] = red_soldier5
        blk_soldier1 = Soldier("BLKSLDR", [6, 0], "black", blk_player, self._board)
        self._board[6][0] = blk_soldier1
        blk_soldier2 = Soldier("BLKSLDR", [6, 2], "black", blk_player, self._board)
        self._board[6][2] = blk_soldier2
        blk_soldier3 = Soldier("BLKSLDR", [6, 4], "black", blk_player, self._board)
        self._board[6][4] = blk_soldier3
        blk_soldier4 = Soldier("BLKSLDR", [6, 6], "black", blk_player, self._board)
        self._board[6][6] = blk_soldier4
        blk_soldier5 = Soldier("BLKSLDR", [6, 8], "black", blk_player, self._board)
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

    def pos_convert(self, pos):
        """Converts the player inputted pos to integers to represent index locations on board. Returns as a list."""
        row = int(pos[1:]) - 1  # Convert the number in the pos into the row integer
        column = pos[:1].lower()  # Get the letter to be converted into column integer

        convert_dict = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8}
        if column in convert_dict:  # Convert to corresponding integer
            column = convert_dict[column]
        else:  # If string is not a-i, convert to arbitrary number off the board
            column = 77

        return [row, column]

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
        cp = self.pos_convert(curr_pos)  # current position coordinates as a list
        np = self.pos_convert(new_pos)  # intended new position coordinates as a list

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
    DEBUG = False
    if DEBUG == True:
        print(msg1, msg2, msg3, msg4)


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 30
HEIGHT = 30

# This sets the margin between each cell
MARGIN = 5

# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range(10):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(9):
        grid[row].append(0)  # Append a cell

# Set row 1, cell 5 to one. (Remember rows and
# column numbers start at zero.)
grid[1][5] = 1

# Initialize pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [320, 355]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Array Backed Grid")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            # Set that location to one
            grid[row][column] = 1
            print("Click ", pos, "Grid coordinates: ", row, column)

    # Set the screen background
    screen.fill(BLACK)

    # Draw the grid
    for row in range(10):
        for column in range(9):
            color = WHITE
            if grid[row][column] == 1:
                color = GREEN
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
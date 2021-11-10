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

        red_palace = ([0, 3], [0, 4], [0, 5], [1, 3], [
                      1, 4], [1, 5], [2, 3], [2, 4], [2, 5])
        black_palace = ([7, 3], [7, 4], [7, 5], [8, 3], [
                        8, 4], [8, 5], [9, 3], [9, 4], [9, 5])

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
        if new_pos != [cp[0] + 1, cp[1]] and new_pos != [cp[0] - 1, cp[1]] and new_pos != [cp[0], cp[1] + 1] and new_pos != [cp[0], cp[1] - 1]:
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
        red_palace = ([0, 3], [0, 4], [0, 5], [1, 3], [
                      1, 4], [1, 5], [2, 3], [2, 4], [2, 5])
        black_palace = ([7, 3], [7, 4], [7, 5], [8, 3], [
                        8, 4], [8, 5], [9, 3], [9, 4], [9, 5])

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
        coord = [[cp[0] + 1, cp[1] + 1], [cp[0] + 1, cp[1] - 1],
                 [cp[0] - 1, cp[1] + 1], [cp[0] - 1, cp[1] - 1]]

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
                             [cp[0] + 1, cp[1] + 2], [cp[0] - 1,
                                                      cp[1] + 2], [cp[0] + 1, cp[1] - 2],
                             [cp[0] - 1, cp[1] - 2]]

        # List of positions that need to be checked for blocking pieces
        coord = [[cp[0] + 1, cp[1]], [cp[0] - 1, cp[1]],
                 [cp[0], cp[1] + 1], [cp[0], cp[1] - 1]]
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
            # Get the amount of spaces the chariot is moving
            spaces = cp[1] - new_pos[1]
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
            # Get the amount of spaces the chariot is moving
            spaces = cp[0] - new_pos[0]
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
        # When trying to take an enemy piece
        if self._board[new_pos[0]][new_pos[1]] != "_______":
            if cp[0] == new_pos[0]:  # When moving horizontal
                # Get the amount of spaces the chariot is moving
                spaces = cp[1] - new_pos[1]
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
                    # If space being checked is empty
                    if self._board[cp[0]][cp[1] - num] == "_______":
                        return self.legal_move_test(new_pos, num + 1, tracker)
                    else:
                        if tracker < 1:  # If there is a piece in space being checked
                            tracker += 1
                            return self.legal_move_test(new_pos, num + 1, tracker)
                        else:
                            # debug("Cannon cannot jump over 2 pieces.")
                            return False
                elif cp[1] < new_pos[1]:  # Rightward movement
                    # If space being checked is empty
                    if self._board[cp[0]][cp[1] + num] == "_______":
                        return self.legal_move_test(new_pos, num + 1, tracker)
                    else:
                        if tracker < 1:  # If there is a piece in space being checked
                            tracker += 1
                            return self.legal_move_test(new_pos, num + 1, tracker)
                        else:
                            # debug("Cannon cannot jump over 2 pieces.")
                            return False
            elif cp[1] == new_pos[1]:  # When moving vertical
                # Get the amount of spaces the chariot is moving
                spaces = cp[0] - new_pos[0]
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
                    # If space being checked is empty
                    if self._board[cp[0] - num][cp[1]] == "_______":
                        return self.legal_move_test(new_pos, num + 1, tracker)
                    else:
                        if tracker < 1:  # If there is a piece in space being checked
                            tracker += 1
                            return self.legal_move_test(new_pos, num + 1, tracker)
                        else:
                            # debug("Cannon cannot jump over 2 pieces.")
                            return False
                elif cp[0] < new_pos[0]:  # Rightward movement
                    # If space being checked is empty
                    if self._board[cp[0] + num][cp[1]] == "_______":
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
                # Get the amount of spaces the chariot is moving
                spaces = cp[1] - new_pos[1]
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
                # Get the amount of spaces the chariot is moving
                spaces = cp[0] - new_pos[0]
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

def debug(msg1, msg2="", msg3="", msg4=""):
    DEBUG = True
    if DEBUG == True:
        print(msg1, msg2, msg3, msg4)

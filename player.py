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

def debug(msg1, msg2="", msg3="", msg4=""):
    DEBUG = True
    if DEBUG == True:
        print(msg1, msg2, msg3, msg4)
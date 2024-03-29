# Programmer(s): Anish Ramanadham
# Github Username: ARamanadham
# Description: A functional chess game with slightly modified ruleset (see README for more information)

class GameError(Exception):
    """Custom exception class for Chessboard-related errors"""
    pass


class GameManager:
    """
    Helper class made up of class methods designed to:
    Keep track of the turn count
    Keep track of current player
    Sets of piece names for each player
    A list of tuples indicated captured pieces and the turn they were captured on for each player
    Hold a mapping of rows/column labels for 0-based indexing
    The overall state of the game
    """
    # pre-initialized variables
    _current_player = 'WHITE'
    _turn_count = 1
    _white_pieces = {'P', 'R', 'N', 'B', 'Q', 'K', 'F', 'H'}
    _black_pieces = {'p', 'r', 'n', 'b', 'q', 'k', 'f', 'h'}
    _captured_white_pieces = []
    _captured_black_pieces = []
    _column_mapping = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
    _row_mapping = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    _game_state = 'UNFINISHED'

    @classmethod
    def set_current_player(cls):
        """
        :return: Updates the current player based on the turn count, odd turns are white players turns, evens are black
        """
        cls._current_player = 'WHITE' if cls._turn_count % 2 == 1 else 'BLACK'

    @classmethod
    def get_current_player(cls):
        """
        :return: 'WHITE' or 'BLACK' depending on whose turn it is
        """
        return cls._current_player

    @classmethod
    def set_turn_count(cls):
        """
        :return: Increments the turn count by 1
        """
        cls._turn_count += 1

    @classmethod
    def get_turn_count(cls):
        """
        :return: Current turn number
        """
        return cls._turn_count

    @classmethod
    def get_white_pieces(cls):
        """
        :return: set of white piece names
        """
        return cls._white_pieces

    @classmethod
    def get_black_pieces(cls):
        """
        :return: Set of black piece names
        """
        return cls._black_pieces

    @classmethod
    def set_captured_pieces(cls, piece_name, turn_count):
        """
        adds a tuple (piece_name, turn_count) to the appropriate captured pieces dictionary
        :param piece_name: Name of the piece that was captured, uppercase indicates white player piece, lowercase black
        :param turn_count: The turn the piece was captured on
        :return: updates the appropriate captured pieces list
        """
        if piece_name in cls._white_pieces:
            cls._captured_white_pieces.append((piece_name, turn_count))
        else:
            cls._captured_black_pieces.append((piece_name, turn_count))

    @classmethod
    def get_captured_white_pieces(cls):
        """
        :return: a list of tuples containing piece name + turn the piece was captured on
        """
        return cls._captured_white_pieces

    @classmethod
    def get_captured_black_pieces(cls):
        """
        :return: a list of tuples containing piece name + turn the piece was captured on
        """
        return cls._captured_black_pieces

    @classmethod
    def get_column_mapping(cls):
        """
        :return: 0-based index column mapping
        """
        return cls._column_mapping

    @classmethod
    def get_row_mapping(cls):
        """
        :return: 0-based index row mapping
        """
        return cls._row_mapping

    @classmethod
    def set_game_state(cls):
        """
        :return: Updates the state of the game based on captured pieces
        """
        game_state = 'UNFINISHED'
        if any(piece[0] == 'K' for piece in cls._captured_white_pieces):
            game_state = 'BLACK_WON'
        if any(piece[0] == 'k' for piece in cls._captured_black_pieces):
            game_state = 'WHITE_WON'
        cls._game_state = game_state

    @classmethod
    def get_game_state(cls):
        """
        :return: 'UNFINISHED', 'WHITE_WON', 'BLACK_WON'
        """
        return cls._game_state

    @classmethod
    def reset_game(cls):
        """
        :return: resets game everytime a new instance of the game is called
        """
        cls._current_player = 'WHITE'
        cls._turn_count = 1
        cls._captured_white_pieces = []
        cls._captured_black_pieces = []
        cls._game_state = 'UNFINISHED'


class Pieces:
    """
    The pieces class just checks if the move we are trying to make is legal or not.
    More specifically, it only checks if it is possible to get from the source square to destination square based on,
    The name of the piece and the expected movement of the piece. It does not check if the move can be made
    """

    def __init__(self):
        """
        Initializes variables for row/column mapping and player pieces
        """
        self._columns = GameManager.get_column_mapping()
        self._rows = GameManager.get_row_mapping()
        self._white_pieces = GameManager.get_white_pieces()
        self._black_pieces = GameManager.get_black_pieces()

    def get_valid_move(self, source_piece, dest_piece, source_square, dest_square):
        """
        Checks the piece and location information to call the appropriate valid move method
        :param source_piece: piece we are checking move validity for
        :param dest_piece: piece or '_' at the square we are moving to
        :param source_square: location on chessboard we are moving from
        :param dest_square: location on chessboard we are moving to
        :return: True if valid, False otherwise
        """
        # Checking that if there is a piece at the dest_square, that it does not belong to current player
        if (
                (GameManager.get_current_player() == 'WHITE' and dest_piece.isupper()) or
                (GameManager.get_current_player() == 'BLACK' and dest_piece.islower())
        ):
            raise GameError(f"Move cannot be made the {dest_piece} at {dest_square} belongs to you.")

        # using piece name to call individual valid move methods
        if source_piece.upper() == 'P':
            return self.valid_pawn_move(source_square, dest_square, dest_piece)
        if source_piece.upper() == 'R':
            return self.valid_rook_move(source_square, dest_square, dest_piece)
        if source_piece.upper() == 'B':
            return self.valid_bishop_move(source_square, dest_square, dest_piece)
        if source_piece.upper() == 'N':
            return self.valid_knight_move(source_square, dest_square, dest_piece)
        if source_piece.upper() == 'Q':
            return self.valid_queen_move(source_square, dest_square, dest_piece)
        if source_piece.upper() == 'K':
            return self.valid_king_move(source_square, dest_square, dest_piece)
        if source_piece.upper() == 'F':
            return self.valid_falcon_move(source_square, dest_square, dest_piece)
        if source_piece.upper() == 'H':
            return self.valid_hunter_move(source_square, dest_square, dest_piece)

    def valid_pawn_move(self, source, destination, dest_piece):
        """
        Checks pawn movement from the source to the destination
        Special parameters for pawns: Can only capture diagonally, forward movement only to '_' spaces
        :param source: location pawn is currently at
        :param destination: location pawn is attempting to move to
        :param dest_piece: True if possible, False otherwise
        :return:
        """
        # Row and column mapping for source and destination squares
        source_col = self._columns[source[0]]
        source_row = self._rows[source[1]]
        dest_col = self._columns[destination[0]]
        dest_row = self._rows[destination[1]]

        # Determine the direction based on current player, since rows are mapped in reverse White direction is neg
        if GameManager.get_current_player() == 'WHITE':
            direction = -1
        else:
            direction = 1

        # Checking pawn vertical movement
        if dest_col == source_col:
            if dest_row == source_row + direction and dest_piece == '_':
                return True
            elif (
                    (GameManager.get_current_player() == 'WHITE' and source_row == 6) or
                    (GameManager.get_current_player() == 'BLACK' and source_row == 1)
            ):
                # checking that no piece is in the way
                if dest_row == source_row + 2 * direction and dest_piece == '_':
                    return True

        # Checking pawn diagonal movement
        if abs(dest_col - source_col) == 1 and dest_row == source_row + direction:
            if dest_piece != '_':
                if (
                        (GameManager.get_current_player() == 'WHITE' and dest_piece not in self._white_pieces) or
                        (GameManager.get_current_player() == 'BLACK' and dest_piece not in self._black_pieces)
                ):
                    return True
        raise GameError("Not a valid Pawn move")

    def valid_rook_move(self, source, destination, dest_piece):
        """
        Checks that a rook is capable of moving from the source square to the destination square
        Special parameters for rooks: Can only move along column or rank (row)
        :param source: location the rook is currently at
        :param destination: location the rook is attempting to move to
        :param dest_piece: Piece at destination
        :return: True if valid move, False otherwise
        """
        # Row and column mapping for source and destination squares
        source_col = self._columns[source[0]]
        source_row = self._rows[source[1]]
        dest_col = self._columns[destination[0]]
        dest_row = self._rows[destination[1]]

        # Checking if rook is moving along a rank or column
        if source_row == dest_row:
            # check piece at destination does not belong to the current player
            if (
                    (GameManager.get_current_player() == 'WHITE' and dest_piece not in self._white_pieces) or
                    (GameManager.get_current_player() == 'BLACK' and dest_piece not in self._black_pieces)
            ):
                return True
        elif source_col == dest_col:
            if (
                    (GameManager.get_current_player() == 'WHITE' and dest_piece not in self._white_pieces) or
                    (GameManager.get_current_player() == 'BLACK' and dest_piece not in self._black_pieces)
            ):
                return True
        else:
            raise GameError("Not a valid Rook Move")

    def valid_bishop_move(self, source, destination, dest_piece):
        """
        Checks that a bishop is capable of moving from source to destination squares
        Special parameters for bishop: Only can move along diagonals
        :param source: location the bishop is currently at
        :param destination: location the bishop is attempting to move to
        :param dest_piece: Piece at destination
        :return: True if valid move, False otherwise
        """
        # Row and column mapping for source and destination squares
        source_col = self._columns[source[0]]
        source_row = self._rows[source[1]]
        dest_col = self._columns[destination[0]]
        dest_row = self._rows[destination[1]]

        # Check movement is along diagonal path
        if abs(dest_row - source_row) == abs(dest_col - source_col):
            # check piece at destination does not belong to the current player
            if (
                    (GameManager.get_current_player() == 'WHITE' and dest_piece not in self._white_pieces) or
                    (GameManager.get_current_player() == 'BLACK' and dest_piece not in self._black_pieces)
            ):
                return True
        else:
            raise GameError("Not a valid Bishop Move")

    def valid_knight_move(self, source, destination, dest_piece):
        """
        Checks that a knight is capable of moving from source to destination squares
        Special parameters for knight: Only can move in an L shape
        :param source: location the knight is currently at
        :param destination: location the knight is attempting to move to
        :param dest_piece: Piece at destination
        :return: True if valid move, False otherwise
        """
        # Row and column mapping for source and destination squares
        source_col = self._columns[source[0]]
        source_row = self._rows[source[1]]
        dest_col = self._columns[destination[0]]
        dest_row = self._rows[destination[1]]

        row_diff = abs(dest_row - source_row)
        col_diff = abs(dest_col - source_col)

        if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
            if (
                    (GameManager.get_current_player() == 'WHITE' and dest_piece not in self._white_pieces) or
                    (GameManager.get_current_player() == 'BLACK' and dest_piece not in self._black_pieces)
            ):
                return True
        else:
            raise GameError("Not a valid Knight move")

    def valid_queen_move(self, source, destination, dest_piece):
        """
        Checks that a queen is capable of moving from source to destination squares
        Special parameters for queen: Can move like a rook or a bishop (along rank, columns, or diagonals)
        :param source: location the queen is currently at
        :param destination: location the queen is attempting to move to
        :param dest_piece: Piece at destination
        :return: True if valid move, False otherwise
        """
        # Checks if movement is like a rook
        if self.valid_rook_move(source, destination, dest_piece):
            return True
        # Checks if movement is like a bishop
        elif self.valid_bishop_move(source, destination, dest_piece):
            return True
        else:
            raise GameError("Not a valid Queen move")

    def valid_king_move(self, source, destination, dest_piece):
        """
        Checks that a king is capable of moving from source to destination squares
        Special parameters for king: Can move one space in any direction
        :param source: location the king is currently at
        :param destination: location the king is attempting to move to
        :param dest_piece: Piece at destination
        :return: True if valid move, False otherwise
        """
        # Row and column mapping for source and destination squares
        source_col = self._columns[source[0]]
        source_row = self._rows[source[1]]
        dest_col = self._columns[destination[0]]
        dest_row = self._rows[destination[1]]

        row_diff = abs(dest_row - source_row)
        col_diff = abs(dest_col - source_col)

        if row_diff <= 1 and col_diff <= 1:
            if (
                    (GameManager.get_current_player() == 'WHITE' and dest_piece not in self._white_pieces) or
                    (GameManager.get_current_player() == 'BLACK' and dest_piece not in self._black_pieces)
            ):
                return True
        else:
            raise GameError("Not a valid King move")

    def valid_falcon_move(self, source, destination, dest_piece):
        """
        Checks that a falcon is capable of moving from source to destination squares
        Special parameters for falcon: Move forward like a bishop and backwards like a rook
        :param source: location the falcon is currently at
        :param destination: location the falcon is attempting to move to
        :param dest_piece: Piece at destination
        :return: True if valid move, False otherwise
        """
        source_row = self._rows[source[1]]
        dest_row = self._rows[destination[1]]

        # determine the 'forward' direction based on current player
        if GameManager.get_current_player() == 'WHITE':
            direction = -1
        else:
            direction = 1

        # Check if we are moving up or down on the board (dest_row > source_row) means moving down on the board
        if dest_row > source_row:
            if direction == -1:
                return self.valid_rook_move(source, destination, dest_piece)
            else:
                return self.valid_bishop_move(source, destination, dest_piece)
        elif dest_row < source_row:
            if direction == -1:
                return self.valid_bishop_move(source, destination, dest_piece)
            else:
                return self.valid_rook_move(source, destination, dest_piece)
        else:
            raise GameError("Not a valid Falcon move")

    def valid_hunter_move(self, source, destination, dest_piece):
        """
        Checks that a hunter is capable of moving from source to destination squares
        Special parameters for hunter: Move forward like a rook and backwards like a bishop
        :param source: location the hunter is currently at
        :param destination: location the hunter is attempting to move to
        :param dest_piece: Piece at destination
        :return: True if valid move, False otherwise
        """
        source_row = self._rows[source[1]]
        dest_row = self._rows[destination[1]]

        # determine the 'forward' direction based on current player
        if GameManager.get_current_player() == 'WHITE':
            direction = -1
        else:
            direction = 1

        # Check if we are moving up or down on the board (dest_row > source_row) means moving down on the board
        if dest_row > source_row:
            if direction == -1:
                return self.valid_bishop_move(source, destination, dest_piece)
            else:
                return self.valid_rook_move(source, destination, dest_piece)
        elif dest_row < source_row:
            if direction == -1:
                return self.valid_rook_move(source, destination, dest_piece)
            else:
                return self.valid_bishop_move(source, destination, dest_piece)
        else:
            raise GameError("Not a valid Hunter move")


class PathChecker:
    """
    Checks the path between source and destination squares to determine if the move can be made
    """
    @staticmethod
    def get_valid_path(chessboard, source, dest):
        """
        Static Method to determine the type of movement and calls the valid check move method
        :param chessboard: chessboard object
        :param source: location we are moving from
        :param dest: location we are moving to
        :return: True if path is clear, false otherwise
        """
        # Knights can jump over pieces, hence only need to check that the destination is empty or an opponent's piece
        if chessboard.get_piece(source).lower() == 'n':
            if chessboard.get_piece(dest) == '_':
                return True
            elif(
                    (GameManager.get_current_player() == 'WHITE' and chessboard.get_piece(dest).islower()) or
                    (GameManager.get_current_player() == 'BLACK' and chessboard.get_piece(dest).isupper())
            ):
                return True
        else:
            # Get source & Destination coordinates
            source_col = GameManager.get_column_mapping()[source[0]]
            source_row = GameManager.get_row_mapping()[source[1]]
            dest_col = GameManager.get_column_mapping()[dest[0]]
            dest_row = GameManager.get_row_mapping()[dest[1]]

            # Check vertical path
            if source_col == dest_col:
                return PathChecker.check_vertical(chessboard, source, dest)

            # Check horizontal Path
            if source_row == dest_row:
                return PathChecker.check_horizontal(chessboard, source, dest)

            # Check diagonal path
            if abs(dest_col - source_col) == abs(dest_row - source_row):
                return PathChecker.check_diagonal(chessboard, source, dest)

    @staticmethod
    def check_vertical(chessboard, source, dest):
        """
        Checks each row from the source to the destination to check if the path is clear
        :param chessboard: chessboard object
        :param source: square we are moving from
        :param dest: square we are moving to
        :return: True if path is clear, False otherwise
        """
        dest_row = GameManager.get_row_mapping()[dest[1]]
        src_row = GameManager.get_row_mapping()[source[1]]
        src_col = GameManager.get_column_mapping()[source[0]]

        # if we are only moving one row, check destination is empty or that piece belongs to the opponent
        if abs(dest_row - src_row) == 1:
            if chessboard.get_piece(dest) == '_':
                return True
            elif(
                    (GameManager.get_current_player() == 'WHITE' and chessboard.get_piece(dest).islower()) or
                    (GameManager.get_current_player() == 'BLACK' and chessboard.get_piece(dest).isupper())
            ):
                return True
            else:
                return False
        else:
            # Set the movement direction
            direction = 1 if dest_row > src_row else -1

            # Iterate through each row in the column starting at one after the source row checking for obstructions
            for row in range(src_row + direction, dest_row, direction):
                if chessboard.get_board()[row][src_col] != '_':
                    return False
            return True

    @staticmethod
    def check_horizontal(chessboard, source, dest):
        """
        Checks each column from the source to the destination to check if the path is clear
        :param chessboard: chessboard object
        :param source: square we are moving from
        :param dest: square we are moving to
        :return: True if path is clear, False otherwise
        """
        src_row = GameManager.get_row_mapping()[source[1]]
        src_col = GameManager.get_column_mapping()[source[0]]
        dest_col = GameManager.get_column_mapping()[dest[0]]

        # if we are only moving one column, check destination is empty or piece belongs to opponent
        if abs(dest_col - src_col) == 1:
            if chessboard.get_piece(dest) == '_':
                return True
            elif(
                    (GameManager.get_current_player() == 'WHITE' and chessboard.get_piece(dest).islower()) or
                    (GameManager.get_current_player() == 'BLACK' and chessboard.get_piece(dest).isupper())
            ):
                return True
            else:
                return False
        else:
            # Setting movement direction
            direction = 1 if dest_col > src_col else -1

            # Iterate through each column in the row, starting at one after the source col checking for any obstructions
            for col in range(src_col + direction, dest_col, direction):
                if chessboard.get_board()[src_row][col] != '_':
                    return False
            return True

    @staticmethod
    def check_diagonal(chessboard, source, dest):
        """
        Checks the diagonal from the source to the destination to check if the path is clear
        :param chessboard: chessboard object
        :param source: square we are moving from
        :param dest: square we are moving to
        :return: True if path is clear, False otherwise
        """
        src_col = GameManager.get_column_mapping()[source[0]]
        src_row = GameManager.get_row_mapping()[source[1]]
        dest_col = GameManager.get_column_mapping()[dest[0]]
        dest_row = GameManager.get_row_mapping()[dest[1]]

        # if we are only moving one space, check destination is empty or piece belongs to opponent
        if abs(dest_col - src_col) == 1 and abs(dest_row - src_row) == 1:
            if chessboard.get_piece(dest) == '_':
                return True
            elif(
                    (GameManager.get_current_player() == 'WHITE' and chessboard.get_piece(dest).islower()) or
                    (GameManager.get_current_player() == 'BLACK' and chessboard.get_piece(dest).isupper())
            ):
                return True
            else:
                return False
        else:
            # Determine movement direction
            col_direction = 1 if dest_col > src_col else -1
            row_direction = 1 if dest_row > src_row else -1

            # Iterate over each diagonal between the source and destination checking for obstructions
            for diagonal in range(1, abs(dest_col - src_col)):
                current_col = src_col + diagonal * col_direction
                current_row = src_row + diagonal * row_direction
                if chessboard.get_board()[current_row][current_col] != '_':
                    return False
            return True


class Chessboard:
    """
    Initializes the chessboard, and handles checking the logic for valid move calls
    It should get and set pieces on the board
    It should also check if a fairy piece can be entered onto the board
    """

    def __init__(self):
        """
        Initializes instance of the pieces class
        Initialize variables necessary for method implementation
        Initializes and empty list to keep track of fairy pieces
        """
        # Initializes instance of pieces class
        self._pieces = Pieces()

        # Get row and column mappings from game manager
        self._columns = GameManager.get_column_mapping()
        self._rows = GameManager.get_row_mapping()

        # Getting piece and captured piece information
        self._white_pieces = GameManager.get_white_pieces()
        self._black_pieces = GameManager.get_black_pieces()

        # Initialize empty list to keep track of entered fairy pieces and checked required pieces
        self._entered_fairy_pieces = []
        self._checked_pieces = []

        # Initializes the chessboard as an empty 2D list and calls the filling method
        self._board = [['_' for _ in range(8)] for _ in range(8)]
        self.initialize_board()

    def initialize_board(self):
        """
        Sets the initial positions of pieces on the board
        White player pieces are UPPERCASE
        Black Player pieces are lowercase
        :return: starting chessboard
        """
        # Black pieces
        self._board[0] = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        self._board[1] = ['p'] * 8

        # White pieces
        self._board[6] = ['P'] * 8
        self._board[7] = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']

    def set_piece(self, source, destination):
        """
        Attempts to move a piece on the chessboard and if the move is a valid move, updates the board
        :param source: Square we are moving from
        :param destination: Square we are moving to
        :return: updated move on the chessboard if possible, false otherwise
        """
        # Validation test 1 - Checking the squares specified are on the chessboard
        if not self.valid_square(source) or not self.valid_square(destination):
            raise GameError(f"Invalid Move: Either {source} or {destination} does not exist on the chessboard")

        source_piece = self.get_piece(source)
        dest_piece = self.get_piece(destination)
        current_player = GameManager.get_current_player()

        # Validation test 2 - If the source piece is '_' we aren't making a valid move
        if source_piece == '_':
            raise GameError(f"There is no piece at {source}. Try again")

        # Validation test 3 - Checks that the source piece belongs to the current player
        if (
                (current_player == 'WHITE' and source_piece.islower()) or
                (current_player == 'BLACK' and source_piece.isupper())
        ):
            raise GameError("You are trying to move your opponents piece!")

        # Validation test 4 - Checking that the move is a legal move according to chess rules
        self._pieces.get_valid_move(source_piece, dest_piece, source, destination)

        # Validation test 5 - Checking that there is no obstructions in the path
        if not PathChecker.get_valid_path(self, source, destination):
            raise GameError("Move cannot be made, a piece is in the way")

        # splitting the source and destination into columns and rows for move indexing
        source_col = GameManager.get_column_mapping()[source[0]]
        source_row = self._rows[source[1]]
        dest_col = self._columns[destination[0]]
        dest_row = self._rows[destination[1]]

        # Setting the source to '_', updating captured pieces list, and moving piece into the destination
        self._board[source_row][source_col] = '_'
        if dest_piece != '_':
            GameManager.set_captured_pieces(dest_piece, GameManager.get_turn_count())

        self._board[dest_row][dest_col] = source_piece

        return True

    def set_fairy_piece(self, fairy_piece, destination):
        """
        Attempts to enter a fairy piece onto the chessboard
        :param fairy_piece: name of piece being entered
        :param destination: location on chessboard the piece is being placed onto
        :return: Sets fairy piece on the chessboard if possible, False otherwise
        """
        # Current player information
        current_player = GameManager.get_current_player()

        # Setting required captured piece list
        required_pieces = ['Q', 'R', 'N', 'B'] if current_player == 'WHITE' else ['q', 'r', 'n', 'b']


        # Ensure square we are place the fairy piece at is on the chessboard
        if not self.valid_square(destination):
            raise GameError(f"{destination} is not on the chessboard")

        # split row and column for indexing
        col = self._columns[destination[0]]
        row = self._rows[destination[1]]

        # Check that the correct player is trying to enter the correct piece name
        if (
                (current_player == 'WHITE' and fairy_piece.isupper()) or
                (current_player == 'BLACK' and fairy_piece.islower())
        ):
            # Check if the piece has already been entered
            if fairy_piece in self._entered_fairy_pieces:
                raise GameError(f"The fairy piece {fairy_piece} is already on the board")
            else:
                if current_player == 'WHITE':
                    if row in [6, 7] and self.get_piece(destination) == '_':
                        for required_piece in required_pieces:
                            for piece, turn_count in GameManager.get_captured_white_pieces():
                                if piece == required_piece and turn_count < GameManager.get_turn_count():
                                    self._entered_fairy_pieces.append(fairy_piece)
                                    self._board[row][col] = fairy_piece
                                    return True
                    else:
                        raise GameError(f"Fairy pieces can only be entered on a blank square in your home two ranks")
                else:
                    if row in [0, 1] and self.get_piece(destination) == '_':
                        for required_piece in required_pieces:
                            for piece, turn_count in GameManager.get_captured_black_pieces():
                                if piece == required_piece and turn_count < GameManager.get_turn_count():

                                    self._entered_fairy_pieces.append(fairy_piece)
                                    self._board[row][col] = fairy_piece
                                    return True
                    else:
                        raise GameError(f"Fairy pieces can only be entered on a blank square in your home two ranks")
        else:
            raise GameError(f"The fairy piece {fairy_piece} does not belong to you!")

    def get_piece(self, square):
        """
        Checks if a square on the chessboard contains a piece or not
        :param square: The location on the chessboard we are checking
        :return: The name of the piece as the specified location
        """
        col = self._columns[square[0]]
        row = self._rows[square[1]]

        return self._board[row][col]

    def valid_square(self, square):
        """
        Ensure that the squares are on the chessboard
        :param square: location on the board we are checking
        :return: True if square is on the chessboard
        """
        if square[0] not in self._columns or square[1] not in self._rows:
            return False
        return True

    def get_board(self):
        return self._board


class ChessVar:
    """
    Responsible for running the game, allowing user to make moves, enter fairy pieces, and return the state of the game
    """

    def __init__(self):
        """
        reset GameManager everytime the game is called
        Initializes an instance of the chessboard to run the game
        Resets the game everytime a new instance of ChessVar is called
        """
        GameManager.reset_game()
        self._chessboard = Chessboard()
        # Calls start method for the game
        self.start_game()

    def start_game(self):
        """
        :return: Beginning game board
        """
        print("Setting up the chessboard")
        self.print_board()
        print("Board ready: it is the White players turn to move first!\n")
        print("If at any point you wish to exit the game, please type 'quit'\n")
        # Checking that the game is still ongoing
        while GameManager.get_game_state() == "UNFINISHED":
            self.make_move()
        print(f"Game over! {GameManager.get_game_state()}")

    def make_move(self):
        if GameManager.get_turn_count() == 1:
            move = self.get_user_input("Please Enter your move (e.g. 'e2, e4'): ")
        else:
            move = self.get_user_input(f"It's {GameManager.get_current_player()} players turn!" +
                                       " Please Enter your move (e.g. 'e2, e4'): ")
        try:
            source, destination = move.split(",")
            source = source.strip()
            destination = destination.strip().upper()

            # Checking if source is 1 char indicating fairy piece entry
            if len(source) == 1:
                if source in ['F', 'H', 'f', 'h']:
                    self.enter_fairy_piece(source, destination)
                else:
                    raise GameError(f" {source} is not one of the valid fairy pieces (F/H for white, f/h for black)")
            else:
                source = source.upper()
                if self._chessboard.set_piece(source, destination):
                    self.print_board()
                    GameManager.set_turn_count()
                    GameManager.set_current_player()
                    GameManager.set_game_state()
                else:
                    return False
        except GameError as e:
            print(f"Invalid Move: {e}")

    def enter_fairy_piece(self, piece, destination):
        try:
            if self._chessboard.set_fairy_piece(piece, destination):
                self.print_board()
                GameManager.set_turn_count()
                GameManager.set_current_player()
            else:
                raise GameError("Fairy Piece entry requirements have not been met")
        except GameError as e:
            print(f"Invalid Move: {e}")

    def get_user_input(self, prompt):
        """
        :return: user input for move
        """
        while True:
            user_input = input(prompt)
            # allows user to quit at any point
            if user_input.lower() == 'quit':
                print("Exiting the game.")
                exit()
            # Checking user input isn't blank
            elif user_input:
                # splits input into source and destination squares
                squares = user_input.split(",")
                if len(squares) != 2:
                    print("Invalid input: enter 2 arguments")
                    continue
                source = squares[0].strip()
                destination = squares[1].strip()
                if len(source) > 2 or len(destination) != 2:
                    print("Invalid input: Source and destination should be in form e2, e4")
                    continue
                return f"{source}, {destination}"

    def print_board(self):
        """
        Handles printing the board, updates after moved pieces as well
        :return: printed board
        """
        column_labels = '   a b c d e f g h '
        row_labels = ['8', '7', '6', '5', '4', '3', '2', '1']

        # Print top border
        print(' ╔' + '═══' * 7 + '╗')

        # Print column labels
        print(' ║' + column_labels + '  ║')

        print(' ║' + '═══' * 7 + '║')

        # Print the board with squares and piece labels
        for row_index, row in enumerate(self._chessboard.get_board()):
            print(f' ║{row_labels[row_index]}║', end=' ')
            for square in row:
                print(square, end=' ')
            print('  ║')

        # Print bottom border
        print(' ╚' + '═══' * 7 + '╝\n')


if __name__ == "__main__":
    game = ChessVar()

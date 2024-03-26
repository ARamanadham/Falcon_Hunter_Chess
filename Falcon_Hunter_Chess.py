# Author: Anish Ramanadham
# Github username: ARamanadham
# Description: Create a functional chess game, based on the falcon-hunter rule variation,
# check README for more information
class GameManager:
    """
    The GameManager class manages the state of the chess game including:
    holds the name of pieces for each player
    the turn count
    the current player information
    a list of tuples indicating captured pieces and the turn they were captured on
    a mapping of rows/columns with 0 based indexing
    the state of the game ('UNFINISHED', 'WHITE_WON', 'BLACK_WON'

    these methods are all classmethods which allow for the methods to be used by other classes without creating an
    instance of the class, this is because they do not rely on any class specific information
    though some may be initialized in order to maintain accuracy

    Implemented as I ran into a recursion error
    """

    # Pre-initialized variables
    _white_pieces = {'K', 'Q', 'R', 'B', 'N', 'P', 'F', 'H'}
    _black_pieces = {'k', 'q', 'r', 'b', 'n', 'p', 'f', 'H'}
    _turn_counter = 1
    _current_player = 'WHITE'
    _columns = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    _rows = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    _captured_pieces = []
    _game_state = 'UNFINISHED'

    @classmethod
    def get_columns(cls):
        """
        :return: column index mapping to be used by other classes
        """
        return cls._columns

    @classmethod
    def get_rows(cls):
        """
        :return: row index mapping to be used by other classes
        """
        return cls._rows

    @classmethod
    def set_captured_pieces(cls, piece_name, turn_counter):
        """
        adds a tuple (piece, turn number piece was captured on) to the captured pieces list
        :param piece_name: name of the piece that was captured
        :param turn_counter: the turn it was captured on
        :return: updates the list of captured pieces
        """
        cls._captured_pieces.append((piece_name, turn_counter))

    @classmethod
    def get_captured_pieces(cls):
        """
        :return: list of tuples (captured piece name, turn number it was lost on) for use by other classes
        """
        return cls._captured_pieces

    @classmethod
    def set_current_player(cls):
        """
        :return: Based on the turn counter, returns whose turn it is (odd turn count = 'WHITE', even = 'BLACK')
        """
        cls._current_player = 'WHITE' if cls._turn_counter % 2 == 1 else 'BLACK'

    @classmethod
    def get_current_player(cls):
        """
        :return: returns 'WHITE' or 'BLACK' depending on whose turn it is
        """
        return cls._current_player

    @classmethod
    def set_turn_counter(cls):
        """
        :param turn_counter: the turn counter, setting it to the updated value after every move call
        :return: updates turn counter
        """
        cls._turn_counter += 1

    @classmethod
    def get_turn_counter(cls):
        """
        :return: Returns the turn count to be used in other classes
        """
        return cls._turn_counter

    @classmethod
    def set_game_state(cls):
        """
        :return: Updates the state of the game based on the list of captured pieces
        """
        game_state = 'UNFINISHED'
        captured_pieces = cls.get_captured_pieces()
        for piece, _ in captured_pieces:
            if piece == 'k':
                game_state = 'WHITE_WON'
            elif piece == 'K':
                game_state = 'BLACK_WON'
        cls._game_state = game_state

    @classmethod
    def get_game_state(cls):
        """
        :return: 'UNFINISHED', 'WHITE_WON', 'BLACK_WON' based on state of the game
        """
        return cls._game_state

    @classmethod
    def get_white_pieces(cls):
        """
        :return: list of white players pieces
        """
        return cls._white_pieces

    @classmethod
    def get_black_pieces(cls):
        """
        :return: list of black players pieces
        """
        return cls._black_pieces

    @classmethod
    def set_reset_game(cls):
        """
        :return: Resets turn counter to 1
        """
        cls._turn_counter = 1
        cls._current_player = 'WHITE'
        cls._captured_pieces = []
        cls._game_state = 'UNFINISHED'


class Pieces:
    """
    The pieces class is used to check if a move is legal or not by:
    Checking that the source square piece is an actual piece
    Checking that the destination square is either empty or contains a piece from the opposing player
    Validating that the move from the source square to the destination square is legal by piece logic
    """

    def __init__(self):
        """
        Initializes variables for:
        the row and column mapping of Game Manager,
        the current player,
        and the player piece dictionaries
        """
        self._columns = GameManager.get_columns()
        self._rows = GameManager.get_rows()
        self._white_pieces = GameManager.get_white_pieces()
        self._black_pieces = GameManager.get_black_pieces()

    def get_valid_move(self, source_piece, destination_piece, source_square, dest_square):
        """
        Checks the piece_name from chessboard to call the appropriate valid move method
        :param source_piece: Piece that we are checking for move validity
        :param destination_piece: Piece or '_' at the square we are moving to
        :param source_square: location on chessboard we are moving from
        :param dest_square: location on chessboard we are moving to
        :return: True if move is valid, False otherwise
        """
        # getting current player information
        current_player = GameManager.get_current_player()

        # If the current player is trying to move their opponents piece, return false
        if (
                (current_player == 'WHITE' and source_piece.islower()) or
                (current_player == 'BLACK' and source_piece.isupper())
        ):
            return False

        # if the destination piece belongs to the current player, we can't move there, return False
        if (
                (current_player == 'WHITE' and destination_piece.isupper()) or
                (current_player == 'BLACK' and destination_piece.islower())
        ):
            return False

        # Use the piece name to call the individual valid move methods
        if source_piece.upper() == 'P':
            return self.valid_pawn_move(source_square, dest_square, destination_piece)
        elif source_piece.upper() == 'R':
            return self.valid_rook_move(source_square, dest_square)
        elif source_piece.upper() == 'B':
            return self.valid_bishop_move(source_square, dest_square)
        elif source_piece.upper() == 'N':
            return self.valid_knight_move(source_square, dest_square)
        elif source_piece.upper() == 'Q':
            return self.valid_queen_move(source_square, dest_square)
        elif source_piece.upper() == 'K':
            return self.valid_king_move(source_square, dest_square)
        elif source_piece.upper() == 'F':
            return self.valid_falcon_move(current_player, source_square, dest_square)
        elif source_piece.upper() == 'H':
            return self.valid_hunter_move(current_player, source_square, dest_square)
        else:
            # If there is no source piece ('_') return False
            return False

    def valid_pawn_move(self, source, destination, destination_piece):
        """
        Checks that a pawn is capable of moving from the source square to the destination square
        Requirements:
        Current player determines the move direction, Black moves down (positive); White moves up (Negative)
        If the pawn has not moved from the source row (Black 1, White 6) it can move 2 spaces
        If it is attempting a diagonal movement it can only do so in the correct direction
        :param source: location the pawn is currently at
        :param destination: location the pawn is attempting to move to
        :return: True if possible, False otherwise
        """
        # capturing row and column information for source and destination squares
        source_row = self._rows[source[1]]
        source_col = self._columns[source[0]]
        dest_row = self._rows[destination[1]]
        dest_col = self._columns[destination[0]]

        # setting the direction pawn is allowed to move in based on whose turn it is
        if GameManager.get_current_player() == 'WHITE':
            direction = -1
        else:
            direction = 1

        # check if the pawn is moving forward
        if dest_col == source_col:
            if dest_row == source_row + direction:
                return True
            # Checking if pawn is moving two squares from its starting location
            elif (
                    (GameManager.get_current_player() == 'WHITE' and source_row == 6) or
                    (GameManager.get_current_player() == 'BLACK' and source_row == 1)
            ):
                if dest_row == source_row + 2 * direction:
                    return True

        # Checking that diagonal movement is only one row away in appropriate direction
        if abs(dest_col - source_col) == 1 and dest_row == source_row + direction:
            if destination_piece != '_':
                return True
        return False

    def valid_rook_move(self, source, destination):
        """
        Checks that a rook is capable of moving from the source square to the destination square
        rook movement is only along rows or columns, no specific player restrictions
        :param source: location the rook is currently at
        :param destination: location the rook is attempting to move to
        :return: True if possible, False otherwise
        """
        # capturing row and column information for source and destination squares
        source_row = self._rows[source[1]]
        source_col = self._columns[source[0]]
        dest_row = self._rows[destination[1]]
        dest_col = self._columns[destination[0]]

        # Checking if rook is moving along a row
        if source_row == dest_row:
            return True
        # Checking if rook is moving along a column
        elif source_col == dest_col:
            return True
        else:
            return False

    def valid_bishop_move(self, source, destination):
        """
        Checks that a bishop is capable of moving from the source square to the destination square
        bishop movement is only along diagonals, no specific player restrictions
        :param source: location the rook is currently at
        :param destination: location the rook is attempting to move to
        :return: True if possible, False otherwise
        """
        # capturing row and column information for source and destination squares
        source_row = self._rows[source[1]]
        source_col = self._columns[source[0]]
        dest_row = self._rows[destination[1]]
        dest_col = self._columns[destination[0]]

        # Check if movement is along the diagonal path
        if abs(dest_row - source_row) == abs(dest_col - source_col):
            return True
        else:
            return False

    def valid_knight_move(self, source, destination):
        """
        Checks that a knight is capable of moving from the source square to the destination square
        knight move in an L shape: move two spaces (vertically or horizontally) and then one space perpendicular to that
        no specific player restrictions
        :param source: location the rook is currently at
        :param destination: location the rook is attempting to move to
        :return: True if possible, False otherwise
        """
        # capturing row and column information for source and destination squares
        source_row = self._rows[source[1]]
        source_col = self._columns[source[0]]
        dest_row = self._rows[destination[1]]
        dest_col = self._columns[destination[0]]

        # absolute difference in the indices
        row_diff = abs(dest_row - source_row)
        col_diff = abs(dest_col - source_col)

        # check if movement can happen in an L
        if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
            return True
        else:
            return False

    def valid_queen_move(self, source, destination):
        """
        Checks that a Queen is capable of moving from the source square to the destination square
        Queens can move like a rook (along rows and columns) or a bishop (along diagonals)
        no specific player restrictions
        :param source: location the rook is currently at
        :param destination: location the rook is attempting to move to
        :return: True if possible, False otherwise
        """

        # Checks if we move like a rook
        if self.valid_rook_move(source, destination):
            return True
        # If not like a rook then check if it moves like a bishop
        if self.valid_bishop_move(source, destination):
            return True
        else:
            return False

    def valid_king_move(self, source, destination):
        """
        Checks that a King is capable of moving from the source square to the destination square
        King can move one square in any direction
        no specific player restrictions
        :param source: location the rook is currently at
        :param destination: location the rook is attempting to move to
        :return: True if possible, False otherwise
        """
        # capturing row and column information for source and destination squares
        source_row = self._rows[source[1]]
        source_col = self._columns[source[0]]
        dest_row = self._rows[destination[1]]
        dest_col = self._columns[destination[0]]

        row_diff = abs(dest_row - source_row)
        col_diff = abs(dest_col - source_col)
        if row_diff <= 1 and col_diff <= 1:
            return True
        else:
            return False

    def valid_falcon_move(self, current_player, source, destination):
        """
        Checks that a falcon is capable of moving from the source square to the destination square
        Falcon moves forward like a bishop and backwards like a rook cannot move along rank (row)
        Moving forward/backward is different depending on whose turn it is
        :param current_player: 'White' or 'Black'
        :param source: location the rook is currently at
        :param destination: location the rook is attempting to move to
        :return: True if possible, False otherwise
        """
        # capturing row and column information for source and destination squares
        source_row = self._rows[source[1]]
        dest_row = self._rows[destination[1]]

        # Determining the 'forward' direction based on current player
        if current_player == 'WHITE':
            forward_direction = -1
        else:
            forward_direction = 1

        # Check if we are moving up or down on the board (dest_row > source_row) means we are moving down
        if dest_row > source_row:
            # Checking if current player is white or black
            if forward_direction == -1:
                # if we are moving down on the board, and its white's turn we are moving backwards
                return self.valid_rook_move(source, destination)
            else:  # if current player is black
                return self.valid_bishop_move(source, destination)
        # else if we are moving up
        elif dest_row < source_row:
            if forward_direction == -1:
                # if we are moving up we are moving forwards
                return self.valid_bishop_move(source, destination)
            else:
                return self.valid_rook_move(source, destination)
        else:
            return False

    def valid_hunter_move(self, current_player, source, destination):
        """
        Checks that a hunter is capable of moving from the source square to the destination square
        hunter moves forward like a rook and backwards like a bishop, cannot move along rank (row)
        Moving forward/backward is different depending on whose turn it is
        :param current_player: 'White' or 'Black'
        :param source: location the rook is currently at
        :param destination: location the rook is attempting to move to
        :return: True if possible, False otherwise
        """
        # capturing row and column information for source and destination squares
        source_row = self._rows[source[1]]
        dest_row = self._rows[destination[1]]

        # Determining the 'forward' direction based on current player
        if current_player == 'WHITE':
            forward_direction = -1
        else:
            forward_direction = 1

        # checking if we are moving forward or backwards, dest_row > source_row means we are moving down
        if dest_row > source_row:
            if forward_direction == -1:
                # if we are white and moving down on the board we are moving backwards
                return self.valid_bishop_move(source, destination)
            else:
                return self.valid_rook_move(source, destination)
        # dest_row < source_row means we are moving up on the board
        elif dest_row < source_row:
            if forward_direction == -1:
                # if we are white and moving up on the board we are moving forwards
                return self.valid_rook_move(source, destination)
            else:
                return self.valid_bishop_move(source, destination)
        else:
            return False


class Chessboard:
    """
    Initializes the chessboard, and handles the checking logic for every move call
    It should get and set pieces on the board
    It should also help manage if a fairy piece can be entered onto the board
    It interacts with the Pieces class in order to ensure that a move is valid
    """

    def __init__(self):
        """
         initializes an instance of the pieces class
         uses the class methods of the GameManger to get columns and row mappings
         initializes an empty 2D list which will be the board
         calls the initialize_board() method to display the board
         """
        # initialize instance of the pieces class
        self._pieces = Pieces()

        # getting the column mappings from game manager
        self._columns = GameManager.get_columns()

        # getting the row mappings from game manager
        self._rows = GameManager.get_rows()

        # list of player pieces
        self._white_pieces = GameManager.get_white_pieces()
        self._black_pieces = GameManager.get_black_pieces()

        # Initialize empty list to keep track of entered fairy pieces
        self._entered_fairy_pieces = []

        # Setting the empty 2D list for the board and then filling it
        self._board = [['_' for _ in range(8)] for _ in range(8)]
        self.initialize_board()

    def initialize_board(self):
        """
        Sets the initial positions of pieces on the board White pieces are UPPERCASE; Black pieces lowercase
        :return:  initial positions for the print_board method
        """

        # Black Pieces
        self._board[0] = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        self._board[1] = ['p'] * 8

        # White Pieces
        self._board[7] = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        self._board[6] = ['P'] * 8
        # self.print_board()

    def set_piece(self, source, destination):
        """
        Attempts to move a piece on the chessboard and updates the board if true
        :param source: square we are moving from
        :param destination: square we are moving to
        :return: True if the move can be successfully made, False otherwise
        """

        """ 
        Initial Validation Checks:
        1) Check that the source square, and the destination square passed exist on the chessboard
        2) Interact with Pieces class to ensure that the piece at the source square can legally make the desired move
        3) Check if anything is stopping the movement from the source to the destination square
        """

        # Initial Validation Check 1
        if not self.get_valid_square(source) or not self.get_valid_square(destination):
            return False

        # Initialize variables for the source piece and destination piece
        source_piece = self.get_piece(source)
        destination_piece = self.get_piece(destination)

        # Initial Validation Check 2
        if not self._pieces.get_valid_move(source_piece, destination_piece, source, destination):
            return False

        # Initial Validation Check 3
        if not self.path_check(source_piece, destination_piece, source, destination):
            return False

        # If move is legal use the chessboard to check the path (knights can skip over pieces so no need to check path)
        # if not (piece_being_moved.lower() == 'n'):
        #    if not self.clear_path_check(source_row, source_col, dest_row, dest_col, piece_at_dest):
        #        return False

        # Splitting source and destination into column and rows for indexing
        source_col = self._columns[source[0]]
        source_row = self._rows[source[1]]
        dest_col = self._columns[destination[0]]
        dest_row = self._rows[destination[1]]

        # Move is successful so set the source square to '_'
        self._board[source_row][source_col] = '_'

        # Update captured pieces list and update the game state
        if destination_piece != '_':
            GameManager.set_captured_pieces(destination_piece, GameManager.get_turn_counter())

        # move piece into destination square
        self._board[dest_row][dest_col] = source_piece

        # self.print_board()
        return True

    def get_valid_square(self, square):
        """
        Checks if the location specified is within the bounds of the chessboard
        :param square: source/destination location for the piece
        :return: True if on the chessboard
        """
        if square[0] not in self._columns or square[1] not in self._rows:
            return False
        return True

    def set_fairy_piece(self, piece, square):
        """
        Enters the fairy piece onto the chess board
        - checks that the name of the piece being entered is appropriate
        - checks that the square being entered is appropriate
        - Checks if captured pieces holds the required piece needed to enter a fairy piece into the game
        :param piece: determines if fairy piece can be entered onto the board
        :param square: location on chessboard where fairy piece is entering
        :return: True if fairy piece can be set, False otherwise
        """
        piece_to_be_entered = piece

        # Check if the piece name is correct
        if piece not in {'F', 'H', 'f', 'h'}:
            return False

        # Check if piece has already been entered
        if piece in self._entered_fairy_pieces:
            return False

        # Checks that the entry square meets all the requirements
        if not self.get_valid_fairy_square(square):
            return False

        current_player = GameManager.get_current_player()
        captured_pieces = GameManager.get_captured_pieces()

        # Checks if captured pieces holds the correct information
        if current_player == 'White':
            required_pieces = ['Q', 'R', 'N', 'B']
        else:
            required_pieces = ['q', 'r', 'n', 'b']

        # Verifying captured piece and turn requirement
        if (
                (current_player == 'WHITE' and piece_to_be_entered.islower()) or
                (current_player == 'BLACK' and piece_to_be_entered.isupper())
        ):
            return False
        else:
            for required_piece in required_pieces:
                for piece, turn_count in captured_pieces:
                    if piece == required_piece and turn_count < GameManager.get_turn_counter():
                        col = self._columns[square[0]]
                        row = self._rows[square[1]]
                        self._entered_fairy_pieces.append(piece_to_be_entered)
                        self._board[row][col] = piece_to_be_entered
                        # self.print_board()

                        return True

    def get_valid_fairy_square(self, square):
        """
        Determines if a fairy piece can be entered into a square
        :param square: location the fairy piece is being entered into
        :return: True if allowed, False otherwise
        """
        # Ensure square is on the chessboard
        if not self.get_valid_square(square):
            return False

        # Splitting column and row for easier indexing
        col = self._columns[square[0]]
        row = self._rows[square[1]]

        # Verify that the entry square is empty
        if self._board[row][col] != '_':
            return False

        # Verify entry into home ranks
        if GameManager.get_current_player() == 'WHITE':
            return row in [6, 7]
        elif GameManager.get_current_player() == 'BLACK':
            return row in [0, 1]
        else:
            return False

    def path_check(self, source_piece, destination_piece, source, destination):
        """
        Determines the type of movement between source and destination and calls the appropriate check
        :param source_piece: piece we are moving
        :param destination_piece: piece at the destination
        :param source: location on chessboard we are moving from
        :param destination: location on chessboard we are moving to
        :return: True if path is valid, False otherwise
        """
        current_player = GameManager.get_current_player()
        # Check if the source piece is a knight, it can skip over pieces aka move directly to destination
        if source_piece.lower() == 'n':
            # check that the destination piece is either '_' or belongs to the opponent
            if destination_piece == '_':
                return True
            elif (
                    (current_player == 'WHITE' and destination_piece.islower()) or
                    (current_player == 'BLACK' and destination_piece.isupper())
            ):
                return True
            else:
                return False

        # Splitting source and destination into column and rows for indexing
        source_col = self._columns[source[0]]
        source_row = self._rows[source[1]]
        dest_col = self._columns[destination[0]]
        dest_row = self._rows[destination[1]]

        # check if we are making a vertical move
        if source_col == dest_col:
            return self.vertical_path_check(current_player, source_col, source_row, dest_row, source_piece,
                                            destination_piece)
        # Check if we are moving horizontally
        elif source_row == dest_row:
            return self.horizontal_path_check(current_player, source_row, source_col, dest_col, destination_piece)
        # Check if we are moving diagonally
        elif abs(dest_col - source_col) == abs(dest_row - source_row):
            return self.diagonal_path_check(current_player, source_row, source_col, dest_row, dest_col,
                                            destination_piece)

    def vertical_path_check(self, current_player, source_col, source_row, dest_row, source_piece, destination_piece):
        """
        Vertically checks each row of the column between the source and destination to determine if path is clear
        If only moving one row, check that the destination piece belongs to opposite player
        Otherwise set the direction and iterate through each row, making sure that the squares are empty
        Pawns have an additional functionality where they can't capture forward only in diagonals
        :param current_player: 'White' or 'Black'
        :param source_col: column we are moving within
        :param source_row: row in our source column that we are moving from
        :param dest_row: row in our source column that we are moving towards
        :param source_piece: piece at the source square
        :param destination_piece: piece at the destination square
        :return: True if path is clear, False otherwise
        """
        # Check if we are only moving one row
        if abs(dest_row - source_row) == 1:
            # Check destination piece is empty
            if destination_piece == '_':
                return True
            # If it is not empty does it belong to the opponent
            elif (
                    (current_player == 'WHITE' and destination_piece.islower()) or
                    (current_player == 'BLACK' and destination_piece.isupper())
            ):
                # if the piece is a pawn we can't capture forward
                if source_piece.lower() == 'p':
                    return False
                return True

            # It is not empty, and belongs to the current player
            else:
                return False
        else:
            # Determine movement direction
            direction = 1 if dest_row > source_row else -1

            # Initialize row index
            row = source_row + direction

            # Iterate through each row in column (Inclusive)
            while row != dest_row + direction:
                if (
                        (current_player == 'WHITE' and destination_piece.islower()) or
                        (current_player == 'BLACK' and destination_piece.isupper())
                ):
                    if source_piece.lower() == 'p':
                        return False
                if self._board[row][source_col] != '_':
                    return False
                row += direction
            return True

    def horizontal_path_check(self, current_player, source_row, source_col, dest_col, destination_piece):
        """
        Horizontally checks each column of the row between the source and destination to determine if path is clear
        If only moving one column, check that the destination piece belongs to opposite player
        Otherwise set the direction and iterate through each column, making sure squares are empty
        :param current_player: 'White' or 'Black'
        :param source_row: row we are moving within
        :param source_col: column in our source row that we are starting from
        :param dest_col: column in our source row that we are moving towards
        :param destination_piece: piece at the destination square
        :return: True if path is clear, False otherwise
        """
        # Checking if we are only moving one column
        if abs(dest_col - source_col) == 1:
            # Checks if destination piece is empty
            if destination_piece == '_':
                return True
            # If it is not empty does it belong to the opponent
            elif (
                    (current_player == 'WHITE' and destination_piece.islower()) or
                    (current_player == 'BLACK' and destination_piece.isupper())
            ):
                return True
            # It is not empty, and belongs to the current player
            else:
                return False
        else:
            # Determine movement direction
            direction = 1 if dest_col > source_col else -1

            # Iterate through each column in the row checking for any obstructions
            for col in range(source_col + direction, dest_col, direction):
                if self._board[source_row][col] != '_':
                    return False
            return True

    def diagonal_path_check(self, current_player, source_row, source_col, dest_row, dest_col, destination_piece):
        """
        Checks the diagonal pathway from source to destination for any obstructions
        :param current_player: 'WHITE' or 'BLACK'
        :param source_row: row index we are moving from
        :param source_col: col index we are moving from
        :param dest_row: row index we are moving to
        :param dest_col: col index we are moving to
        :param destination_piece: piece at destination square
        :return: True if path is clear, false otherwise
        """
        # Check if we are moving diagonally one square
        if abs(dest_col - source_col) == 1 and abs(dest_row - source_row) == 1:
            # Check if it is empty
            if destination_piece == '_':
                return True
            # If it is not empty does it belong to the opponent
            elif (
                    (current_player == 'WHITE' and destination_piece.islower()) or
                    (current_player == 'BLACK' and destination_piece.isupper())
            ):
                return True
            # It is not empty, and belongs to the current player
            else:
                return False
        else:
            # Determine the movement directions
            col_direction = 1 if dest_col > source_col else -1
            row_direction = 1 if dest_row > source_row else -1

            # iterate over each square in the diagonal path between source and destination
            current_row = source_row + row_direction
            current_col = source_col + col_direction

            while current_row != dest_row and current_col != dest_col:
                if self._board[current_row][current_col] != '_':
                    return False
                current_row += row_direction
                current_col += col_direction
            return True

    def get_piece(self, square):
        """
        Gets the piece that is at the specified square
        :param square: location on the chessboard
        :return: piece in that location
        """
        col = self._columns[square[0]]
        row = self._rows[square[1]]

        return self._board[row][col]

    def get_board(self):
        return self._board


class ChessVar:
    """
    Runs the game, allowing user to make moves, enter fairy pieces, and returns the state of the game
    """

    def __init__(self):
        """
        Initializes an instance of the chessboard class in order to run the game
        Resets the game a new instance of ChessVar is called
        """
        self._chessboard = Chessboard()
        self._reset_game = GameManager.set_reset_game()
        self.start_game()

    def start_game(self):
        print("Setting up the game")
        self.print_board()
        print("Board ready: White its your move!\n")

    def make_move(self, source, destination):
        """
        Attempts to make a move on the chessboard
        :param source: location on the board which we are attempting to move from
        :param destination: location on the board which we are attempting to move to
        :return: True if move can be made, False otherwise
        """
        print(f"Current Player: {GameManager.get_current_player()}")
        print(f"Attempting to move {self._chessboard.get_piece(source)} at {source} to {destination}\n")

        # Checks if the game is over via GameManager
        if GameManager.get_game_state() != 'UNFINISHED':
            return False

        # Attempts to make the move, if self._chessboard.set_piece is false, return false
        if not self._chessboard.set_piece(source, destination):
            return False

        # on move success do the following:

        # Increment the turn counter
        GameManager.set_turn_counter()

        # Update current player
        GameManager.set_current_player()

        # Update the game state
        GameManager.set_game_state()

        self.print_board()

    def enter_fairy_piece(self, piece_name, source):
        """
        Checks if we can enter a fairy piece onto the board and the square it will enter into
        :param piece_name: 'F' 'H' for white fairy/hunter 'f', 'h' for black fairy/hunter
        :param source: square we are entering into
        :return: True if allowed, False otherwise
        """
        print(f"Turn {GameManager.get_turn_counter()}")
        print(f"Current Player: {GameManager.get_current_player()}")
        print(f"Attempting to enter fairy piece: {piece_name} into square {source}\n")

        # Checks if game is over
        if GameManager.get_game_state() != 'UNFINISHED':
            return False

        # Attempts to enter fairy piece onto the chessboard
        if not self._chessboard.set_fairy_piece(piece_name, source):
            return False

        # Increment the turn counter
        GameManager.set_turn_counter()

        # Update current player
        GameManager.set_current_player()

        # Update the game state
        GameManager.set_game_state()

    def get_game_state(self):
        """
        Gets the game state from the Game Manager, currently doesn't work til lnext move is called
        :return: 'UNFINISHED' 'WHITE_WON' 'BLACK_WON'
        """
        return GameManager.get_game_state()

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
        print(' ╚' + '═══' * 7 + '╝')

        if GameManager.get_game_state() != 'UNFINISHED':
            print(f"Game over! {GameManager.get_game_state()}")
            return True

        if GameManager.get_turn_counter() == 1:
            return True
        else:
            print(f"{GameManager.get_current_player()}, you're up!\n")


if __name__ == "__main__":
    game = ChessVar()
    game.make_move('e2', 'e4')  # e2 e4 white true
    game.make_move('d7', 'd5')  # d7 d5 black true
    game.make_move('d1', 'd4')  # d1 d4 white false
    game.make_move('d1', 'g4')  # d1 g4 white true
    game.make_move('d8', 'f6')  # d8 f6 black false
    game.make_move('d8', 'd6')  # d8 d6 black true
    game.make_move('g4', 'c8')
    game.make_move('d6', 'b4')
    game.make_move('c8', 'c7')

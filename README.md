# Falcon_Hunter_Chess
Complete coding projects, including both classwork projects and personal projects

This Chess game is of the Falcon Hunter ruleset variant, and does not implement high level moves such as castling or en passant
Additonally, this game does not take into account Checks or Checkmates, only ending when the opposing King was captured

Rules for Falcon & Hunter pieces:
- Both players Falcon and Hunter pieces start off the chessboard
- A player may enter either thier falcon or their hunter piece on any empty square of their home two ranks (rows) if the following condition has been met:
  - A play must lose either their queen, rook, bishop or knight
  - The entry of the falcon or hunter piece must come on any subsequent turn after the specified pieces have been captured
- The remaining falcon/hunter piece can be entered after a second required piece has been lost at any point (does not need to be after entering the first fairy piece)
- Entering a fairy piece constitutes a turn
- Falcons: Move forward like a bishop, backwards like a rook
- Hunters: Move forward like a rook, backwards like a bishop
- Neither piece can move along rank (row)

The game is designed to be run as an interactive script, meaning it will ask the user to input moves for each turn
The game will print the initial board, print an updated board upon a successful made move or return an error and re-prompt the user for a correct move

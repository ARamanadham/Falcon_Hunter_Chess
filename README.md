This game is designed to be a fully functional modified Chess game, that is easily accessible for Chess first timers.
This game differentiates between player pieces by letter case, the white player pieces are all uppercase & the black player pieces lowercase

Modification:
  - Falcon - Hunter variant ruleset
  - Game ends when king is captured, as such check/checkmate is not taken into account
  - Higher level techniques like casteling and en passant are not incorporated

Falcon - Hunter rules:
  - Falcons (F, f): Move forwards like a Bishop and move backwards like a Rook
  - Hunters (H, h): Move forwards like a Rook and backwards like a Bishop
  - Neither piece can move along rank (row)
  - Both pieces start off of the chessboard
  - Can be placed on any empty space of the players home two ranks on any subsequent turn after that player has lost a Queen, Bishop, Knight or Rook
  - Entering a fairy piece constitutes as a turn

This script is interactive for the user, with players entering moves in the format of [source] , [destination] for example: e2, e4
  - Note: Fairy pieces can be entered by notation [piece name], [entry location] for example: F, e2 (White) or h, d7 (Black) 
After a successful move is made an updated chessboard will be printed to the terminal showing the valid move
Invalid moves will return an error message and prompt the player to try again 
The game will automatically end when a King has been captured

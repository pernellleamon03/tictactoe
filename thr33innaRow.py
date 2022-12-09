import socket
import threading

class thr33innaRow:

  def __init__(self):
    self.turn = "X"
    self.you = "X"
    self.opponent = "O"
    self.board = [[" ", " ", " "], [" ", " ", " "], [" " , " ", " "]]
    self.winner = None
    self.game_over = False
    self.counter = 0

  def host_game(self, host, port):
    socketserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketserver.bind((host,port))
    socketserver.listen(1)

    client = socketserver.accept()
    addr = socketserver.accept()

    self.you = "X"
    self.opponent = "0"

    threading.Thread(target = self.connection, args = (client,)).start()
    socketserver.close()
  def connect_to_game(self, host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host,port))
    
    self.you = "0"
    self.opponent = "X"
    threading.Thread(target= self.connection, args=(client,)).start()
  def connection(self, client):
    while not self.game_over:
      if self.turn == self.you:
        move = input("Enter a coordinate to place character in (row, column) format: ")
        if self.check_valid_move(move.split(',')):
          self.apply_move(move.split(','), self.you)
          self.turn = self.opponent
          client.send(move.encode('utf-8'))
        else:
          print ("Invalid Move, try again.")
      else:
        data = client.recv(1024)
        if not data:
          client.close()
          break
        else:
          self.apply_move(data.decode('utf-8').split(','), self.opponent)
          self.turn = self.you
    client.close()

  def apply_move(self, move, player):
    if self.gameover:
      return
    self.counter += 1
    self.boaord[int(move[0])][int(move[1])] = player
    self.print_board()
    self.check_for_winner()
    if self.winner == self.you:
        print ("You win!")
    elif self.winner == self.opponent:
        print("You lose...")
    else:
      if self.counter ==  9:
        print("Tie.")
        exit()

  def check_valid_move(self, move):
    return self.board[int(move[0])][int(move[1])] == " "

  def check_if_won(self):
    for row in range(3):
      if self.board[row][0]== self.board[row][1] == self.board[row][2] != " ":
        self.winner = self.board[row][0]
        self.game_over = True
        return True
    for column in range(3):
      if self.board[0][column]== self.board[1][column] == self.board[2][column] != " ":
        self.winner = self.board[0][column]
        self.game_over = True
        return True
    if self.board[0][0] == self.board [1][1] == self.board[2][2] != " ":
      self.winner = self.board[0][0]
      self.game_over = True
      return True
    if self.board[0][2] == self.board [1][1] == self.board[2][0] != " ":
      self.winner = self.board[0][0]
      self.game_over = True
      return True
    return False

  def print_board(self):
    for row in range(3):
      print (" | ".join(self.board[row]))
      if row!= 2:
        print("------------")

game = thr33innaRow()
game.host_game("localhost", 9999)
    

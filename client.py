#!/usr/bin/python3

import socket

class tictactoe_game:
  def __init__(self, gridsize):
    self.turn = 0
    self.grid_size = gridsize
    self.grid = create_grid(self.grid_size)
    self.current_player = 0
    self.won = False
    self.winner = 1

  def take_turn(self, x, y):
    if self.grid[x][y] == 0:
      self.grid[x][y] = self.current_player + 1
      self.turn = self.turn + 1
      self.check_won(self.current_player + 1)
      self.current_player = (self.current_player + 1) % 2
      self.print_grid()
      return True
    return False


  def check_won(self, player):
    # Horizontal and vertical rows
    for x in range(self.grid_size):
      win1 = True
      win2 = True
      for y in range(self.grid_size):
        win1 = win1 and self.grid[x][y] == player + 1
        win2 = win2 and self.grid[x][y] == player + 1
      if win1 or win2:
        self.winner = player
        self.won = True
    if(self.won):
        return True

    # diagonals
    win1 = True
    win2 = True
    for k in range(self.grid_size):
      win1 = win1 and self.grid[k][k] == player + 1
      win2 = win2 and self.grid[k][self.grid_size - k - 1] == player + 1
      if win1 or win2:
        self.winner = player
        self.won = True
        return True

    return False

  def print_grid(self):
    print("Turn ", self.turn)
    for x in range(self.grid_size):
      row = "|"
      for y in range(self.grid_size):
        row = row + str(self.grid[x][y]) + "|"
      print(row)
      print("-------")
    if(self.won):
      print("Player " + str(self.winner) + " won!")
    print("")

def create_grid(n):
  grid = [[0 for x in range(n)] for y in range(n)]
  return grid



def connect(host, port):
  client_socket = socket.socket()
  client_socket.connect((host, port))
  return client_socket



def tictactoe_client(host, port):
  client_socket = connect(host, port)

  def send(message):
    msg = message + "\n"
    client_socket.send(msg.encode())

  def receive():
    return client_socket.recv(1024).decode()

  send("GAME-JOIN")
  response = receive()

  player_id = ""
  if response:
    response = response.split()
    if response[0] == "GAME-JOIN-ACK":
      player_id = response[1]
  print("Player id: ", player_id)
  print("Waiting for game...")

  response = receive()
  game = None
  opponent = ""
  if response:
    response = response.split()
    if response[0] == "GAME-READY":
      grid_size = int(response[1])
      opponent = response[2]
      game = tictactoe_game(grid_size)
      send("GAME-READY-ACK")

  print("Game ready! Opponent: " + opponent)

  # client_socket.send(message.encode())  # send message
  # data = client_socket.recv(1024).decode()  # receive response
  # client_socket.close()  # close the connection



if __name__ == '__main__':
  import sys

  if len(sys.argv) != 3:
    print("Usage: {} <server-host> <server-port>".format(sys.argv[0]))
    sys.exit(1)

  host, port = sys.argv[1], int(sys.argv[2])

  tictactoe_client(host, port)

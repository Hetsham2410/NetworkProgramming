import socket
import threading

class TicTacToeServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.players = []
        self.current_player = 0
        self.board = [["", "", ""],
                      ["", "", ""],
                      ["", "", ""]]
        self.lock = threading.Lock()

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        print("Waiting for players to join...")

        while len(self.players) < 2:
            client_socket, client_address = self.server_socket.accept()
            player_name = client_socket.recv(1024).decode()
            self.players.append((player_name, client_socket))
            print(f"Player {player_name} connected.")

        self.send_board_to_all()

        thread1 = threading.Thread(target=self.handle_moves, args=(0,))
        thread2 = threading.Thread(target=self.handle_moves, args=(1,))

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        self.server_socket.close()

    def handle_moves(self, player_index):
        player_name, client_socket = self.players[player_index]

        while True:
            try:
                row = int(client_socket.recv(1024).decode())
                col = int(client_socket.recv(1024).decode())

                if self.is_valid_move(row, col, player_index):
                    self.update_board(row, col, player_index)

                    if self.check_winner(player_index):
                        self.send_winner(player_name)
                        self.reset_board()
                    elif self.is_board_full():
                        self.send_draw()
                        self.reset_board()
                    else:
                        self.send_board_to_all()
                        self.switch_player()

            except ValueError:
                pass

            except ConnectionResetError:
                self.players.pop(player_index)
                print(f"Player {player_name} disconnected.")
                break

    def is_valid_move(self, row, col, player_index):
        with self.lock:
            if 0 <= row < 3 \
                    and 0 <= col < 3 \
                    and self.board[row][col] == "" \
                    and player_index == self.current_player:
                return True
            else:
                return False

    def update_board(self, row, col, player_index):
        player_name, _ = self.players[player_index]
        self.board[row][col] = player_name

    def check_winner(self, player_index):
        player_name, _ = self.players[player_index]
        for i in range(3):
            #check rows
            if self.board[i][0] == self.board[i][1] == self.board[i][2] == player_name:
                return True
            #check columns
            if self.board[0][i] == self.board[1][i] == self.board[2][i] == player_name:
                return True
        #check daiagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == player_name:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == player_name:
            return True
        return False

    def is_board_full(self):
        for row in self.board:
            if "" in row:
                return False
        return True

    def reset_board(self):
        self.board = [["", "", ""],
                      ["", "", ""],
                      ["", "", ""]]

    def switch_player(self):
        self.current_player = 1 - self.current_player

    def send_board_to_all(self):
        board_str = "\n".join(["|".join(row) for row in self.board])
        for _, client_socket in self.players:
            client_socket.send(board_str.encode())

    def send_winner(self, winner_name):
        message = f"Winner: {winner_name}"
        for _, client_socket in self.players:
            client_socket.send(message.encode())

    def send_draw(self):
        message = "It's a draw!"
        for _, client_socket in self.players:
            client_socket.send(message.encode())


if __name__ == "__main__":
    server = TicTacToeServer("127.0.0.1", 7002)
    server.start()

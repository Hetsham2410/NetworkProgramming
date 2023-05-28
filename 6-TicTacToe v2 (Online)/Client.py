import socket
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from threading import Thread

class TicTacToeClient:
    def __init__(self, player_name, host, port):
        self.player_name = player_name
        self.board = [["", "", ""],
                      ["", "", ""],
                      ["", "", ""]]

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.client_socket.send(self.player_name.encode())

        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe")
        self.root.configure(bg="#0F4444")

        self.style = ttk.Style()
        self.style.configure("Game.TButton", font=("algerian", 24, "bold"), foreground="red", background="white",
                             width=10, height=5)
        self.style.configure("ResultLabel.TLabel", font=("algerian", 16, "bold"), foreground="#A74F4F")

        self.welcome_label = ttk.Label(self.root, text="Welcome to X|O play", style="ResultLabel.TLabel")
        self.welcome_label.grid(row=3, column=0, columnspan=3, pady=10)

        self.buttons = []
        for row in range(3):
            button_row = []
            for col in range(3):
                button = ttk.Button(self.root, text="", style="Game.TButton",
                                    command=lambda r=row, c=col: self.make_move(r, c))
                button.grid(row=row, column=col, padx=5, pady=5)
                button_row.append(button)
            self.buttons.append(button_row)

        self.listen_for_moves()

    def make_move(self, row, col):
        if self.board[row][col] == "":
            self.client_socket.send(str(row).encode())
            self.client_socket.send(str(col).encode())

    def listen_for_moves(self):
        receive_thread = Thread(target=self.receive_messages)
        receive_thread.start()

    def receive_messages(self):
        while True:
            response = self.client_socket.recv(1024).decode()

            if response.startswith("Winner"):
                winner_name = response.split(":")[1].strip()
                messagebox.showinfo("Game Over", f"Player {winner_name} wins!")
                self.reset_board()
            elif response == "It's a draw!":
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_board()
            else:
                self.update_board(response)

    def update_board(self, board_str):
        self.board = [row.split("|") for row in board_str.split("\n")]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]["text"] = self.board[i][j]

    def reset_board(self):
        self.board = [["", "", ""],
                      ["", "", ""],
                      ["", "", ""]]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]["text"] = ""

if __name__ == "__main__":
    player_name = input("Enter your name: ")
    client = TicTacToeClient(player_name, "127.0.0.1", 7002)
    client.root.mainloop()

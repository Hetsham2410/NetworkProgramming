
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading


class TicTacToeGUI:
    def __init__(self):
        self.current_player = "X"
        self.board = [["", "", ""],
                      ["", "", ""],
                      ["", "", ""]]

        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe")
        self.root.configure(bg="#0F4444")

        self.style = ttk.Style()
        self.style.configure("Game.TButton",
                             font=("algerian", 24, "bold"),
                             foreground="red",
                             background="white",
                             width=10,
                             height=5)
        self.style.configure("ResultLabel.TLabel",
                             font=("algerian", 16, "bold"),
                             foreground="#A74F4F")

        self.buttons = []
        for row in range(3):
            button_row = []
            for col in range(3):
                button = ttk.Button(self.root, text="", style="Game.TButton",
                                    command=lambda r=row, c=col: self.play(r, c))
                button.grid(row=row, column=col, padx=5, pady=5)
                button_row.append(button)
            self.buttons.append(button_row)

        self.next_player_label = ttk.Label(self.root,
                                           text="Next Player: X",
                                           style="ResultLabel.TLabel")
        self.next_player_label.grid(row=3, column=0, columnspan=3, pady=10)

    def play(self, row, col):
        if self.board[row][col] == "":
            self.board[row][col] = self.current_player
            self.buttons[row][col]["text"] = self.current_player

            if self.check_winner():
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.reset_board()
            elif self.check_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_board()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.next_player_label["text"] = f"Next Player: {self.current_player}"

    def check_winner(self):
        # Check rows
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != "":
                return True

        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != "":
                return True

        # Check diagonals
        if (self.board[0][0] == self.board[1][1] == self.board[2][2] != "") or \
                (self.board[0][2] == self.board[1][1] == self.board[2][0] != ""):
            return True

        return False

    def check_draw(self):
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == "":
                    return False
        return True

    def reset_board(self):
        self.current_player = "X"
        self.board = [["", "", ""],
                      ["", "", ""],
                      ["", "", ""]]
        for row in range(3):
            for col in range(3):
                self.buttons[row][col]["text"] = ""
        self.next_player_label["text"] = "Next Player: X"


def play_game():
    gui = TicTacToeGUI()
    gui.root.mainloop()

thread = threading.Thread(target=play_game)
thread.start()

import tkinter as tk
from tkinter import messagebox
import math

# Global board and buttons
board = [' ' for _ in range(9)]
buttons = []

# Win check
def check_winner(player):
    win_cond = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # cols
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    return any(all(board[i] == player for i in combo) for combo in win_cond)

# Draw check
def is_draw():
    return ' ' not in board

# Minimax
def minimax(depth, is_maximizing):
    if check_winner('O'): return 1
    if check_winner('X'): return -1
    if is_draw(): return 0

    if is_maximizing:
        best = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                best = max(best, minimax(depth+1, False))
                board[i] = ' '
        return best
    else:
        best = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                best = min(best, minimax(depth+1, True))
                board[i] = ' '
        return best

# AI move
def ai_move():
    best_score = -math.inf
    move = -1
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(0, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                move = i
    if move != -1:
        board[move] = 'O'
        buttons[move].config(text='O', state='disabled')

# Player click
def handle_click(i):
    if board[i] == ' ':
        board[i] = 'X'
        buttons[i].config(text='X', state='disabled')
        if check_winner('X'):
            messagebox.showinfo("Result", "You win!")
            disable_buttons()
            return
        if is_draw():
            messagebox.showinfo("Result", "It's a draw!")
            return
        ai_move()
        if check_winner('O'):
            messagebox.showinfo("Result", "AI wins!")
            disable_buttons()
        elif is_draw():
            messagebox.showinfo("Result", "It's a draw!")

# Disable all
def disable_buttons():
    for btn in buttons:
        btn.config(state='disabled')

# Reset
def reset_game():
    global board
    board = [' ' for _ in range(9)]
    for btn in buttons:
        btn.config(text=' ', state='normal')

# UI
root = tk.Tk()
root.title("Tic Tac Toe (Minimax AI)")

frame = tk.Frame(root)
frame.pack()

for i in range(9):
    b = tk.Button(frame, text=' ', font=('Arial', 20), width=5, height=2,
                  command=lambda i=i: handle_click(i))
    b.grid(row=i//3, column=i%3)
    buttons.append(b)

reset_button = tk.Button(root, text="Reset", font=('Arial', 14), command=reset_game)
reset_button.pack(pady=10)

root.mainloop()

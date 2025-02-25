import tkinter as tk
import random

class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Game")
        
        self.setup_game()
    
    def setup_game(self):
        self.setup_frame = tk.Frame(self.root)
        self.setup_frame.pack()
        
        tk.Label(self.setup_frame, text="Enter sequence length (15-25):", font=("Arial", 12)).pack()
        
        self.entry = tk.Entry(self.setup_frame)
        self.entry.pack()
        
        tk.Button(self.setup_frame, text="Start Game", command=self.start_game).pack()
    
    def start_game(self):
        try:
            length = int(self.entry.get())
            if 15 <= length <= 25:
                self.setup_frame.destroy()
                self.sequence = [random.randint(1, 9) for _ in range(length)]
                self.player1_score = 0
                self.player2_score = 0
                self.turn = 1
                
                self.label = tk.Label(self.root, text=self.get_game_state(), font=("Arial", 14))
                self.label.pack()
                
                self.frame = tk.Frame(self.root)
                self.frame.pack()
                
                self.buttons = []
                self.create_buttons()
            else:
                self.entry.delete(0, tk.END)
                self.entry.insert(0, "Enter a valid number!")
        except ValueError:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Enter a valid number!")
    
    def get_game_state(self):
        return f"Sequence: {self.sequence}\nP1: {self.player1_score}, P2: {self.player2_score}, Turn: {'P1' if self.turn == 1 else 'P2'}"

    def create_buttons(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        self.buttons = []
        if self.turn == 1:
            for i in range(len(self.sequence) - 1):
                btn = tk.Button(self.frame, text=f"{self.sequence[i]} {self.sequence[i+1]}", 
                                command=lambda i=i: self.make_move(i))
                btn.pack(side=tk.LEFT)
                self.buttons.append(btn)
        else:
            self.root.after(500, self.ai_move)

    def make_move(self, i):
        sum_val = self.sequence[i] + self.sequence[i + 1]
        
        if sum_val > 7:
            self.sequence[i] = 1
            if self.turn == 1:
                self.player1_score += 1
            else:
                self.player2_score += 1
        elif sum_val < 7:
            self.sequence[i] = 3
            if self.turn == 1:
                self.player2_score -= 1
            else:
                self.player1_score -= 1
        else:
            self.sequence[i] = 2
            self.player1_score += 1
            self.player2_score += 1
        
        del self.sequence[i + 1]
        self.turn *= -1
        
        self.label.config(text=self.get_game_state())
        self.create_buttons()
        
        if len(self.sequence) == 1:
            self.end_game()
    
    def ai_move(self):
        if len(self.sequence) > 1:
            i = random.randint(0, len(self.sequence) - 2)
            self.make_move(i)
    
    def end_game(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        winner = "Draw" if self.player1_score == self.player2_score else ("P1 Wins" if self.player1_score > self.player2_score else "P2 Wins")
        self.label.config(text=f"Game Over!\n{winner}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GameApp(root)
    root.mainloop()

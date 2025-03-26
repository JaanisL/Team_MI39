import tkinter as tk
import random
from node import Node
from tree import Tree

class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Game")
        self.tree_window = None
        self.ai_method = "alpha-beta"
        self.setup_game()
        
    def setup_game(self):
        self.setup_frame = tk.Frame(self.root)
        self.setup_frame.pack()
        
        tk.Label(self.setup_frame, text="Enter sequence length (15-25):", font=("Arial", 12)).pack()
        self.entry = tk.Entry(self.setup_frame)
        self.entry.pack()
        
        tk.Label(self.setup_frame, text="Choose AI method:", font=("Arial", 12)).pack()
        self.method_var = tk.StringVar(value="alpha-beta")
        tk.Radiobutton(self.setup_frame, text="Minimax", variable=self.method_var, value="minimax").pack()
        tk.Radiobutton(self.setup_frame, text="Alpha-Beta", variable=self.method_var, value="alpha-beta").pack()

        tk.Label(self.setup_frame, text="Who should start?", font=("Arial", 12)).pack()
        self.start_var = tk.StringVar(value="Player")
        tk.Radiobutton(self.setup_frame, text="Player", variable=self.start_var, value="Player").pack()
        tk.Radiobutton(self.setup_frame, text="AI", variable=self.start_var, value="AI").pack()
        
        tk.Button(self.setup_frame, text="Start Game", command=self.start_game).pack()

    
    def start_game(self):
        try:
            length = int(self.entry.get())
            if 15 <= length <= 25:
                self.ai_method = self.method_var.get()
                self.start_turn = self.start_var.get()
                self.setup_frame.destroy()
                self.initialize_game_state(length)
                self.create_game_ui()
            else:
                self.show_error("Enter a valid number!")
        except ValueError:
            self.show_error("Enter a valid number!")

    
    def initialize_game_state(self, length):
        self.node = Node([random.randint(1, 9) for _ in range(length)])
        
        if self.start_turn == "AI":
            self.node.turn = -1

    
    def create_game_ui(self):
        self.label = tk.Label(self.root, text=self.get_game_state(), font=("Arial", 14))
        self.label.pack()

        self.frame = tk.Frame(self.root)
        self.frame.pack()
        
        self.create_buttons()

        if self.node.turn == -1:
            self.root.after(500, self.ai_move)

    
    def get_game_state(self):
        return f"Sequence: {self.node.sequence}\nPlayer: {self.node.player_score}, AI: {self.node.ai_score}, Turn: {'Player' if self.node.turn == 1 else 'AI'}"
    
    def create_buttons(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        if self.node.turn == 1:
            for i in range(len(self.node.sequence) - 1):
                btn = tk.Button(self.frame, text=f"{self.node.sequence[i]} {self.node.sequence[i+1]}", 
                                command=lambda i=i: self.make_move(i))
                btn.pack(side=tk.LEFT)
    
    def make_move(self, i):
        self.node.make_move(i)
        self.label.config(text=self.get_game_state())
        
        if len(self.node.sequence) == 1:
            self.end_game()
        else:
            self.create_buttons()
            self.visualize_game_tree()

            if self.node.turn == -1:
                self.root.after(500, self.ai_move)
    
    def ai_move(self):
        if len(self.node.sequence) > 1:
            best_move = self.node.find_best_move(method=self.ai_method)
            if best_move is not None:
                self.make_move(best_move)

    
    def end_game(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        winner = "Draw" if self.node.player_score == self.node.ai_score else ("Player Wins" if self.node.player_score > self.node.ai_score else "AI Wins")
        self.label.config(text=f"Game Over!\n{winner}")
        
        self.restart_button = tk.Button(self.root, text="Restart Game", command=self.restart_game)
        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit).pack()
        self.restart_button.pack()

    def restart_game(self):
        if self.tree_window is not None:
            self.tree_window.destroy()
            self.tree_window = None

        self.node.player_score = 0
        self.node.ai_score = 0
        
        self.root.destroy()
        root = tk.Tk()
        GameApp(root)
        root.mainloop()

    def visualize_game_tree(self):
        print("\n--- Game Tree ---")
        tree = Tree(self.node.sequence, self.node.player_score, self.node.ai_score, self.node.turn)
        tree.generate_tree(self.node)
        tree.print_tree()
        
    def show_error(self, message):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, message)

if __name__ == "__main__":
    root = tk.Tk()
    app = GameApp(root)
    root.mainloop()

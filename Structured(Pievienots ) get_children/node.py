import time

class Node:
    id_counter = 0

    def __init__(self, sequence, player_score=0, ai_score=0, turn=1, depth=0):
        self.sequence = sequence
        self.player_score = player_score
        self.ai_score = ai_score
        self.turn = turn
        self.depth = depth
        self.id = Node.id_counter
        Node.id_counter += 1
        self.children = []
        self.value = None
        self.evaluated = False
        
    def get_children(self):
        children = []
        for i in range(len(self.sequence) - 1):
            new_node = Node(self.sequence[:], self.player_score, self.ai_score, self.turn, self.depth + 1)
            new_node.make_move(i)
            children.append(new_node)
        return children


    def make_move(self, i):
        sum_val = self.sequence[i] + self.sequence[i + 1]

        if sum_val > 7:
            self.sequence[i] = 1
            if self.turn == 1:
                self.player_score += 1
            else:
                self.ai_score += 1
        elif sum_val < 7:
            self.sequence[i] = 3
            if self.turn == 1:
                self.ai_score -= 1
            else:
                self.player_score -= 1
        else:
            self.sequence[i] = 2
            self.player_score += 1
            self.ai_score += 1

        del self.sequence[i + 1]
        self.turn *= -1

    def evaluate_state(self):
        score_difference = self.ai_score - self.player_score
        sequence_score = sum(1 if num in [1, 2] else -1 for num in self.sequence)
        return score_difference + sequence_score

    def minimax(self, depth, maximizing_player, nodes_evaluated=0):
        nodes_evaluated += 1
        if depth == 0 or len(self.sequence) == 1:
            return self.evaluate_state(), nodes_evaluated
        
        if maximizing_player:
            max_eval = float('-inf')
            for i in range(len(self.sequence) - 1):
                new_node = Node(self.sequence[:], self.player_score, self.ai_score, self.turn, self.depth + 1)
                new_node.make_move(i)
                eval, nodes = new_node.minimax(depth - 1, False, nodes_evaluated)
                nodes_evaluated = nodes
                max_eval = max(max_eval, eval)
            return max_eval, nodes_evaluated
        else:
            min_eval = float('inf')
            for i in range(len(self.sequence) - 1):
                new_node = Node(self.sequence[:], self.player_score, self.ai_score, self.turn, self.depth + 1)
                new_node.make_move(i)
                eval, nodes = new_node.minimax(depth - 1, True, nodes_evaluated)
                nodes_evaluated = nodes
                min_eval = min(min_eval, eval)
            return min_eval, nodes_evaluated

    def alpha_beta(self, depth, alpha, beta, maximizing_player, nodes_evaluated=0):
        nodes_evaluated += 1
        if depth == 0 or len(self.sequence) == 1:
            return self.evaluate_state(), nodes_evaluated
        
        if maximizing_player:
            max_eval = float('-inf')
            for i in range(len(self.sequence) - 1):
                new_node = Node(self.sequence[:], self.player_score, self.ai_score, self.turn, self.depth + 1)
                new_node.make_move(i)
                eval, nodes = new_node.alpha_beta(depth - 1, alpha, beta, False, nodes_evaluated)
                nodes_evaluated = nodes
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, nodes_evaluated
        else:
            min_eval = float('inf')
            for i in range(len(self.sequence) - 1):
                new_node = Node(self.sequence[:], self.player_score, self.ai_score, self.turn, self.depth + 1)
                new_node.make_move(i)
                eval, nodes = new_node.alpha_beta(depth - 1, alpha, beta, True, nodes_evaluated)
                nodes_evaluated = nodes
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, nodes_evaluated
        
    def find_best_move(self, method="alpha-beta"):
        start_time = time.perf_counter()
        
        best_move = None
        best_value = float('-inf') if self.turn == -1 else float('inf')
        total_nodes_evaluated = 0

        for i in range(len(self.sequence) - 1):
            new_node = Node(self.sequence[:], self.player_score, self.ai_score, self.turn, self.depth + 1)
            new_node.make_move(i)

            if method == "minimax":
                move_value, nodes = new_node.minimax(3, self.turn == -1)
            elif method == "alpha-beta":
                move_value, nodes = new_node.alpha_beta(3, float('-inf'), float('inf'), self.turn == -1)
            
            total_nodes_evaluated += nodes

            if self.turn == -1:
                if move_value > best_value:
                    best_value = move_value
                    best_move = i
            else: 
                if move_value < best_value:
                    best_value = move_value
                    best_move = i
        
        elapsed_time = time.perf_counter() - start_time
        print(f"MI pārbaudīja {total_nodes_evaluated} virsotnes {elapsed_time:.6f} sekundēs.")
        return best_move

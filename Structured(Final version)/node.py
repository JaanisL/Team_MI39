class Node:
    def __init__(self, sequence, player_score=0, ai_score=0, turn=1):
        self.sequence = sequence
        self.player_score = player_score
        self.ai_score = ai_score
        self.turn = turn

    def make_move(self, i):
        sum_val = self.sequence[i] + self.sequence[i + 1]
        self.sequence[i] = 1 if sum_val > 7 else 3 if sum_val < 7 else 2

        if sum_val >= 7:
            if self.turn == 1:
                self.player_score += 1
            else:
                self.ai_score += 1
        else:
            if self.turn == 1:
                self.player_score -= 1
            else:
                self.ai_score -= 1

        del self.sequence[i + 1]
        self.turn *= -1

    def evaluate_state(self):
        return sum(1 if num in [1, 2] else -1 for num in self.sequence)
    
    def minimax(self, depth, maximizing_player):
        if depth == 0 or len(self.sequence) == 1:
            return self.evaluate_state()
        
        if maximizing_player:
            max_eval = float('-inf')
            for i in range(len(self.sequence) - 1):
                new_node = Node(self.sequence[:], self.player_score, self.ai_score, self.turn)
                new_node.make_move(i)
                eval = new_node.minimax(depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(len(self.sequence) - 1):
                new_node = Node(self.sequence[:], self.player_score, self.ai_score, self.turn)
                new_node.make_move(i)
                eval = new_node.minimax(depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval
    
    def alpha_beta(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or len(self.sequence) == 1:
            return self.evaluate_state()
        
        if maximizing_player:
            max_eval = float('-inf')
            for i in range(len(self.sequence) - 1):
                new_node = Node(self.sequence[:], self.player_score, self.ai_score, self.turn)
                new_node.make_move(i)
                eval = new_node.alpha_beta(depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(len(self.sequence) - 1):
                new_node = Node(self.sequence[:], self.player_score, self.ai_score, self.turn)
                new_node.make_move(i)
                eval = new_node.alpha_beta(depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
    
    def find_best_move(self, depth=3, method='alpha-beta'):
        best_score = float('-inf')
        best_index = None
        
        for i in range(len(self.sequence) - 1):
            new_node = Node(self.sequence[:], self.player_score, self.ai_score, self.turn)
            new_node.make_move(i)
            
            if method == 'minimax':
                score = new_node.minimax(depth - 1, False)
            else:
                score = new_node.alpha_beta(depth - 1, float('-inf'), float('inf'), False)
            
            if score > best_score:
                best_score = score
                best_index = i
        
        return best_index
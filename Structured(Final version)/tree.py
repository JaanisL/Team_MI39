# tree.py
import networkx as nx

class Tree:
    def __init__(self, initial_sequence):
        self.root = tuple(initial_sequence)
        self.graph = nx.DiGraph()
        self.graph.add_node(self.root, level=0)

    def generate_tree(self, state, depth=3, level=1):
        if depth == 0 or len(state) == 1:
            return

        for i in range(len(state) - 1):
            new_state = list(state)
            sum_val = new_state[i] + new_state[i + 1]
            new_state[i] = 1 if sum_val > 7 else 3 if sum_val < 7 else 2
            del new_state[i + 1]
            new_state_tuple = tuple(new_state)

            if new_state_tuple not in self.graph:
                self.graph.add_node(new_state_tuple, level=level)
                self.graph.add_edge(state, new_state_tuple)
                self.generate_tree(new_state_tuple, depth - 1, level + 1)

    def get_graph(self):
        return self.graph
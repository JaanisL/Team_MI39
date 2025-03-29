from node import Node
class Tree:
    def __init__(self, initial_sequence, player_score=0, ai_score=0, turn=1, depth_limit=3):
        self.root = Node(initial_sequence, player_score, ai_score, turn)
        self.nodes = [self.root]
        self.depth_limit = depth_limit
        self.generate_tree(self.root)

    def generate_tree(self, node, depth=0):
        if depth >= self.depth_limit or len(node.sequence) == 1:
            return
        
        node.children = node.get_children()
        for child in node.children:
            self.nodes.append(child)
            self.generate_tree(child, depth + 1)

    def print_all(self):
        sorted_list = sorted(self.nodes, key=lambda x: x.id)
        for node in sorted_list:
            s = f"Sequence: {node.sequence} | Children: ["
            for child in node.children:
                s += f"Sequence: {child.sequence},"
            s = s.rstrip(", ") + "]"
            print(s)

    def print_tree(self):
        print(f"Root: Sequence: {self.root.sequence}")
        self.__get_tree(0, self.root)

    def __get_tree(self, indent, node):
        print("-" * indent + f"Sequence: {node.sequence}")
        for child in node.children:
            self.__get_tree(indent + 3, child)

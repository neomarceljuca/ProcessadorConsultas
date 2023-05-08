import graphviz
from graphviz import Digraph


class TreeGraph:
    def __init__(self, nodes, edges, output_path):
        self.nodes = nodes
        self.edges = edges
        self.output_path = output_path
        
    def generate_tree(self):
        dot = Digraph(comment='Tree Graph')
        for node in self.nodes:
            dot.node(node)
        for edge in self.edges:
            dot.edge(edge[0], edge[1])
        dot.render(self.output_path, format='png')
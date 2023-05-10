import graphviz
from graphviz import Digraph


class TreeGraph:
    def __init__(self, inputExpression, output_path):
        #self.nodes
        #self.edges
        self.output_path = output_path
        self.dot = Digraph(comment= "Query Tree Graph")
        self.inputExpression = inputExpression
        
    def generate_tree(self):
        dot = Digraph(comment='Tree Graph')
        for node in self.nodes:
            dot.node(node)
        for edge in self.edges:
            dot.edge(edge[0], edge[1])
        dot.render(self.output_path, format='png')

    #query tree generation
    def generate_queryTree(self):
        #self.dot = Digraph(comment= "Query Tree Graph")
        self.recursiveQueryTree(self.inputExpression)
        self.dot.render(self.output_path, format='png')

    def recursiveQueryTree(self, expression):
        if expression.isspace():
            return
        else:
            #remove string outside brackets
            #if there is brackets in the entire expression, remove first and last brackets
            #call recursiveQueryTree(modifiedExpresion) and possibly branch in case of join clause

    #aux methods
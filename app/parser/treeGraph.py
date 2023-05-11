import re

import graphviz
from graphviz import Digraph


class TreeGraph:
    def __init__(self, inputExpression, output_path):
        self.output_path = output_path
        self.dot = Digraph(comment= "Query Tree Graph")
        self.inputExpression = inputExpression
        self.tree = Tree()
        
    def generate_tree(self):
        dot = Digraph(comment='Tree Graph')
        for node in self.nodes:
            dot.node(node)
        for edge in self.edges:
            dot.edge(edge[0], edge[1])
        dot.render(self.output_path, format='png')

    def treatString(self, expression):
        remainder = []
        trimmedExpression = ""
        stack = []
        indexToBeginningOfTrimmed = -1
        i = 0 
        ignoredCharacters = ['\t', " "]

        while i < len(expression):
            character = expression[i]
            if character == '(':
                if trimmedExpression != "": #found other opening brackets but already have a trimmedExpression; split expression and return
                    if (not expression[:indexToBeginningOfTrimmed].isspace()) and expression[:indexToBeginningOfTrimmed] != "":
                        remainder.append(expression[:indexToBeginningOfTrimmed].strip())
                    remainder.append(expression[i:].strip())
                    break
                else:
                    stack.append(character)
            elif character == ')':
                    stack.pop()
            else:
                if len(stack) > 0:
                    i = i + 1
                    continue
                else: #found expression outside brackets
                    if character not in ignoredCharacters:
                        if indexToBeginningOfTrimmed == -1:
                            indexToBeginningOfTrimmed = i
                        trimmedExpression += character                               
            i = i + 1
            
        if expression != "" and trimmedExpression == "": 
            return ( self.treatString(str(expression[1:-1])) )  #execute again with outter brackets trimmed
        if trimmedExpression != "" and remainder == []: #trimmedExpression was at the very end of the input
            if expression[:indexToBeginningOfTrimmed] != "":
                remainder.append(expression[:indexToBeginningOfTrimmed].strip())

        return trimmedExpression, remainder

    #query tree generation
    def generate_queryTree(self):
        #self.dot = Digraph(comment= "Query Tree Graph")
        self.recursiveQueryTree(self.inputExpression)
        #self.tree.print_tree()
        self.nodes, self.edges = self.tree.to_dot()
        self.generate_tree()
        #self.dot.render(self.output_path, format='png')

    def recursiveQueryTree(self, expression):
        if expression.isspace():
            return None
        else:
            #split string outside brackets from remaining expression
            trimmedExpression, remainder = self.treatString(expression)
            #call recursiveQueryTree(modifiedExpresion) and possibly branch in case of join clause
            if trimmedExpression == "":
                return None
            createdNode = TreeNode(trimmedExpression)
            if self.tree.get_root() == None:
                self.tree.set_root(createdNode)
            for remainderString in remainder:
                if trimmedExpression != "" and remainderString != "":
                    createdNode.add_child(self.recursiveQueryTree(remainderString))
            return createdNode
        
class TreeNode:
    def __init__(self, value=None):
        self.value = value
        self.children = []
    
    def add_child(self, node):
        self.children.append(node)
    
    def remove_child(self, node):
        self.children.remove(node)
    
    def get_children(self):
        return self.children
    
    def get_value(self):
        return self.value
    
    def set_value(self, value):
        self.value = value


class Tree:
    def __init__(self, root=None):
        self.root = root
    
    def set_root(self, node):
        self.root = node
    
    def get_root(self):
        return self.root
    
    def depth_first_traversal(self):
        visited = []
        self._depth_first_traversal(self.root, visited)
        return visited
    
    def _depth_first_traversal(self, node, visited):
        visited.append(node.get_value())
        children = node.get_children()
        for child in children:
            self._depth_first_traversal(child, visited)

    def to_dot(self):
        # Example list of nodes
        #nodes = ['A', 'B', 'C', 'D', 'E', 'F']
        # Example list of edges
        #edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'), ('C', 'F')]
        nodes = []
        edges = []
        self._to_dot(self.root, nodes, edges)
        return nodes, edges
    
    def _to_dot(self, node, nodes, edges):
        nodes.append(f"{node.get_value()}")
        children = node.get_children()
        for child in children:
            edges.append((f"{node.get_value()}", f"{child.get_value()}"))
            self._to_dot(child, nodes, edges)
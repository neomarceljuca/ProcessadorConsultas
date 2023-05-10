import re

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
            trimmedExpression, remainingExpression = treatString(expression)
            
            #if there is brackets in the entire expression, remove first and last brackets
            #call recursiveQueryTree(modifiedExpresion) and possibly branch in case of join clause

    #aux methods
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
                        remainder.append(expression[:indexToBeginningOfTrimmed])
                    remainder.append(expression[i:])
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
            remainder.append(expression[:indexToBeginningOfTrimmed])

        return trimmedExpression, remainder
    

    # def GPTtreatString(expression):
    #     if '(' not in expression and ')' not in expression:
    #         return expression, []

    #     stack = []
    #     trimmedExpression = ""
    #     remainingExpressions = []
    #     i = 0
    #     while i < len(expression):
    #         if expression[i] == '(':
    #             stack.append('(')
    #             if trimmedExpression == "" and len(stack) == 1:
    #                 trimmedExpression = expression[:i].strip()
    #                 expression = expression[i:]
    #                 i = -1
    #         elif expression[i] == ')':
    #             if stack and stack[-1] == '(':
    #                 stack.pop()
    #             if not stack and trimmedExpression == "":
    #                 trimmedExpression = expression[:i+1].strip()
    #                 expression = expression[i+1:]
    #                 i = -1
    #         i += 1

    #     if trimmedExpression and trimmedExpression[0] == '(' and trimmedExpression[-1] == ')':
    #         return treatString(trimmedExpression[1:-1])

    #     if expression:
    #         remainingExpressions.append(expression)

    #     return trimmedExpression, remainingExpressions
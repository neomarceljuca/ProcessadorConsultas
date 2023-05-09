import re
import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
import networkx as nx
from processor import Operator, QueryProcessor
from sql_parser import SQLParser


class GraphNode:
    def __init__(self, label, children=None):
        self.label = label
        self.children = children if children else []

    def add_child(self, child):
        self.children.append(child)


class QueryProcessorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Processador de Consultas")
        self.geometry("800x600")

        self.create_widgets()

    def dict_to_relational_algebra(self, query_dict):
        a = query_dict['select'][0]
        select = ", ".join(a)
        from_clause = query_dict['from']

        join_clause = ""
        if 'joins' in query_dict and query_dict['joins'] is not None:
            join_table = query_dict['joins'][0]['table']
            join_condition = f"{query_dict['joins']['left']} = {query_dict['joins']['right']}"
            join_clause = f"|X| {join_condition} {join_table}"

        where_clause = ""
        if 'where' in query_dict and query_dict['where'] is not None:
            where = " ∧ ".join([f"{k} = '{v}'" for k, v in query_dict['where'].items()])
            where_clause = f"({where})"

        relational_algebra = f"{select} ({from_clause} {join_clause} {where_clause})"
        return relational_algebra.strip()

    def algebra_to_query_graph(self, relational_algebra):
        # Gera um grafo de operadores a partir da álgebra relacional
        root = GraphNode("root")

        projections = GraphNode("Π", [GraphNode(column) for column in
                                      re.findall(r"Π (.*?)\(", relational_algebra)[0].split(', ')])
        root.add_child(projections)

        selections = GraphNode("σ", [GraphNode(condition) for condition in
                                     re.findall(r"σ (.*?)\(", relational_algebra)[0].split(' ∧ ')])
        projections.add_child(selections)

        join_nodes = [GraphNode("⨝", [GraphNode(condition)]) for condition in
                      re.findall(r"⨝_(.*?) ", relational_algebra)]
        if join_nodes:
            for i, join_node in enumerate(join_nodes):
                if i == 0:
                    selections.add_child(join_node)
                else:
                    join_nodes[i - 1].add_child(join_node)

                join_node.add_child(GraphNode(re.findall(r" (.*?) ⨝", relational_algebra)[i]))

            join_nodes[-1].add_child(GraphNode(re.findall(r" ⨝.*? (.*?)\)", relational_algebra)[0]))
        else:
            selections.add_child(GraphNode(re.findall(r"\((.*?)\)", relational_algebra)[0]))

        return root

    def create_widgets(self):
        self.query_entry = ttk.Entry(self, width=80)
        self.query_entry.pack(pady=10)

        self.execute_button = ttk.Button(self, text="Executar Consulta", command=self.process_query)
        self.execute_button.pack(pady=10)

        self.result_text = tk.Text(self, wrap=tk.WORD, width=80, height=20)
        self.result_text.pack(pady=10)

    def draw_query_graph(self, node, G=None, parent=None):
        if G is None:
            G = nx.DiGraph()

        G.add_node(node.label)
        if parent is not None:
            G.add_edge(parent.label, node.label)

        for child in node.children:
            self.draw_query_graph(child, G, node)

        return G

    def visualize_query_graph(self, query_graph):
        G = self.draw_query_graph(query_graph)
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', font_size=8, node_size=3000, font_weight='bold',
                arrows=True)
        plt.show()

    def process_query(self):
        query = self.query_entry.get()

        try:
            parser = SQLParser(query)
            parsed_query = parser.parse()
            #relational_algebra = self.dict_to_relational_algebra(parsed_query)
            #query_graph = self.algebra_to_query_graph(relational_algebra)
            #self.visualize_query_graph(query_graph)
            # transformed_query = parser.sql_dict_to_relational_algebra(parsed_query)
        except Exception as e:
            print(str(e))
            # Exibir mensagem de erro no campo de texto
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Erro ao analisar a consulta:\n\n")
            self.result_text.insert(tk.END, str(e))
            return

        # Implementar o processamento da consulta aqui
        # ...

        # Exibir os resultados no campo de texto
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Resultados da consulta:\n\n")
        self.result_text.insert(tk.END, str(parsed_query))  # Exibe a consulta analisada


if __name__ == "__main__":
    app = QueryProcessorApp()
    app.mainloop()

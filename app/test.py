import re
from collections import defaultdict

def apply_heuristics(relational_algebra):
    # Aplica heurísticas na álgebra relacional e retorna a árvore de consulta otimizada
    # Para simplificar, vamos assumir que a álgebra relacional possui apenas seleções, projeções e junções

    # 1. Seleções
    selections = re.findall(r'σ\s*\(.*?\)', relational_algebra)

    # 2. Projeções
    projections = re.findall(r'Π\s*\(.*?\)', relational_algebra)

    # 3. Junções
    joins = re.findall(r'⨝.*?\s', relational_algebra)

    # Reordenar os nós folha da árvore de consulta
    leaf_nodes = defaultdict(list)
    for sel in selections:
        table = re.findall(r'\((.*?)\)', sel)[0]
        leaf_nodes[table].append(sel)

    # Evitar operações de produto cartesiano
    # Ajustar o restante da árvore de forma apropriada
    # Como a álgebra relacional fornecida já possui junções,
    # vamos assumir que não há produtos cartesianos

    # Construir a árvore de consulta otimizada
    optimized_query_tree = ""
    for join in joins:
        table = re.findall(r'⨝(.*?)_', join)[0].strip()
        conditions = ' ∧ '.join(leaf_nodes[table])
        optimized_query_tree += f"({conditions})({table}) {join} "
    optimized_query_tree = optimized_query_tree.strip()

    # Adicionar projeções ao topo da árvore
    for proj in projections:
        optimized_query_tree = f"{proj} ({optimized_query_tree})"

    return optimized_query_tree

def generate_query_graph(relational_algebra):
    # Gera um grafo de operadores a partir da álgebra relacional
    graph = defaultdict(list)

    # Processa as operações da álgebra relacional e gera o grafo
    operations = re.findall(r'([Πσ⨝].*?)\s*\(', relational_algebra)
    for op in operations:
        node = op.strip()
        children = re.findall(r'\(.*?\)', relational_algebra)
        for child in children:
            child = child.strip("()").replace(" ", "")
            graph[node].append(child)
            relational_algebra = relational_algebra.replace(child, "", 1)

    return graph


def print_query_graph(query_graph):
    # Exibe o grafo de operadores
    for node, children in query_graph.items():
        for child in children:
            print(f"{node} -> {child}")

relational_algebra = "Π nome, datanascimento, descricao, saldoinicial (σ (descricao not in ('1', '2', '3') ∧ saldoinicial >= 235 ∧ uf = 'ce' ∧ cep <> '62930000' ∧ cep in (1, 2, 3) ∧ uf = 'jp') ((usuario) ⨝_usuario.idusuario = contas.usuario_idusuario contas))"
query_graph = generate_query_graph(relational_algebra)
print_query_graph(query_graph)
class Operator:
    def __init__(self, type_, name=None, data=None, columns=None, conditions=None, condition=None):
        self.type = type_
        self.name = name
        self.data = data
        self.columns = columns
        self.conditions = conditions
        self.condition = condition
        self.children = []

    def add_child(self, operator):
        self.children.append(operator)


class Graph:
    def __init__(self):
        self.operators = []

    def add_operator(self, operator):
        self.operators.append(operator)


class QueryProcessor:
    def __init__(self, graph):
        self.graph = graph

    def process(self):
        # Ordena os operadores de acordo com as heurísticas básicas
        operators = self.order_operators()

        # Executa a consulta
        results = self.execute_query(operators[0])

        # Retorna os resultados
        return results

    def order_operators(self):
        # Inicializa os dicionários de operadores e arestas
        operators_dict = {}
        edges_dict = {}
        for operator in self.graph.operators:
            operators_dict[operator.name] = operator
            edges_dict[operator.name] = set()

        # Cria as arestas do grafo de operadores
        for operator in self.graph.operators:
            for child in operator.children:
                edges_dict[operator.name].add(child.name)

        # Ordena os operadores
        ordered_operators = []
        while operators_dict:
            # Encontra os operadores sem dependências
            free_operators = {name for name, edges in edges_dict.items() if not edges}
            if not free_operators:
                raise Exception("Circular dependency in operators")
            # Adiciona os operadores sem dependências na lista ordenada
            ordered_operators.extend([operators_dict[name] for name in sorted(free_operators)])
            # Remove os operadores adicionados e suas arestas
            for operator in ordered_operators:
                operators_dict.pop(operator.name)
                for edges in edges_dict.values():
                    edges.discard(operator.name)

        return ordered_operators

    def execute_query(self, operator):
        if operator.type == "table":
            # Retorna os dados da tabela
            return operator.data
        elif operator.type == "select":
            # Executa a operação de seleção
            results = self.execute_query(operator.children[0])
            for condition in operator.conditions:
                results = self.apply_condition(results, condition)
            # Executa a operação de projeção
            columns = [self.get_column_index(results, column) for column in operator.columns]
            results = [[row[column] for column in columns] for row in results]
            return results
        elif operator.type == "join":
            # Executa a operação de junção
            left_data = self.execute_query(operator.children[0])
            right_data = self.execute_query(operator.children[1])
            left_index = self.get_column_index(left_data, operator.condition[0])
            right_index = self.get_column_index(right_data, operator.condition[2])
            results = []
            for left_row in left_data:
                for right_row in right_data:
                    if left_row[left_index] == right_row[right_index]:
                        results.append(left_row + right_row)
            return results

    def apply_condition(self, data, condition):
        column_index = self.get_column_index(data, condition[0])
        if condition[1] == "=":
            return [row for row in data if row[column_index] == condition[2]]
        elif condition[1] == ">":
            return [row for row in data if row[column_index] > condition[2]]
        elif condition[1] == "<":
            return [row for row in data if row[column_index] < condition[2]]
        elif condition[1] == ">=":
            return [row for row in data if row[column_index] >= condition[2]]
        elif condition[1] == "<=":
            return [row for row in data if row[column_index] <= condition[2]]
        elif condition[1] == "<>":
            return [row for row in data if row[column_index] != condition[2]]
        elif condition[1] == "in":
            return [row for row in data if row[column_index] in condition[2]]
        elif condition[1] == "not in":
            return [row for row in data if row[column_index] not in condition[2]]
        else:
            raise Exception("Invalid condition operator: " + condition[1])

    def get_column_index(self, columns, column_name):
        for i in range(len(columns)):
            if columns[i].strip() == column_name.strip():
                return i
        raise Exception("Column not found: " + column_name)
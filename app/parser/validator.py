import re
from itertools import chain


class SQLQueryValidator:
    def __init__(self, table_fields):
        self.table_fields = table_fields
        self.table_pattern = r"\b(" + "|".join(self.table_fields.keys()) + r")\b"
        self.field_pattern = (
            r"(?<!\w)("
            + "|".join(list(chain.from_iterable(self.table_fields.values())))
            + r")(?!\w)"
        )

        self.operator_pattern = r"(?i)(\s+(?:AND|OR)\s+)+"
        
        #self.query_pattern = r"(?i)SELECT\s+(?P<fields>{0}(?:\s*,\s*{0})*)\s+FROM\s+(?P<tables>{1})\s+(?P<join>JOIN\s+{1}\s+ON.+?)?(?:\s+WHERE\s+(?P<conditions>.+?))?(?:\s+ORDER\s+BY\s+(?P<order_by>.+))?;".format(self.field_pattern, self.table_pattern)

        #JoinOld
        self.query_pattern = r"(?i)SELECT\s+({0}(?:\s*,\s*{0})*)\s+FROM\s+({1})(?:\s+(?:JOIN|INNER JOIN|LEFT JOIN|RIGHT JOIN|FULL OUTER JOIN)\s+({1})\s+ON\s+(.+?))?(?:\s+WHERE\s+(.+?))?(?:\s+ORDER\s+BY\s+(.+))?;".format(self.field_pattern, self.table_pattern)
       
        #Old
        #self.query_pattern = r"(?i)SELECT\s+({0}(?:\s*,\s*{0})*)\s+FROM\s+({1})(?:\s+WHERE\s+(.+?))?(?:\s+ORDER\s+BY\s+(.+))?;".format(self.field_pattern, self.table_pattern)


    def validate_query(self, sql_query):
        table_matches = re.findall(self.table_pattern, sql_query)

        # Verifica se há alguma correspondência de tabelas encontradas na consulta SQL
        if not table_matches:
            return False

        # Verifica se a consulta SQL está no formato esperado
        if not re.match(self.query_pattern, sql_query):
            return False
        
        # Verifica se todas as tabelas na consulta existem no dicionário de tabelas e campos válidos
        if not all(table in self.table_fields for table in table_matches):
            return False

        #Verifica se a quantidade de campos eh multiplo da quantidade de tabelas
        field_matches = [match.group() for match in re.finditer(self.field_pattern, sql_query)]
        if len(field_matches) % len(table_matches) != 0:
            return False

        # Verifica se todos os campos na consulta existem no dicionário de campos válidos
        for field, table in zip(field_matches, table_matches):
            if field not in self.table_fields[table]:
                print(f"{field} is not a valid field for table {table}")
                return False
        return True

    def validate_queryOld(self, sql_query):
        table_matches = re.findall(self.table_pattern, sql_query)
        if not table_matches:
            return False

        if not re.match(self.query_pattern, sql_query):
            return False

        if not all(table in self.table_fields for table in table_matches):
            return False

        field_matches = list(
            chain.from_iterable(re.findall(self.field_pattern, sql_query))
        )
        for field, table in zip(field_matches, table_matches):
            if field not in self.table_fields[table]:
                print(f"{field} is not a valid field for table {table}")
                return False
        return True

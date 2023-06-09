from treeGraph import TreeGraph
from validator import SQLQueryValidator

# Create SQL query validator instance
validator = SQLQueryValidator()
#parser = Parser()

# # Sample SQL queries to validate
# query1 = "Select id, name, email From users Where id = 1;"
# query2 = "SELECT name, price FROM productsThisTableDoesntExist WHERE price < 10.0 ORDER BY name;"
# query3 = "SELECT Nome, DataNascimento, Descricao, SaldoInicial FROM Usuario join Contas on Usuario.idUsuario = Contas.Usuario_idUsuario WHERE SaldoInicial >= 235 and UF ='ce' and CEP <> '62930000';"
# query4 = "SELECT idusuario, nome, datanascimento, descricao, saldoinicial, UF, Descrição FROM usuario join contas on usuario.idUsuario = contas.Usuario_idUsuario join tipoconta on tipoconta.idTipoConta = contas.TipoConta_idTipoConta WHERE saldoinicial < 3000 and uf = 'ce' and Descrição <> 'Conta Corrente' and idusuario > 3; "
# query5 = "SELECT idUsuario FROM Usuario JOIN Contas ON Usuario.idUsuario = Contas.Usuario_idUsuario;"
# query6 = "SELECT idUsuario FROM Usuario;"
# # Validate SQL queries
# print(validator.validate_query(query1))  # True
# print(validator.validate_query(query2))  # False
# print(validator.validate_query(query3))  # True
# print(validator.validate_query(query4))  # True
# print(validator.validate_query(query5))  # True
# print(validator.validate_query(query6))  # True


#test1 Select Tb1.Nome, tb3.sal From Tb1 Join Tb2 on tb1.pk = tb2.fk Join tb3 on tb2.pk = tb3.fk Where tb1.id > 300 and tb3.sal <> 0;

inputString = "	( (A(B(C))) D (E(F))) G (H((I (J))))"
output_path = './app/RelationalTree'
#Create a TreeGraph object, generate and export the graph as 'RelationalTree.png'
tree = TreeGraph(inputString, output_path)

cases = [
    "( (A(B(C))) D (E(F))) GEEE (H((I (J))))",
    "GEEE (H((I (J))))",
    "( (A(B(C))) D (E(F))) GEEE",
    "GEEE",
    "((GEE))",
    ""
    ]
for case in cases:
    print(tree.treatString(case))  


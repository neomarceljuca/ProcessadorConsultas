import re

query = "JOIN contas ON usuario.idUsuario = contas.Usuario_idUsuario"

padrao = r"(?<=ON\s).*"

clausula_onde = re.search(padrao, query).group()

print(clausula_onde)
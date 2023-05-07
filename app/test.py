array1 = ['tb1.pk', 'tb2.fk', 'tb2.pk', 'tb3.fk', 'Tb1.Nome', 'tb3.sal']
array2 = [2, 4]

result = [array1[idx] for idx in array2]

print(result)  # ['tb1.pk', 'Tb1.Nome']

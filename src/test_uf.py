import modod.uf as uf
x = uf.UF(map(chr, range(65, 70)))
print("Initialize UF with A ... E : ", x)
for y in map(chr, range(70, 75)):
    x.makeset(y)
    print("Add ", y, " : ", x)
print(x)

unions = [
    ('A', 'B'), ('C', 'E'), ('G', 'J'),
    ('B', 'F'), ('G', 'H'), ('I', 'A'),
    ('D', 'C'), ('H', 'E'), ('A', 'E')
]

for a,b in unions:
    x.union(a, b)
    print("Uniting ",a,", ",b," : ",x)
    

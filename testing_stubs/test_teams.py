from teams import Teams

p1 = Teams(list("A B C D E F G".split()))
print(p1.randomizer())
print()
p1.remove('G')
print(p1.randomizer())
p1.add('Vibha')
print()
print(p1.randomizer())
p1.Clear()
print()
while 1:
    x = p1.randomizer()
    if (x == None or x == []):
        break
    #print(p1.manipulate)
    #print()
    print(x)
    print()

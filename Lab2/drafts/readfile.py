f=open('./input.txt')
txt=[]
for line in f:
    txt.append(line.strip())
    word = line.split()
    print("word is ",word)
    for i in word:
        i = i.strip(',')[1:]
        print("i = {}".format(i))
print(txt)

str = 'hongmao123lantu456'
s = ''.join([x for x in str if x.isdigit()])
print(s)
#output : 123456

str = 'hongmao123lantu456'
s = ''.join([x for x in str if x.isalpha()])
print(s)
#output:hongmaolantu


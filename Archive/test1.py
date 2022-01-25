words = input("")
words = words.split(",")
#words = ['Test','andnasd','a','a','the','yes']

min_value = len(words[0])

lens = []

for x in words:
    lens.append([len(x),x])

lens.sort()
#print(lens)

min_val = lens[0][0]
second = 9999

for y in lens[1::]:
    if y[0] == min_val :
        continue
    elif y[0] > second:
        break
    #print(y[1])
    second = y[0]
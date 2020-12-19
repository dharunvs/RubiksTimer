import random
moves = ['R', 'U', 'D', 'B', 'F', 'L', 'R\'', 'U\'', 'D\'',
         'B\'', 'F\'', 'L\'', 'R2', 'U2', 'D2', 'B2', 'F2']
lst = []
txt = ""


def scramble():
    string = ""
    for i in range(random.randint(15, 20)):
        string += f"{random.choice(moves)} "

    return(string)


def text(n):
    global txt
    for i in range(n):
        lst.append(scramble())
    for i in lst:
        txt += f"{i}\n"


def run():
    inp = int(input("Number of patterns = "))
    text(inp)
    print(txt)
    with open("temp.txt", 'w') as f:
        f.write(txt)

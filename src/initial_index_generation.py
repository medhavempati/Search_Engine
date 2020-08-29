decl = ""

for f in 'abcdefghijklmnopqrstuvwxyz':
    for s in 'abcdefghijklmnopqrstuvwxyz':
        decl = decl + "'" + str(f) + str(s) + "':{}, "

decl = decl[:-2]
decl += " }"
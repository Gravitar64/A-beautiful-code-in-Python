from random import shuffle

liste = "amazing gorgeous blazing stunning tremendous greatest best fantastic phenomenal \
         delightful ambitious outstanding incredible spectacular super cool magical \
         revolutionary beautiful jaw-dropping".upper().split()
shuffle(liste)

for strophe in range(5):
    for n a in range(2):
        for i in range(4):
             print("SPAM ", end='')
        print()
    el1 = liste.pop()
    el2 = liste.pop()

    print("{} SPAM, {} SPAM".format(el1, el2))
    print()

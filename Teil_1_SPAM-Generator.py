from random import shuffle

superlatives = "amazing gorgeous blazing stunning tremendous greatest best fantastic \
               phenomenal delightful ambitious outstanding incredible spectacular \
               super cool magical revolutionary beautiful jaw-dropping lovely".upper().split()
shuffle(superlatives)

for strophe in range(5):
    for zeile in range(2):
        for word in range(4):
            print("SPAM ", end='')
        print()
    el1 = superlatives.pop()
    el2 = superlatives.pop()

    print("{} SPAM, {} SPAM".format(el1, el2))
    print()

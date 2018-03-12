from random import shuffle

superlative = "amazing gorgeous blazing stunning tremendous greatest best fantastic \
               phenomenal delightful ambitious outstanding incredible spectacular \
               super cool magical revolutionary beautiful jaw-dropping lovely".upper().split()
shuffle(superlative)

for strophe in range(5):
    for zeile in range(2):
        for word in range(4):
            print("SPAM ", end='')
        print()
    el1 = superlative.pop()
    el2 = superlative.pop()

    print("{} SPAM, {} SPAM".format(el1, el2))
    print()

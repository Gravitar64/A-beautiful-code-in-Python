import turtle

hilbert_seq = "b"

for _ in range(5):
    new_seq = ""
    for char in hilbert_seq:
        if char == "a":
            new_seq += "-bF+aFa+Fb-"
        elif char == "b":
            new_seq += "+aF-bFb-Fa+"
        else:
            new_seq += char
    hilbert_seq = new_seq

for char in hilbert_seq:
    if char == "F":
        turtle.forward(9)
    elif char == "+":
        turtle.right(90)
    elif char == "-":
        turtle.left(90)
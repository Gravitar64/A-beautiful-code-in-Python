import turtle


def fib(n):
  if n < 2: return n
  return fib(n-1) + fib(n-2)


def draw_quadrat(size):
  for _ in range(4):
    x.forward(size)
    x.right(90)
  x.forward(size)
  x.right(90)
  x.forward(size)


def fiboPlot(n):
  x.pensize(3)
  x.pencolor("grey")
  for i in range(n):
    draw_quadrat(fib(i)*SCALE)

  x.penup()
  x.goto(START)
  x.pendown()
  x.pencolor("blue")
  x.pensize(10)
  x.setheading(180)
  for i in range(n):
    x.circle(-SCALE*fib(i), 90)


START, SCALE = (-400, -200), 7

x = turtle.Turtle()
x.penup()
x.goto(START)
x.pendown()
x.speed(5)
fiboPlot(13)
turtle.done()

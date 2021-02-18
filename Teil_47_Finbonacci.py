import turtle


def fib(n,tiefe=0):
  if n < 2: return n
  print(' '*tiefe, n)
  a = fib(n-1, tiefe +1)
  print(' '*tiefe + f'fib({n-1}) = ',a)
  b = fib(n-2, tiefe +1)
  print(' '*tiefe + f'fib({n-2}) = ',b)
  return a + b
  


def draw_quadrat(size):
  
  for _ in range(4):
    x.forward(size)
    x.right(90)
  x.forward(size)
  x.right(90)
  x.forward(size)


def fiboPlot(n):
  fibseq = ''
  t1 = turtle.Turtle()
  t1.penup()
  t1.setposition(-600,400)
  t1.pendown()
  x.pensize(3)
  x.pencolor("grey")
  for i in range(n):
    fibseq += str(fib(i))+', '
    t1.write(fibseq,font=('Arial',48,'normal'))
    draw_quadrat(fib(i)*SCALE)

  x.penup()
  x.goto(START)
  x.pendown()
  x.pencolor("blue")
  x.pensize(10)
  x.setheading(180)
  for i in range(n):
    x.circle(-SCALE*fib(i), 90)

print(fib(10))

START, SCALE = (-400, -200), 7

x = turtle.Turtle()
x.penup()
x.goto(START)
x.pendown()
x.speed(5)
fiboPlot(13)
turtle.done()

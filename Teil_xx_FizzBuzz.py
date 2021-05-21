def fizzbuzz(n, output=''):
  if not n % 3: output += 'Fizz'
  if not n % 5: output += 'Buzz'
  return output or n


for i in range(100):
  a = fizzbuzz(i)
  b = "Fizz"* (not i%3) + "Buzz" * (not i%5) or i
  if a != b: print(a,b)
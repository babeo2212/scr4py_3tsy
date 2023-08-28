def itl(a):
  for i in a:
      yield i
a = [1, 2, 3]

h = itl(a)
print(next(h))
print(next(h))
print(next(h))
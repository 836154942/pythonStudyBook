def source():
     n=1
     while True:
          n = n + 2
          yield n

def select(n):
   
          return lambda x: x% n>0
def start():
     n=3
     it =source()
     while True :
          n =  next(it)
          yield n
          it = filter(select(n),it)


def go():
     for i in start():
          if i<=100:
               print(i)
          else:
               break;

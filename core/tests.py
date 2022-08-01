from django.test import TestCase

# Create your tests here.

def posible_changes(usenames):
    
    pass

# x = lambda a : a + 10
# print(x(5))

# y = lambda a, b : a + b
# print(y(4,5))

def multipliers():
    return [lambda x: i * x for i in range(4)]
 
result = [m(2) for m in multipliers()]

print(result)
    

# def myfunc(n):
#     return lambda a: a * n
# mydoubler = myfunc(3)

# print(mydoubler(11))        
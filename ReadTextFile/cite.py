class CountFromBy:
    def __init__(self, v: int, i: int) -> None:
        self.val = v
        self.incr = i
    def increase(self)-> None:
        self.val += self.incr
        
    def __repr__(self) -> str:
        return str(self.val)


c = CountFromBy(10,2)
c.increase()
print(c)


# def soundbite(from_outside):
#     insider = 'James'
#     outsider = from_outside
#     print(from_outside, insider, outsider)
    
# name = 'Bond'
# soundbite(name)
# name
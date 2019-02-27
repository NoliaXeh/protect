

class PrivateMethod:
    def __init__(self, f):
        self.f = f
        self.__name__ = f.__name__
        self.__str__ = lambda self : f"<PrivateMethod {self.__name__}>"
    def __call__(*args, **kwargs):
        raise Exception("Cannot access private member") 

def private(f):
    return PrivateMethod(f)

def trace(f):
    return lambda *args, **kwargs : print("called", f.__name__); f

def better(obj):
    class Meta(obj):
        def __init__(self, *args, **kwargs):
            obj.__init__(self, *args, **kwargs)
            for k, v in obj.__dict__.items():
                self.__dict__["__old__" + k] = v
            tmp = {}
            for k, v in self.__dict__.items():
                if callable(v):
                    print(v, callable(v))
                    tmp[k[7:]] = lambda *args, **kwargs : v(self, *args, **kwargs)
                else:
                    tmp[k[7:]] = v
            self.__dict__.update(tmp)
            for k, v in self.__dict__.items():
                print(f"{k: <20} -> {v}")
    return Meta

@better
class Test:
    def __init__(self):
        self._x = 42

    @private
    def add(self):
        self._x += 42

    def __str__(self):
        return f"x = {self._x}"


'''
t = Test()
print(t.add)
print(callable(t.add))
print(t)
print(t.add)
t.add()
'''
@private
def lol():
    print(123)

lol()

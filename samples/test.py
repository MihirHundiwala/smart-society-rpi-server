def f():
    x= 1
    def z():
        global x
        x+=1
        print(x)
    z()

f()
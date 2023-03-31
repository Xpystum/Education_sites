def outher():
    def inner():
        print("Это inner функция.")

    print("Это функция outher - которая вернула inner")
    return inner

def myfoo(*args):
    for a in args:
        print(a, end=' ')
    if args:
        print();

myfoo(20,30,40)
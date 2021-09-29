import taichi as ti
ti.init(ti.cpu)

# 测试foo和bar

d = 1
n = 3

def foo():
    d_python = d
    print("d_python = ", d_python)

@ti.kernel
def bar(n: int, d: int):
    d_taichi = d
    for i in range(n):
        d_taichi += 1
        print("d_taichi = ", d_taichi)

@ti.kernel
def kern():
    for i in range(100):
        print(i)



for i in range(n):
    d += i
    bar(n, d)
    foo()

# kern()

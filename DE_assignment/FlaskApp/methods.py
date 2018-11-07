from math import cos, sin, e as eps


def euler(x, h, ypr):
    y = []
    y.append(ypr)
    for i in x:
        new = ypr + h * f(i, ypr)
        y.append(round(new, 8))
        ypr = new
    return y


def improved_euler(x, h, ypr):
    y = []
    y.append(ypr)
    for i in x:
        new = ypr + h * f(i + round(h / 2, 8), ypr + round(h / 2, 8) * f(i, ypr))
        y.append(round(new, 8))
        ypr = new
    return y


def runge_kuffa(x, h, ypr):
    y = []
    y.append(ypr)
    for i in x:
        k1 = f(i, ypr)
        k2 = f(i + round(h / 2, 8), ypr + round(h / 2, 8) * k1)
        k3 = f(i + round(h / 2, 8), ypr + round(h / 2, 8) * k2)
        k4 = f(i + h, ypr + h * k3)
        new = ypr + round(h / 6, 8) * (k1 + 2 * k2 + 2 * k3 + k4)
        y.append(round(new, 8))
        ypr = new
    return y


def f(x, y):
    return cos(x) * (sin(x) - y)


def exact(x, C):
    return C * pow(eps, -sin(x)) + sin(x) - 1


def xl(x0, X, h):
    x = []
    while round(x0, 8) <= X:
        x.append(round(x0, 8))
        x0 += h
    return x

def getConstant(x0,y0):
    return float(y0-sin(x0)+1)/pow(eps,-sin(x0))
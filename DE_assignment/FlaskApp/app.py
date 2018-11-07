import json
from math import cos, sin, e as eps

from flask import Flask, render_template, request

app = Flask(__name__)


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


def exact(x):
    return 2 * pow(eps, -sin(x)) + sin(x) - 1


def xl(x0, X, h):
    x = []
    while round(x0, 8) <= X:
        x.append(round(x0, 8))
        x0 += h
    return x


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/getChart")
def get_chart():
    _from = float(request.args.get('from'))
    _to = float(request.args.get('to'))
    _step = float(request.args.get('step'))

    y0 = float(request.args.get('y0'))
    x = xl(_from, _to, _step)

    n0 = float(request.args.get('n0'))
    n = float(request.args.get('n'))

    euler_y = euler(x, _step, y0)
    impr_euler_y = improved_euler(x, _step, y0)
    runge_y = runge_kuffa(x, _step, y0)

    exact_res = [[x[i], exact(x[i])] for i in range(len(x))]
    euler_res = [[x[i], euler_y[i]] for i in range(len(x))]
    impr_euler_res = [[x[i], impr_euler_y[i]] for i in range(len(x))]
    runge_res = [[x[i], runge_y[i]] for i in range(len(x))]

    euler_err = [[euler_res[i][0], exact_res[i][1] - euler_res[i][1]] for i in range(len(euler_res))]
    impr_euler_err = [[impr_euler_res[i][0], exact_res[i][1] - impr_euler_res[i][1]] for i in
                      range(len(impr_euler_res))]
    runge_err = [[runge_res[i][0], exact_res[i][1] - runge_res[i][1]] for i in range(len(runge_res))]

    euler_total = []
    impr_euler_total = []
    runge_total = []

    for N in range(int(n0), int(n) + 1):
        h = float(_to - _from) / float(N)
        x = xl(_from, _to, h)

        euler1 = euler(x, h, y0)
        euler2 = [abs(exact(x[i]) - euler1[i]) for i in range(len(x))]
        euler_total.append([N, max(euler2)])

        impr_euler1 = improved_euler(x, h, y0)
        impr_euler2 = [abs(exact(x[i]) - impr_euler1[i]) for i in range(len(x))]
        impr_euler_total.append([N, max(impr_euler2)])

        runge1 = runge_kuffa(x, h, y0)
        runge2 = [abs(exact(x[i]) - runge1[i]) for i in range(len(x))]
        runge_total.append([N, max(runge2)])

    return json.dumps({
        "Exact": exact_res,
        "Euler": euler_res,
        "Improved_Euler": impr_euler_res,
        "Runge_Kutta": runge_res,
        "error_Runge_Kutta": runge_err,
        "error_Euler": euler_err,
        "error_Impr_Euler": impr_euler_err,
        "total_error_Euler": euler_total,
        "total_error_Impr_Euler": impr_euler_total,
        "total_error_Runge": runge_total
    })


if __name__ == "__main__":
    app.run()

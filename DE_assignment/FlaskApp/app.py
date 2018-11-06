import json
from math import  cos, sin

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

    # const = find_const(x0, y0)
    # print(improved_euler_method(funct, x0, y0, _to, _step)

    # exact_res = [[x, get_function_value(solved_funct, x, const)] for x in np.arange(_from, _to + _step, _step)]
    euler_y = euler(x, _step, y0)
    impr_euler_y = improved_euler(x, _step, y0)
    runge_y = runge_kuffa(x, _step, y0)

    euler_res = [[x[i], euler_y[i]] for i in range(len(x))]
    impr_euler_res = [[x[i], impr_euler_y[i]] for i in range(len(x))]
    runge_res = [[x[i], runge_y[i]] for i in range(len(x))]

    # euler_err = [[euler_res[x][0], exact_res[x][1] - euler_res[x][1]] for x in range(len(euler_res))]
    # impr_euler_err = [[impr_euler_res[x][0], exact_res[x][1] - impr_euler_res[x][1]] for x in range(len(impr_euler_res))]
    # runge_err = [[runge_res[x][0], exact_res[x][1] - runge_res[x][1]] for x in range(len(runge_res))]

    return json.dumps({

        "Euler": euler_res,
        "Improved_Euler": impr_euler_res,
        "Runge_Kutta": runge_res,
        # "error_Runge_Kutta": runge_err,
        # "error_Euler": euler_err,
        # "error_Impr_Euler": impr_euler_err
    })


if __name__ == "__main__":
    app.run()

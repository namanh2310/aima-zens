from latex2sympy2 import latex2sympy, latex2latex
from flask import request, jsonify
from sympy import *
import re
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from scipy.optimize import fsolve
import json
import os

def format_sketch_data(data):
    rhs = data.split('=')[-1].strip()
    lhs = data.split('=')[0].strip()
    expression_rhs = latex2sympy(rhs)
    expression_lhs = latex2sympy(lhs)
    expression = expression_lhs - expression_rhs
    return expression

def sketchGraph(data, solution, step):
    input = ''
    output = ''
    print('datatatataat', data)
    input = format_sketch_data(data)
    output = solution
    print("iiiinput", input)
    print("oooutput", output)
    
    if '=' in data:
        equation_string = input
        # expr = equation_string
        expr = simplify(equation_string)
        print("exprexprexprexprexprexprexprexprexpr", expr)
    elif 'x' in output:
        equation_string = output
        print("equation_stringequation_stringequation_string", equation_string)
        expr = simplify(latex2sympy(equation_string))
    else:
        return None

    x = symbols('x')
    func = lambdify(x, expr, "numpy")
    x_values = np.linspace(-2, 5, 400)
    y_values = func(x_values)   
    plt.figure(figsize=(8, 6))
    plt.plot(x_values, y_values, label=f'y = {latex(expr)}')
    plt.title('Graph of ' + f'y = {latex(expr)}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    # Save image
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    base64_encoded = base64.b64encode(buffer.read()).decode()

    plt.close()

    base64_data_uri = "data:image/png;base64," + base64_encoded

    return base64_data_uri
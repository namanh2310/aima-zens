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

from utils.CalModule import sketchGraph
from steps.Integral import handleIntegral


def handleEquation(step, expr, data, solution):
    # if len(solution) > 500:
    #     print(len(solution))
    rhs = expr.split('=')[-1].strip()
    lhs = expr.split('=')[0].strip()
    len_x = 0
    expression_rhs = latex2sympy(rhs)
    expression_lhs = latex2sympy(lhs)
    expression = expression_lhs - expression_rhs
    equation = Eq(expression, 0)
    x, y, u = symbols('x y u')
    
    try:
        poly_equation = Poly(equation.lhs, x)
        coefficients = poly_equation.all_coeffs()
        all_degrees = [degree(term) for term in poly_equation.as_expr().as_ordered_terms()]
    except Exception as e:
        coefficients = []
        all_degrees = []
    all_factors = factor(expression)
    ordered_factors = all_factors.as_ordered_factors()     
    rounded_vals = []

    def re_calc(values):
        for value in values:
            value = latex(value)
            value = value.replace(" i", "I")
            step.append("Substitute back \\(u = x^{2}\\) and solve for x")
            problem = f"x^2 = {value}"
            step.append(f"\\({latex2latex(problem)}\\)")

    def immediately_cal(equation):
        return latex2latex(equation)

    

    def rounded_cal(equation):
        latex_eq = latex(equation)
        if len(latex2latex(latex_eq)) > 200:
            if type(latex2sympy(latex_eq)[0]) == type(Eq(x, 1)):
                print(True)
            else:
                print(False)
            for i in latex2sympy(latex_eq):
                expression = i
                result = expression.rhs.evalf()
                rounded_result = round(result, 4)
                rounded_vals.append(str(rounded_result))
            return rounded_vals
        else:
            return immediately_cal(latex_eq)
    print(len(solution))
  

    def quadric_cal(equation):
        a = coefficients[0]
        b = coefficients[1]
        c = coefficients[2]
        delta = b**2 - 4*a*c
        step.append(f"First, we have to check by calculating: \\(\\Delta = b^{2} - 4ac\\) = {delta}")
        if delta > 0:
            step.append("Because \\(\\Delta > 0 \\), so the equation has two solutions, which can be calculated by:")
            x1 = (-b + sqrt(delta))/ (2*a)
            x2 = (-b - sqrt(delta))/ (2*a)
            step.append(f"\\(\\frac{{-b \\pm \\sqrt{{\\Delta}}}}{{2a}}\\)")
            step.append(f"Value of \\(x_1 = {latex(x1)}\\) and \\(x_2 = {latex(x2)}\\)")
        elif delta == 0:
            step.append("Because \\(\\Delta = 0 \\), so the equation has one solution, which can be calculated by:")
            x = -b/ (2*a)
            step.append(f"\\(\\frac{{-b}}{{2a}}\\)")
            step.append(f"Value of \\(x = {latex(x)}\\)")
        else:
            step.append("Because \\(\\Delta < 0 \\), so the equation has no solution")
            step.append("It only has complex values:")
            step.append(f"\\(x = {rounded_cal(equation)} \\)")
    
    if (len(ordered_factors) == 1 and not ordered_factors[0].is_number) or (len(ordered_factors) == 2 and ordered_factors[0].is_number):
        if all_degrees == [4, 2, 0] or all_degrees == [4, 2]:
            list = []
            equation_u = expression.subs(x**4, u**2).subs(x**2, u)
            step.append("Rewrite the equation \\(u = x^{2}\\) and \\(u^{2} = x^{4}\\)")
            solution_step = solve(equation_u)
            step.append(f"Solve \\({latex(equation_u)} = 0\\) ")
            step.append(f"We have: \\(u = {latex(solution_step)}\\)")
            step.append(re_calc(solution_step))
            for j in solution_step:
                j = latex(j)
                j = j.replace(" i", "I")
                sol = latex2latex(f"x^2 = {j}")
                list.append(sol)
            solution = str(list).replace("'[", "").replace("]'", "").replace("\\\\", "\\")
        elif len(all_degrees) !=0 and all_degrees[0] == 2:
            step.append(quadric_cal(equation))
        else:
            solution = rounded_cal(equation)
    elif len(ordered_factors) > 1:
        step.append(f"Transforming the equation, we have, \\({latex(factor(expression))} = 0\\)")
        for ftr in ordered_factors:
            if not ftr.is_number:
                solution_step = solve(ftr)
                step.append(f"We have \\({latex(ftr)} = 0\\), so x = \\({latex(solution_step)}\\)")
                len_x += len(solution_step)
        step.append(f'Therefore, \\({data}\\) has {len_x} values \\({latex(solve(expression))}\\)')
    else:
        step.append(factor(expression))

    return solution
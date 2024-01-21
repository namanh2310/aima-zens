from flask import request, jsonify
import numpy as np
from sympy import *

class DiffnIntController:
    def trapezoidal():
        if request.method == "POST":
            data = request.json['input']
            function = data["function"]
            a = float(data["a"])
            b = float(data["b"])
            h = b-a
            x = Symbol('x')
            
            try:
                functionReplace = ''
                for i in range(len(function)):
                    if (function[i] == 'x' or function[i] == 'y') and i > 0 and function[i - 1].isdigit():
                        functionReplace += '*' + function[i]
                    else:
                        functionReplace += function[i]

                functionReplace = functionReplace.replace(' ', '').replace('^', '**')

                def functionInput(x, y):
                    return eval(functionReplace)

                def calFunctionInput(x_input, y_input):
                    return functionInput(x_input, y_input)
                
                def f_first_deri(f):
                    return diff(f, x)
                
                def f_second_deri(f_first_deri):
                    return diff(f_first_deri, x)
                
                def showEquation(f):
                    return str(f).replace('**','^').replace('*', '')
                obj = []

                def trapezoidalCal(a, b, h, function, x):
                    slopeA = calFunctionInput(a,0)
                    slopeB = calFunctionInput(b,0)
                    I = h*(slopeA + slopeB)/2
                    f_1_der = diff(function, x)
                    f_2_der = diff(f_1_der, x)
                    f_2_der_mean = integrate(f_2_der, (x, a, b)) / (b - a)
                    error = (-1/12) * f_2_der_mean * (b-a)**3
                    obj.append({
                        "I": '{:.4f}'.format(I),
                        "error": '{:.4f}'.format(error),
                    })
                    return jsonify({
                        'data': obj,
                        'h': h,
                        'slopeA': round(slopeA, 3),
                        'slopeB': round(slopeB, 3),
                        'first_deri': showEquation(f_1_der),
                        'second_deri': showEquation(f_2_der),
                        'f_2_der_mean': round(float(f_2_der_mean), 3)
                })
                return trapezoidalCal(a, b, h, functionReplace, x)
            except:
                return jsonify({'message': 'Please re-check the input fields'})
        
    def trapezoidalMA():
        if request.method == "POST":
            data = request.json['input']
            function = data["function"]
            a = float(data["a"])
            b = float(data["b"])
            n = int(data["n"])
            h = b-a
            x = Symbol('x')
            
            try:
                functionReplace = ''
                for i in range(len(function)):
                    if (function[i] == 'x' or function[i] == 'y') and i > 0 and function[i - 1].isdigit():
                        functionReplace += '*' + function[i]
                    else:
                        functionReplace += function[i]

                functionReplace = functionReplace.replace(' ', '').replace('^', '**')

                def functionInput(x, y):
                    return eval(functionReplace)

                def calFunctionInput(x_input, y_input):
                    return functionInput(x_input, y_input)
                
                def f_first_deri(f):
                    return diff(f, x)
                
                def f_second_deri(f_first_deri):
                    return diff(f_first_deri, x)
                
                def showEquation(f):
                    return str(f).replace('**','^').replace('*', '')
                obj = []

                def trapezoidalMACal(a, b, h, function, x, n):
                    array = np.linspace(a, b, n+1)
                    middle_sum = 0
                    slope_sum = 0
                    for i in range(len(array)):
                        if i == 0 or i == len(array)-1:
                            slope_sum += calFunctionInput(array[i],0)
                        else:
                            middle_sum += calFunctionInput(array[i],0)
                    
                    I = h*(slope_sum + 2*middle_sum)/(2*n)
                    f_1_der = diff(function, x)
                    f_2_der = diff(f_1_der, x)
                    f_2_der_mean = integrate((len(array)-2)*f_2_der, (x, a, b)) / (b - a)
                    error = -f_2_der_mean* (b-a)**3/(12*n**2)

                    obj.append({
                        "I": '{:.4f}'.format(I),
                        "error": '{:.4f}'.format(error),
                    })
                    return jsonify({
                        'data': obj,
                        'h': h,
                        'middle_sum': round(middle_sum, 3),
                        'slope_sum': round(slope_sum, 3),
                        'first_deri': showEquation(f_1_der),
                        'second_deri': showEquation(f_2_der),
                        'f_2_der_mean': round(float(f_2_der_mean), 3),
                        'array': str(array).replace(' ', ',')
                })
                return trapezoidalMACal(a, b, h, functionReplace, x, n)
            except:
                return jsonify({'message': 'Please re-check the input fields'})
        
    def simpson13Rule():
        if request.method == "POST":
            data = request.json['input']
            function = data["function"]
            a = float(data["a"])
            b = float(data["b"])
            
            n = (b-a)/2
            try:
                x = Symbol('x')
                
                functionReplace = ''
                for i in range(len(function)):
                    if (function[i] == 'x' or function[i] == 'y') and i > 0 and function[i - 1].isdigit():
                        functionReplace += '*' + function[i]
                    else:
                        functionReplace += function[i]

                functionReplace = functionReplace.replace(' ', '').replace('^', '**')

                intFunction = integrate(functionReplace, x)

                def functionInput(x, y):
                    return eval(functionReplace)
                
                def round_expr(expr, num_digits):
                    return expr.xreplace({n : round(n, num_digits) for n in expr.atoms(Number)})
                
                def calFunctionInput(x_input, y_input):
                    return functionInput(x_input, y_input)
                
                def integrated_function(f, a, b):
                    return integrate(f, (x, a, b))
                
                
                obj = []

                def simpson13(a, b ,n):
                    I = (n/3)*(calFunctionInput(a, 0)+ 4*calFunctionInput(n, 0)+ calFunctionInput(b, 0))
                    true_value = integrated_function(functionReplace, a, b) 
                    error = ((true_value - I)/true_value)*100
                    obj.append({
                        "I": '{:.4f}'.format(I),
                        "true_value": '{:.4f}'.format(true_value),
                        "error": '{:.4f}'.format(error),
                    })
                    return jsonify({
                            "data": obj,
                            "intFunct": str(round_expr(intFunction, 2)).replace('**','^').replace('*',''),
                            "n": n
                        })
                return simpson13(a, b, n)
            except ValueError:
                return jsonify({'message': 'Please re-check the input fields'})
            
    def simpson13MARule():
        if request.method == "POST":
            data = request.json['input']
            function = data["function"]
            a = float(data["a"])
            b = float(data["b"])
            n = int(data["n"])
            try:
                x = Symbol('x')
                
                functionReplace = ''
                for i in range(len(function)):
                    if (function[i] == 'x' or function[i] == 'y') and i > 0 and function[i - 1].isdigit():
                        functionReplace += '*' + function[i]
                    else:
                        functionReplace += function[i]

                functionReplace = functionReplace.replace(' ', '').replace('^', '**')

                intFunction = integrate(functionReplace, x)

                def functionInput(x, y):
                    return eval(functionReplace)
                
                def round_expr(expr, num_digits):
                    return expr.xreplace({n : round(n, num_digits) for n in expr.atoms(Number)})
                
                def calFunctionInput(x_input, y_input):
                    return functionInput(x_input, y_input)
                
                def integrated_function(f, a, b):
                    return integrate(f, (x, a, b))
                
                obj = []

                def simpson13ma(a, b ,n):
                    denominator = 0
                    array = np.linspace(a, b, n+1)
                    numpy_array = np.array(array)
                    rounded_list = np.round(numpy_array, 4).tolist()
                    # slope = calFunctionInput(a,0)
                    true_value = integrated_function(functionReplace, a, b)
                    for i in range(len(array)):
                        if i == 0 or i == len(array)-1:
                            denominator += calFunctionInput(array[i],0)
                        elif i%2 == 0:
                            denominator += 2*calFunctionInput(array[i],0)
                        else:
                            denominator += 4*calFunctionInput(array[i],0)
                    I = (b-a)*(denominator/(3*n))
                    error = ((true_value - I)/true_value)*100
                    obj.append({
                        "I": '{:.4f}'.format(I),
                        "true_value": '{:.4f}'.format(true_value),
                        "error": '{:.4f}'.format(error),
                    })
                    return jsonify({
                            "data": obj,
                            "input_funct": function.replace("**", "^").replace('*', ''),
                            "intFunct": str(round_expr(intFunction, 2)).replace('**','^').replace('*',''),
                            "n": n,
                            'array': rounded_list,
                            'denominator': round(denominator, 4)
                        })
                return simpson13ma(a, b, n)
            except ValueError:
                return jsonify({'message': 'Please re-check the input fields'})
            
    def simpson38Rule():
        if request.method == "POST":
            data = request.json['input']
            function = data["function"]
            a = float(data["a"])
            b = float(data["b"])
            n = int(data["n"])
            h = (b-a)/3
            try:
                x = Symbol('x')
                
                functionReplace = ''
                for i in range(len(function)):
                    if (function[i] == 'x' or function[i] == 'y') and i > 0 and function[i - 1].isdigit():
                        functionReplace += '*' + function[i]
                    else:
                        functionReplace += function[i]

                functionReplace = functionReplace.replace(' ', '').replace('^', '**')
                
                intFunction = integrate(functionReplace, x)

                def functionInput(x, y):
                    return eval(functionReplace)
                
                def round_expr(expr, num_digits):
                    return expr.xreplace({n : round(n, num_digits) for n in expr.atoms(Number)})
                
                def calFunctionInput(x_input, y_input):
                    return functionInput(x_input, y_input)
                
                def integrated_function(f, a, b):
                    return integrate(f, (x, a, b))
                
                obj = []

                def simpson38(a, b , n, h):
                    points_value = 0
                    array = np.linspace(a, b, n)
                    numpy_array = np.array(array)
                    rounded_list = np.round(numpy_array, 4).tolist()
                    slope = calFunctionInput(a,0)
                    true_value = integrated_function(functionReplace, a, b)
                    for i in range(len(array)):
                        if i == 0 or i == len(array)-1:
                            points_value += calFunctionInput(array[i],0)
                        else:
                            points_value += 3*calFunctionInput(array[i],0)   
                    I = (3*h/8)*(points_value)
                    error = ((true_value - I)/true_value)*100
                    obj.append({
                        "I": '{:.4f}'.format(I),
                        "true_value": '{:.4f}'.format(true_value),
                        "error": '{:.4f}'.format(error),
                    })
                    return jsonify({
                            "data": obj,
                            "intFunct": str(round_expr(intFunction, 2)).replace('**','^').replace('*',''),
                            "n": n,
                            'array': rounded_list,
                            'a': a,
                            'b': b,
                            'points_value': points_value
                    })
                return simpson38(a, b, n, h)
            except ValueError:
                return jsonify({'message': 'Please re-check the input fields'})
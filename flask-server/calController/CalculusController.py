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
from calController.utils.CalModule import sketchGraph
from calController.steps.Integral import handleIntegral
from calController.steps.Equation import handleEquation

class CalculusController: 
    def fundamental():
        if request.method == "POST":
            try:
                step = []
                data = request.json['data']
                print("adadadadada", data)
                raw_data = repr(data.replace("dx", ""))
                print(raw_data)
                try: 
                    expr = sympify(raw_data)
                    sympy_converter = latex2sympy(expr)
                    solution = latex2latex(expr)
                except ValueError:
                    return jsonify({'message': "error"})
                x = Symbol('x')

                if '=' not in expr:
                    handleIntegral(sympy_converter, step, x)
                                                
                elif '=' in expr:
                    # overwrite solution due to rounded results
                    solution = handleEquation(step, expr, data, solution)
                try:
                    return jsonify({'result': solution,'equation': data , 'step': step, 'img': sketchGraph(data, solution)})
                except Exception as e:
                    print(e)
                    return jsonify({'result': solution,'equation': data , 'step': step})

            except ValueError:
                return jsonify({'message': "error"})
    
    
    def LinearAlgebra():
        if request.method == "POST":
            step = []
            data = request.json['input']
            category = data['category']

            def string_to_matrix(input_string_raw):
                input_string_raw = input_string_raw.replace('"','').replace('\\n','\n')
                input_string = re.sub(r'(\d+)\s+\n', r'\1\n', input_string_raw)
                input_string = input_string.rstrip()
                print(input_string)
                rows = input_string.split('\n')
                matrix = []
                for row in rows:
                    elements = row.split(' ')
                    matrix.append([int(element) for element in elements])

                return np.array(matrix)
            
            matrixA = string_to_matrix(data['x'])
            matrixB = string_to_matrix(data['y'])
            if category == '1': # A + B
                rows, cols = matrixA.shape
                result = np.zeros((rows, cols), dtype=int)
                category = 'sum'
                for i in range(rows):
                    for j in range(cols):
                        result[i, j] = matrixA[i, j] + matrixB[i, j]
                        txt = f"{matrixA[i, j]} + {matrixB[i, j]} = {result[i, j]}"
                        step.append(txt)
            
            if category == '2': # A - B
                rows, cols = matrixA.shape
                category = 'difference'
                result = np.zeros((rows, cols), dtype=int)

                for i in range(rows):
                    for j in range(cols):
                        result[i, j] = matrixA[i, j] - matrixB[i, j]
                        txt = f"{matrixA[i, j]} - {matrixB[i, j]} = {result[i, j]}"
                        step.append(txt)
            
            if category == '3': # A x B
                rows, cols = matrixA.shape
                category = 'product'
                result = np.zeros((rows, cols), dtype=int)

                for i in range(rows):
                    for j in range(cols):
                        result[i, j] = matrixA[i, j] * matrixB[i, j]
                        txt = f"{matrixA[i, j]} x {matrixB[i, j]} = {result[i, j]}"
                        step.append(txt)

            if category =='4': # A dot B
                rows1, cols1 = matrixA.shape
                rows2, cols2 = matrixB.shape
                category = 'dot product'
                if cols1 != rows2:
                    raise ValueError("Matrix dimensions are not compatible for dot product.")
                dot_product_step_by_step = np.zeros((rows1, cols2), dtype=int)
                result = np.dot(matrixA, matrixB)
                for i in range(rows1):
                    for j in range(cols2):
                        for k in range(cols1):
                            product = matrixA[i, k] * matrixB[k, j]
                            step.append(f"{matrixA[i, k]} x {matrixB[k, j]} = {product}")
                            dot_product_step_by_step[i, j] += product
                        step.append(f"Partial Sum for element at ({i}, {j}) = {dot_product_step_by_step[i, j]}")
            
            if category =='5': # A dot B
                category = 'convolution'
                matrix_size = data['size']
                matrix_size = matrix_size.replace('"','')
                convRows, convColumns = map(int, matrix_size.split("x"))
                kernel_rows, kernel_cols = matrixB.shape
                result = np.zeros((convRows, convColumns), dtype=int)
                step.append('Calculate with 2 first steps:')
                for i in range(convRows):
                    for j in range(convColumns):
                        patch = matrixA[i:i + kernel_rows, j:j + kernel_cols]
                        convolution_result = patch * matrixB
                        convolution_sum = np.sum(convolution_result)
                        result[i, j] = convolution_sum
                        if j < 2 and i < 1:
                            step.append(patch.tolist())
                            step.append(convolution_result.tolist())
                            step.append(f"We make a sum for whole of this matrix = {convolution_sum}")
                
                step.append('Do continuously with the rest of matrix, and then we have the final result!')

            return jsonify({'matrixA': matrixA.tolist()
                            ,'matrixB': matrixB.tolist()
                            ,'category': category
                            ,'result': result.tolist()
                            , 'step': step})
       
        
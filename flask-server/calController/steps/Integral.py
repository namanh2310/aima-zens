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


pattern_exception = r'\([^,]+,\s*[^,]+,\s*[^)]+\)'
pattern = r"\b\w+\(([^,]+)"

def handleIntegral(sympy_converter, step, x):
    for arg in sympy_converter.args:
        if len(sympy_converter.args) == 2:
            match = re.match(pattern_exception, str(sympy_converter.args[1]))  
            if match:
                try:
                    result = integrate(arg, x)
                    conclu = sympify(sympy_converter).doit()
                    step.append([latex(arg),
                        latex(result),
                        latex(conclu)])
                    break
                except:
                    break
            else:
                if 'Integral' in str(arg):
                    matches = re.findall(pattern, str(arg))
                    for match in matches:
                        result = integrate(match, x)
                        conclu = sympify(arg).doit()
                        step.append([latex(match),
                        latex(str(result)),
                        latex(str(conclu))])
        else:
            if 'Integral' in str(arg):
                matches = re.findall(pattern, str(arg))
                for match in matches:
                    result = integrate(match, x)
                    conclu = sympify(arg).doit()
                    step.append([latex(match),
                        latex(str(result)),
                        latex(str(conclu))])
                    

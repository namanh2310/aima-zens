from flask import request, jsonify
import numpy as np
from sympy import *
import gdown

from latex2sympy2 import latex2sympy, latex2latex
from pix2text import Pix2Text, merge_line_texts
from pix2tex import cli as pix2tex

from io import BytesIO
import os
from PIL import Image
import PIL
import base64
import re
import requests
from munch import Munch
from torchvision import transforms
import cv2

script_dir = os.path.dirname(os.path.abspath(__file__))
server_dir = os.path.dirname(os.path.dirname(script_dir))
model_dir = os.path.join(server_dir, 'flask-server' ,'model', 'model.pth')
print(123123)
print(f"{model_dir}")

class AIController:
    def AIforWeb():
        if request.method == "POST":
            format = request.json['format']
            # if int(PIL.__version__[0]) < 9:
            #     print('Mandatory restart: Execute this cell again!')
            #     os.kill(os.getpid(), 9)
            image_base64 = bytes(format, 'utf-8')
            # image_base64 = base64.b64encode(image_data)
            image_bytes = BytesIO(base64.b64decode(image_base64))
            def get_dimension(img):
                to_tensor = transforms.ToTensor()
                tensor_image = to_tensor(img).size()
                return tensor_image
            print(image_bytes)
            # weight_path = 'C:/Users/user/Documents/Thesis/Thesis/flask-server/mixed_e25_step16296.pth'
            weight_path = r'C:\Users\user\Documents\Thesis\Thesis\flask-server\mixed_e25_step16296.pth'
            print(weight_path)
            arguments = Munch({'config': 'settings/config.yaml', 'checkpoint': weight_path, 'no_cuda': True, 'no_resize': True})
            img = Image.open(image_bytes)
            model = pix2tex.LatexOCR(arguments)
            raw_dimension = get_dimension(img)
            print("Raw dimension", raw_dimension)
            ratio = raw_dimension[2]/raw_dimension[1]
            expected_height = 95
            expected_width = 600
            if raw_dimension[1] >= 160:
                new_size = (round(expected_height*ratio), expected_height)
            elif raw_dimension[2] >= 1000:
                new_size = (expected_width, round(expected_width/ratio))
            else:
                new_size = (raw_dimension[2], raw_dimension[1])
            img = img.resize(new_size)
            new_dimension = get_dimension(img)
            print("Image's dimension", new_dimension)
            math = model(img)
            # math = model(img)
            raw_data = repr(math)
            expr = sympify(raw_data)
            print(raw_data)
            temp_symbol = '###'
            step = []
            sympy_converter = latex2sympy(expr)
            pattern = r"\b\w+\(([^,]+)"
            pattern_exception = r'\([^,]+,\s*[^,]+,\s*[^)]+\)'
            x = Symbol('x')
            if '=' not in expr:
                for arg in sympy_converter.args:
                        if len(sympy_converter.args) == 2:
                            match = re.match(pattern_exception, str(sympy_converter.args[1]))  
                            if match:
                                try:
                                    result = integrate(arg, x)
                                    conclu = sympify(sympy_converter).doit()
                                    step.append([str(arg).replace('**', temp_symbol).replace('*x', 'x').replace(temp_symbol, '^'), 
                                            str(result).replace('**', temp_symbol).replace('*', '').replace(temp_symbol, '^'),
                                            str(conclu).replace('**', temp_symbol).replace('*', '').replace(temp_symbol, '^')
                                            ])
                                    print(step[0])
                                    break
                                except:
                                    break
                            else:
                                if 'Integral' in str(arg):
                                    matches = re.findall(pattern, str(arg))
                                    for match in matches:
                                        result = integrate(match, x)
                                        conclu = sympify(arg).doit()
                                        step.append([match.replace('**', temp_symbol).replace('*x', 'x').replace(temp_symbol, '^'), 
                                            str(result).replace('**', temp_symbol).replace('*', '').replace(temp_symbol, '^'),
                                            str(conclu).replace('**', temp_symbol).replace('*', '').replace(temp_symbol, '^')
                                            ])
                        else:
                            if 'Integral' in str(arg):
                                matches = re.findall(pattern, str(arg))
                                for match in matches:
                                    result = integrate(match, x)
                                    conclu = sympify(arg).doit()
                                    step.append([match.replace('**', temp_symbol).replace('*x', 'x').replace(temp_symbol, '^'), 
                                            str(result).replace('**', temp_symbol).replace('*', '').replace(temp_symbol, '^'),
                                            str(conclu).replace('**', temp_symbol).replace('*', '').replace(temp_symbol, '^')
                                            ])
               
           
            
        
        # return jsonify({'result': latex2latex(expr), 'eq': str(math)})
        return jsonify({'eq': str(math), 'res': latex2latex(expr), 'step': step})

    def AIforApp():
        if request.method == "POST":
            try:
                # if not os.path.exists(model_dir):
                #     url = "https://drive.google.com/file/d/1sjb2oUc00oIrh3FCIDYipvEEb_z-9Y2b/view?usp=drive_link"
                #     gdown.download(url, model_dir, quiet=False,fuzzy=True)
                
                print(159357)
                if 'regenerate_status' in request.json:
                    regenerate_status = request.json['regenerate_status']
                else:
                    regenerate_status = None  
                img = request.json['img']
                print("2q2312132", img)
                response = requests.get(img)
                image_data = response.content
                
                image_base64 = base64.b64encode(image_data)
                print('hello')
                # print(image_base64)
                
                image_bytes = BytesIO(base64.b64decode(image_base64))
                img = Image.open(image_bytes)
                # weight_path = 'C:/Users/user/Documents/Thesis/Thesis/flask-server/mixed_e25_step16296.pth'
                weight_path = model_dir
                arguments = Munch({'config': 'settings/config.yaml', 'checkpoint': weight_path, 'no_cuda': True, 'no_resize': True})
                # img = Image.open(image_bytes)
                

                image_bytes_pre = base64.b64decode(image_base64)
                imagee = cv2.imdecode(np.frombuffer(image_bytes_pre, np.uint8), cv2.IMREAD_GRAYSCALE)
                white_pixels = np.sum(imagee == 255)
                black_pixels = np.sum(imagee == 0)
                white_black_ratio = white_pixels / (black_pixels + 1e-5)
                if white_black_ratio > 15:
                    print("Ảnh có nền trắng chữ đen.")
                    preprocess_img = img
                    print(type(preprocess_img))

                else:
                    print("Ảnh có nền bị nhiễu.")
                    _, thresholded_image = cv2.threshold(imagee, 128, 255, cv2.THRESH_BINARY)
                    _, img_encoded = cv2.imencode('.png', thresholded_image)
                    image_base64_pre = base64.b64encode(img_encoded).decode('utf-8')
                    image_bytes_pre = BytesIO(base64.b64decode(image_base64_pre))
                    preprocess_img = Image.open(image_bytes_pre)
                    print("preprocess_imgpreprocess_imgpreprocess_imgpreprocess_imgpreprocess_img", preprocess_img)

                def get_dimension(img):
                    to_tensor = transforms.ToTensor()
                    tensor_image = to_tensor(img).size()
                    return tensor_image
                
                raw_dimension = get_dimension(preprocess_img)
                print("1231231231231", raw_dimension)
                res_list = []

                def predict_img(expected_height, expected_width, height_threshold, width_threshold, image):
                    model = pix2tex.LatexOCR(arguments)
                    ratio = raw_dimension[2]/raw_dimension[1]
                    if raw_dimension[1] >= height_threshold and raw_dimension[2] < width_threshold:
                        new_size = (round(expected_height*ratio), expected_height)
                    elif raw_dimension[2] >= width_threshold:
                        new_size = (expected_width, round(expected_width/ratio))
                    else:
                        new_size = (raw_dimension[2], raw_dimension[1])
                    img = image.resize(new_size)  
                    new_dimension = get_dimension(img)
                    print("Image's dimension", new_dimension)
                    math = model(img)
                    equation = math.replace("\\dx", "")
                    return equation

                equation = predict_img(80, 600, 160, 1000, preprocess_img)
                if regenerate_status == None:
                    print("roixg")
                if regenerate_status != None:
                    print(12312312312313)
                    res_list.append(predict_img(80, 600, 160, 1000, preprocess_img))
                    res_list.append(predict_img(120, 600, 160, 1000, preprocess_img))
                    res_list.append(predict_img(raw_dimension[1], raw_dimension[2], 0, 0, preprocess_img))
                    try:
                        latex2latex(predict_img(raw_dimension[1], raw_dimension[2], 0, 0, img))
                        res_list.append(predict_img(raw_dimension[1], raw_dimension[2], 0, 0, img))
                    except:
                        pass

                res_list_set = set(res_list)
                opt_list = list(res_list_set)
                return jsonify({'eq': equation, 'complex': False, 'res_list': opt_list})
            except ValueError:
                print(ValueError)

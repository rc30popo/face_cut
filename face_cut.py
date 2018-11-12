#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Detect face in image and cut

import cv2, os
import numpy as np
from PIL import Image
import argparse

# Please put your opencv installed directory name to opencv_dir
opencv_dir = '/home/toy/anaconda3/envs/py36/share/OpenCV'

cascade_filter_path = 'haarcascades/haarcascade_frontalface_alt2.xml'

face_filter = os.path.join(opencv_dir,cascade_filter_path)

start_num = 1
out_fname_base = 'face_'
input_dir = None
output_dir = None
img_w = 200
img_h = 200


faceCascade = cv2.CascadeClassifier(face_filter)

def make_outfname():
    global start_num
    global out_fname_base

    outfname = '{fname}{num:05}.jpg'.format(fname=out_fname_base,num=start_num)
    start_num = start_num + 1
    return outfname

# Argument Parser
parser = argparse.ArgumentParser(prog='face_cut',description='Cutting out and gray scaled human faces from photographs.')
parser.add_argument('input_dir',help='Input Directory Path')
parser.add_argument('output_dir',help='Output Directory Path')
parser.add_argument('-s','--startindex',help='Output filename start index',type=int,required=False)
parser.add_argument('-b','--base',help='Output filename base',required=False)
parser.add_argument('--width',help='Output image width',type=int,required=False)
parser.add_argument('--height',help='Output image height',type=int,required=False)


args = parser.parse_args()

input_dir = args.input_dir
output_dir = args.output_dir
if args.startindex != None:
    start_num = args.startindex
if args.base != None:
    out_fname_base = args.base
if args.height != None:
    img_h = args.height
if args.width != None:
    img_w = args.width

# Check parameters
param_error = False
if os.path.isdir(input_dir) != True:
    print('Input dir : {} not found!'.format(input_dir))
    param_error = True
if os.path.isdir(output_dir) != True:
    print('Output dir: {} not found!'.format(output_dir))
    param_error = True

if param_error == True:
    exit(1)

for f in os.listdir(input_dir):
    image_path = os.path.join(input_dir,f)
    print('Processing '+image_path)
    image_pil = Image.open(image_path).convert('L')
    image = np.array(image_pil, 'uint8')
    image_h,image_w = image.shape

    faces = faceCascade.detectMultiScale(image)

    for (x,y,w,h) in faces:
        roi = cv2.resize(image[y: y + h, x: x + w], (img_w, img_h), interpolation=cv2.INTER_LINEAR)
        out_image_path = os.path.join(output_dir,make_outfname())
        print(' Writing '+out_image_path)
        cv2.imwrite(out_image_path,roi)


exit(0)


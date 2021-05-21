import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir
from os.path import join

img_path="D:\\competition\\水下机器人目标检测\\train\\image"
box_path="D:\\competition\\水下机器人目标检测\\train\\box" 
label_path="D:\\competition\\水下机器人目标检测\\train\\labels"
classes = ['holothurian', 'echinus', 'scallop', 'starfish']
imgs=os.listdir(img_path)
def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(imgname):  # 转换这一张图片的坐标表示方式（格式）,即读取xml文件的内容，计算后存放在txt文件中。
    out_file = open(os.path.join(label_path,imgname+".txt"), 'w')

    if not os.path.exists(os.path.join(box_path,imgname+".xml")):
        pass
    else:
        tree=ET.parse(os.path.join(box_path,imgname+".xml"))
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)

        for obj in root.iter('object'):
            
            cls = obj.find('name').text
            if cls in classes :
                
                cls_id = classes.index(cls)
                xmlbox = obj.find('bndbox')
                b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
                bb = convert((w,h), b)
                out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')



if not os.path.exists(label_path):
    os.makedirs(label_path)  # 新建一个 label 文件夹，用于存放yolo格式的标签文件：000001.txt

for _ in imgs:
    imgname=_.split('.')[0]

    convert_annotation(imgname)  # 转换这一张图片的坐标表示方式（格式）
    
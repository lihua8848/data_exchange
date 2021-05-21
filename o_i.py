import os
import cv2 as cv

mat_file="D:\\work\\nuclear segment\\dateset_train\\nucleus\\png\\tnbc\\Labels_png"
tar_file="D:\\work\\nuclear segment\\dateset_train\\nucleus\\png\\tnbc\\Labels_png_01"

def custom_image(filename,_):
    gray = cv.cvtColor(filename, cv.COLOR_BGR2GRAY)
    ret,thresh1= cv.threshold(gray,0,255,cv.THRESH_BINARY)
    if not os.path.exists(tar_file):
        os.mkdir(tar_file)
    cv.imwrite(os.path.join(tar_file,_),thresh1)


lists=os.listdir(mat_file)
for _ in lists:
    
    img = cv.imread(os.path.join(mat_file,_))
    custom_image(img,_)
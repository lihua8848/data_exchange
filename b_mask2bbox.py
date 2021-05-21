import numpy as np
from skimage import measure
import os
from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt
# rle masks.
b_mask_path = "D:\\work\\nuclear segment\\dateset_train\\nucleus\\train\\tnbc\\Labels_png_01"
masks = os.listdir(b_mask_path)

#基于cv2
#基于连通区域获取bbox&&area
def mask2bbox(binary_mask,filename):
    mask = Image.open(os.path.join(b_mask_path,filename))
    binary_mask = np.array(mask, np.uint8)
    contours,hierarchy = cv2.findContours(
        binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    areas = []
    bounding_boxs = []    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        areas.append(area)
    # 取最大面积的连通区域
    #idx = areas.index(np.max(areas))
        #计算cnt的bbox
        x, y, w, h = cv2.boundingRect(cnt)
        bounding_box = [x, y, x+w, y+h]
        bounding_boxs.append(bounding_box)
    return bounding_boxs

#获取的bbox显示在原图上 
def img_show(bounding_boxs,filename):
    image = cv2.imread(os.path.join(b_mask_path,filename))
    for i in bounding_boxs:
        cv2.rectangle(image, (i[0], i[1]), (i[2], i[3]), (0, 0, 255),2)
    cv2.imshow(str(_), image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("#################################")

def close_contour(contour):
    if not np.array_equal(contour[0], contour[-1]):
        contour = np.vstack((contour, contour[0]))
    return contour

#从二值图用Douglas-Peucker algorithm获取坐标
def binary_mask_to_polygon(binary_mask, tolerance=0):
    """Converts a binary mask to COCO polygon representation

    Args:
        binary_mask: a 2D binary numpy array where '1's represent the object
        tolerance: Maximum distance from original points of polygon to approximated
            polygonal chain. If tolerance is 0, the original coordinate array is returned.

    """
    polygons = []
    # pad mask to close contours of shapes which start and end at an edge
    padded_binary_mask = np.pad(binary_mask, pad_width=1, mode='constant', constant_values=0)
    contours = measure.find_contours(padded_binary_mask, 0.5)
    contours = np.subtract(contours, 1)
    #fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(9, 4))
    #plt.gray()
    #ax2.imshow(binary_mask)
    for contour in contours:
        contour = close_contour(contour)
        contour = measure.approximate_polygon(contour, tolerance)
        #ax2.plot(contour[:, 1], contour[:, 0], '-r', linewidth=2)
        #plt.show()
        if len(contour) < 3:
            continue
        contour = np.flip(contour, axis=1)
        segmentation = contour.ravel().tolist()
        # after padding and subtracting 1 we may get -0.5 points in our segmentation 
        segmentation = [0 if i < 0 else i for i in segmentation]
        polygons.append(segmentation)
    

    return polygons

#将坐标整理为x，y
def binary_mask_to_xy(binary_mask):
    polygons = binary_mask_to_polygon(binary_mask, tolerance=2)
    

    #each cell 
    x=[]
    y=[]
    for polygon in polygons:
        xs = []
        ys = []
        for tdx in range(0, len(polygon), 2):
            xs.append(polygon[tdx])
            ys.append(polygon[tdx + 1])
        x.append(xs)
        y.append(ys)
    
    return x, y



bounding_boxs = []
k=0
for _ in masks:
    box=[]
    print(str(_))
    mask = Image.open(os.path.join(b_mask_path,_))
    
    binary_mask = np.array(mask, np.uint8)
    boxes=mask2bbox(binary_mask,_)
    #img_show(boxes,_)
    #binary_mask_to_polygon(binary_mask,0)
    x, y = binary_mask_to_xy(binary_mask)
    if len(x) < 1 or len(y) < 1:
        continue
    # left, top, right, bottom
    
    for i,j in zip(x,y):
        box.append([int(min(i)), int(min(j)), int(max(i)), int(max(j))])
    bounding_boxs.append(box)
    img_show(bounding_boxs[k],_)
    k+=1
    

for _,j in zip(range(len(bounding_boxs)),masks):
    #cv2.destroyAllWindows()
    img_show(bounding_boxs[_],j)

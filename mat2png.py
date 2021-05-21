import os
import scipy.io as scio
from PIL import Image
import numpy as np

mat_file="D:\\work\\nuclear segment\\dateset_train\\nucleus\\cpm15\\Labels"
tar_file="D:\\work\\nuclear segment\\dateset_train\\nucleus\\cpm15\\Labels_png"

def mat2png(matname,tar_file):
    mat=scio.loadmat(os.path.join(mat_file,matname))
    pngdata=mat["inst_map"]
    data = pngdata*255
    new_im = Image.fromarray(data.astype(np.uint8))
    if not os.path.exists(tar_file):
        os.mkdir(tar_file)
    outfile=os.path.join(tar_file,matname.split(".")[0]+".png")
    new_im.save(outfile)

lists=os.listdir(mat_file)
for _ in lists:
    mat2png(_,tar_file)

 

import os
import scipy.io as scio
from PIL import Image
import numpy as np

mat_file="D:\\work\\nuclear segment\\dateset_train\\nucleus\\tnbc\\Labels"
tar_file="/home/omnisky/lxy_workspace/nucleus/pffnet/PFFNet/nucleus/tnbc/Labels_png"

def mat2png(matname,tar_file):
    mat=scio.loadmat(os.path.join(mat_file,matname))
    pngdata=mat["inst_map"]


lists=os.listdir(mat_file)
for _ in lists:
    mat2png(_,tar_file)
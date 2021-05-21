import os
from PIL import Image

raw_file="D:\\work\\nuclear segment\\dateset_train\\nucleus\\png\\kumar\\monuseg\\Images"
tar_file="D:\\work\\nuclear segment\\dateset_train\\nucleus\\png\\kumar\\monuseg\\Images_png"

def tif2png(filename,tar_file):
    im = Image.open(os.path.join(raw_file, filename))
    im.thumbnail(im.size)
    if not os.path.exists(tar_file):
        os.mkdir(tar_file)
    outfile=os.path.join(tar_file,filename.split(".")[0]+".png")
    im.save(outfile, quality=100)

lists=os.listdir(raw_file)
for _ in lists:
    tif2png(_,tar_file)
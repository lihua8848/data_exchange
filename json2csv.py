import json
import pandas as pd
import csv
import numpy as np
# 从json文件中读取数据
# 数据存储在一个字典列表中
load_path="D:\\competition\\under_rob\\result\\4\\result.json"
save_path="D:\\competition\\under_rob\\result\\4\\file.csv"
fields = ["name","image_id","confidence","xmin","ymin","xmax","ymax"]
x=np.empty(shape=[0,7],dtype=int)
with open(load_path) as f:
    data_listofdict = json.load(f)
for _ in data_listofdict:
    x=np.append(x,[[_["category"],_["name"].split(".")[0],float(_["score"]),int(_["bbox"][0]),int(_["bbox"][1]),int(_["bbox"][2]),int(_["bbox"][3])]],axis=0)

# 以列表中的字典写入倒csv文件中

df=pd.DataFrame(x)
df.columns=["name","image_id","confidence","xmin","ymin","xmax","ymax"]

df.to_csv(save_path,index=False)
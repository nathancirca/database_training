import os,shutil
from natsort import natsorted, ns

s = "/media/pc-visualisation/DATA/dataset_sqlite/VOCdevkit/VOC2012/JPEGImages"
d = "/media/pc-visualisation/DATA/dataset_sqlite/entrainement/images"
files = natsorted(os.listdir(d))

highest_index = 13225

for i,f in enumerate(natsorted(os.listdir(s)),highest_index):
    new_name = "{}.jpg".format(i)
    shutil.copy(os.path.join(s,f),os.path.join(d,new_name))
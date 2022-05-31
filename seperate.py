import os, os.path, shutil
import random

def verif(table):
	for i in range(len(table)):
		for j in range(i+1,len(table)):
			if table[i]==table[j]:
				return "error"
	return "ok"

def copy(test,valid):
	dir="/media/pc-visualisation/DATA/dataset_sqlite/entrainement"
	num=len(os.listdir(dir+"/images"))
	l = [i for i in range(1,num+1)]
	table_test=random.sample(l,int(test*num))
	s_im=dir+"/images"
	dt_im=dir+"/test/images"
	s_lab=dir+"/labels"
	dt_lab=dir+"/test/labels"
	for k in table_test:
		shutil.copy(os.path.join(s_im,str(k)+".jpg"),os.path.join(dt_im,str(k)+".jpg"))
	for j in table_test:
		shutil.copy(os.path.join(s_lab,str(j)+".txt"),os.path.join(dt_lab,str(j)+".txt"))
	for elem in table_test:
		l.remove(elem)
	table_valid=random.sample(l,int(valid*num))
	dv_im=dir+"/valid/images"
	dv_lab=dir+"/valid/labels"
	for m in table_valid:
		shutil.copy(os.path.join(s_im,str(m)+".jpg"),os.path.join(dv_im,str(m)+".jpg"))
	for n in table_valid:
		shutil.copy(os.path.join(s_lab,str(n)+".txt"),os.path.join(dv_lab,str(n)+".txt"))
	for elem in table_valid:
		l.remove(elem)
	dtr_im=dir+"/train/images"
	dtr_lab=dir+"/train/labels"
	for o in l:
		shutil.copy(os.path.join(s_im,str(o)+".jpg"),os.path.join(dtr_im,str(o)+".jpg"))
	for p in l:
		shutil.copy(os.path.join(s_lab,str(p)+".txt"),os.path.join(dtr_lab,str(p)+".txt"))
	print(verif(l+table_valid+table_test))



copy(0.15,0.15)

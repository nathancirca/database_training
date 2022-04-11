import sqlite3 as sql
import os
from sqlite3 import Error

#**********************************
def calcul(obj_id,i) :
    (obj_id[i],)=obj_id[i]
    cx1=cursor.execute("select x1 from Lignes where objet_id=:obj_id",{"obj_id":obj_id[i]}).fetchall()
    cy1=cursor.execute("select y1 from Lignes where objet_id=:obj_id",{"obj_id":obj_id[i]}).fetchall()
    cx2=cursor.execute("select x2 from Lignes where objet_id=:obj_id",{"obj_id":obj_id[i]}).fetchall()
    cy2=cursor.execute("select y2 from Lignes where objet_id=:obj_id",{"obj_id":obj_id[i]}).fetchall()
    L1=[]
    L2=[]
    L3=[]
    L4=[]
    L1.extend([cx1[0],cy1[0],cx2[0],cy2[0]])
    L2.extend([cx1[1],cy1[1],cx2[1],cy2[1]])
    L3.extend([cx1[2],cy1[2],cx2[2],cy2[2]])
    L4.extend([cx1[3],cy1[3],cx2[3],cy2[3]])
    (a,)=L1[0]
    (b,)=L1[2]
    (c,)=L2[1]
    (d,)=L2[3]
    cx=(a+b)/2
    cy=(c+d)/2
    h=(d-c)
    w=(b-a)
    return [cx,cy,w,h]

#*********************************
conn=sql.connect('baseImage.db')

 # To view table data in table format
print ("******Objets Table Data*******")
cur = conn.cursor()
print ("Exporting data into TXT............")
img_id0=cur.execute('''SELECT ID from Images''').fetchall()
print(img_id0)
img_id=cur.execute('''SELECT image_id from Objets''').fetchall()
print(img_id)
cursor = conn.cursor()
for k in range(len(img_id0)):
  #for j in range(len(img_id)):
    (img_id0[k],)=img_id0[k]
  
    obj_id=cur.execute("SELECT ID from Objets where image_id=:img_id",{"img_id":img_id0[k]})
    obj_id=obj_id.fetchall() #(x1+x2)/2
    print(obj_id)
    for i in range(len(obj_id)):
      L=[]
      L=calcul(obj_id,i)
      print(L)
     
      classe=cursor.execute("select classe from Objets where image_id=:img_id",{"img_id":img_id0[k]})
      (classe,)=classe.fetchone()
      fichier = "fichier{}.txt".format(k+1)
      with open(fichier, 'a') as txt_file:
        txt_file.write(str(classe)+' '+str(L[0])+' '+str(L[1])+' '+str(L[2])+' '+str(L[3]))
        txt_file.writelines('\n')

dirpath = os.getcwd() + "/data_txt.txt"
print("Data exported Successfully into {}".format(dirpath))

'''except Error as e:
  print(e)

# Close database connection
finally: '''
conn.close()



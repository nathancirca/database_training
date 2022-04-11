import sqlite3
import re
import yaml

def appartient(list1,elem):
    for i in range(len(list1)):
        if list1[i]==elem:
            return True
    return False

def addImageYolov5(chemin,annotation): ###annotation est une liste contenant la classe, le point central, la largeur et la hauteur
    
    con=sqlite3.connect('baseImage.db')
    cur=con.cursor()
    cur.execute("INSERT INTO Images VALUES (?,?)", (None,chemin)) #création de l'objet image
    imgID=cur.execute('SELECT ID FROM Images WHERE chemin=:chemin',{"chemin":chemin})
    imgID=imgID.fetchone()
    with open('/home/nathan/cours/projet2A/dataset_waffle/data.yaml', 'r') as f:
        names_set=yaml.load(f)['names']
    for i in range(len(annotation)//5):
        names_base=cur.execute('SELECT DISTINCT nom FROM Objets').fetchall()
        for j in range(len(names_base)):
            (names_base[j],)=names_base[j]
        names=names_set[annotation[i*5]]
        k=0
        while k<len(names_base) and not appartient(names_base[k].split(','),names):
            k+=1
        if k<len(names_base):
            (classe,)=cur.execute('SELECT classe FROM Objets WHERE nom=:names',{"names":names_base[k]}).fetchone()
            cur.execute('INSERT INTO Objets VALUES (?,?,?,?)',(None,imgID[0],classe,names_base[k]))
        else:
            print('le nom de la classe est '+names+', quels noms lui sont équivalents ? (exemple : pour la classe human, vous pouvez entrer humain, personne, person, people…)\nSi vous avez terminé, appuyez sur entrer pour passer sans rien écrire' )
            add_name=input()
            while add_name!='':
                names=names+','+add_name
                add_name=input()
            cur.execute('INSERT INTO Objets VALUES (?,?,?,?)',(None,imgID[0],annotation[i*5],names)) #création de l'objet objet
        objID=cur.execute('SELECT MAX(ID) FROM Objets').fetchone()
        cx,cy,w,h=annotation[(i*5)+1],annotation[(i*5)+2],annotation[(i*5)+3],annotation[(i*5)+4]
        x1=cx-w/2
        y1=cy-h/2 #point en haut à gauche
        x2=cx+w/2
        y2=cy-h/2 #point en haut à droite
        x3=cx+w/2
        y3=cy+h/2 #point en bas à droite
        x4=cx-w/2
        y4=cy+h/2 #point en bas à gauche
        cur.execute('INSERT INTO Lignes VALUES (?,?,?,?,?,?)',(None,objID[0],x1,y1,x2,y2))
        cur.execute('INSERT INTO Lignes VALUES (?,?,?,?,?,?)',(None,objID[0],x2,y2,x3,y3))
        cur.execute('INSERT INTO Lignes VALUES (?,?,?,?,?,?)',(None,objID[0],x3,y3,x4,y4))
        cur.execute('INSERT INTO Lignes VALUES (?,?,?,?,?,?)',(None,objID[0],x4,y4,x1,y1)) #création des 4 lignes entourant l'objet
    con.commit()

for j in range(1,1148):
    with open(r'/home/nathan/cours/projet2A/dataset_waffle/train/labels/'+str(j)+'.txt') as coordFile:
        lines=coordFile.read()
        annotation=re.split(' |\n',lines)
        for i in range(len(annotation)//5):
            annotation[i*5]=int(annotation[i*5])
            annotation[i*5+1]=float(annotation[i*5+1])
            annotation[i*5+2]=float(annotation[i*5+2])
            annotation[i*5+3]=float(annotation[i*5+3])
            annotation[i*5+4]=float(annotation[i*5+4])
    addImageYolov5('/home/nathan/cours/projet2A/dataset_waffle/train/images/'+str(j)+'.jpg',annotation)
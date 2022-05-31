from random import randrange
import sqlite3
import xml.etree.ElementTree as ET

def appartient(list1,elem):
    for i in range(len(list1)):
        if list1[i]==elem:
            return True
    return False


def get_classe_name(object,names_base,cursor):
    names=object[0].text
    k=0
    while k<len(names_base) and not appartient(names_base[k].split(','),names):
        k+=1
    if k<len(names_base):
        (classe,)=cursor.execute('SELECT classe FROM Objets WHERE nom=:names',{"names":names_base[k]}).fetchone()
        return (classe, names_base[k])
    else:
        print('le nom de la classe est '+names+', quels noms lui sont équivalents ? (exemple : pour la classe human, vous pouvez entrer humain, personne, person, people…)\nSi vous avez terminé, appuyez sur entrer pour passer sans rien écrire' )
        add_name=input()
        while add_name!='':
            names=names+','+add_name
            add_name=input()
        (classe,)=cursor.execute('SELECT MAX(classe) FROM Objets').fetchone()
        if not classe :
            classe=1
        else :
            classe+=1
        return (classe,names)

def get_coord(object,annotation):
    w=float(annotation[-2][2].text)
    h=float(annotation[-2][1].text)
    k=1
    while object[k].tag!="bndbox":
        k+=1
    x1=float(object[k][1].text)/w
    y1=float(object[k][3].text)/h
    x2=float(object[k][0].text)/w
    y2=y1
    x3=x2
    y3=float(object[k][2].text)/h
    x4=x1
    y4=y3
    return (x1,y1,x2,y2,x3,y3,x4,y4)

def main():
    con=sqlite3.connect('baseImages.db')
    cur=con.cursor()
    for j in range(1,2165): 
        chemin='/media/pc-visualisation/DATA/dataset_sqlite/VOCdevkit/VOC2012/JPEGImages/14992+'+str(j)+'.jpg'
        tree = ET.parse('/media/pc-visualisation/DATA/dataset_sqlite/VOCdevkit/VOC2012/Annotations/14992+'+str(j)+'.xml')
        annotation = tree.getroot()
        cur.execute("INSERT INTO Images VALUES (?,?)", (None,chemin))
        (imgID,)=cur.execute('SELECT ID FROM Images WHERE chemin=:chemin',{"chemin":chemin}).fetchone()
        for i in range(2,len(annotation)-3):
            object=annotation[i]
            names_base=cur.execute('SELECT DISTINCT nom FROM Objets').fetchall()
            for j in range(len(names_base)):
                (names_base[j],)=names_base[j]
            (classe,names)=get_classe_name(object,names_base,cur)
            cur.execute('INSERT INTO Objets VALUES (?,?,?,?)',(None,imgID,classe,names))
            (objID,)=cur.execute('SELECT MAX(ID) FROM Objets').fetchone()
            (x1,y1,x2,y2,x3,y3,x4,y4)=get_coord(object,annotation)
            cur.execute('INSERT INTO Lignes VALUES (?,?,?,?,?,?)',(None,objID,x1,y1,x2,y2))
            cur.execute('INSERT INTO Lignes VALUES (?,?,?,?,?,?)',(None,objID,x2,y2,x3,y3))
            cur.execute('INSERT INTO Lignes VALUES (?,?,?,?,?,?)',(None,objID,x3,y3,x4,y4))
            cur.execute('INSERT INTO Lignes VALUES (?,?,?,?,?,?)',(None,objID,x4,y4,x1,y1))
    con.commit()

main()
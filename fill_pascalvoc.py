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
        print(k)
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
    w=float(annotation[4][0].text)
    h=float(annotation[4][1].text)
    x1=float(object[4][0].text)/w
    y1=float(object[4][1].text)/h
    x2=x1
    y2=float(object[4][3].text)/h
    x3=float(object[4][2].text)/w
    y3=y1
    x4=x3
    y4=y2
    return (x1,y1,x2,y2,x3,y3,x4,y4)

def main():
    con=sqlite3.connect('baseImage.db')
    cur=con.cursor()
    for j in range(1,4341):
        chemin='/home/nathan/cours/projet2A/Annotations/'+str(j)+'.xml'
        tree = ET.parse(chemin)
        annotation = tree.getroot()
        cur.execute("INSERT INTO Images VALUES (?,?)", (None,chemin))
        (imgID,)=cur.execute('SELECT ID FROM Images WHERE chemin=:chemin',{"chemin":chemin}).fetchone()
        for i in range(6,len(annotation)):
            object=annotation[i]
            names_base=cur.execute('SELECT DISTINCT nom FROM Objets').fetchall()
            for j in range(len(names_base)):
                (names_base[j],)=names_base[j]
            (classe,names)=get_classe_name(object,names_base,cur)
            print(imgID,classe,names)
            cur.execute('INSERT INTO Objets VALUES (?,?,?,?)',(None,imgID,classe,names))
            (objID,)=cur.execute('SELECT MAX(ID) FROM Objets').fetchone()
            (x1,y1,x2,y2,x3,y3,x4,y4)=get_coord(object,annotation)
            cur.execute('INSERT INTO Lignes VALUES (?,?,?,?,?,?)',(None,objID,x1,y1,x2,y2))
            cur.execute('INSERT INTO Lignes VALUES (?,?,?,?,?,?)',(None,objID,x2,y2,x3,y3))
            cur.execute('INSERT INTO Lignes VALUES (?,?,?,?,?,?)',(None,objID,x3,y3,x4,y4))
            cur.execute('INSERT INTO Lignes VALUES (?,?,?,?,?,?)',(None,objID,x4,y4,x1,y1))
    con.commit()

main()
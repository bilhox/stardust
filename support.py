# -*- coding:Utf-8 -*-
#------------------------------------------------------------------------------
# Author:  M. SALVA
# Name:    main.py
# Purpose: Logiciel de traitement d'image au format PBM, PGM ou PPM
# Created: 12/12/2021
# Python:  3.10
# Modules: traitement, support
# Licence: Creative Commons BY NC SA
#-------------------------------------------------------------------------------

import os
from PIL import Image # Pour la lecture d'image .jpg
import tkinter as Tk
from tkinter import messagebox

#-------------------------------------------------------------------------------
def readPBM(file_path, img):
    """ Sous-fonction de la fonction ouvrir(). """
    with open(file_path, 'r') as f:
        texte = f.read().splitlines()
    img["meta"]["col"]= int(texte[1])
    img["meta"]["lig"]= int(texte[2])

    i = 0
    for line in texte[3:]:
        img["pix"].append([])
        for val in line.split():
            if val == "1":
                img["pix"][i].append((0, 0, 0))
            else:
                img["pix"][i].append((255, 255, 255))
        i += 1

    return img

def readPGM(fichier, img):
    """ Sous-fonction de la fonction ouvrir(). """
    with open(fichier, 'r') as f:
        texte = f.read().splitlines()

    img["meta"]["col"]= int(texte[1])
    img["meta"]["lig"]= int(texte[2])

    i = 0
    for line in texte[4:]:
        img["pix"].append([])
        for val in line.split():
            img["pix"][i].append((int(val), int(val), int(val)))
        i += 1

    return img

def readPPM(fichier, img):
    """ Sous-fonction utilisée dans la fonction ouvrir(). """
    with open(fichier, 'r') as f:
        texte = f.read().splitlines()

    img["meta"]["col"] = int(texte[1])
    img["meta"]["lig"] = int(texte[2])

    i = 0
    for line in texte[4:]:
        img["pix"].append([])
        line = line.split()
        for x in range(0 , len(line) , 3):
            tup_pix = (int(line[x]), int(line[x+1]), int(line[x+2]))
            img["pix"][i].append(tup_pix)
        i += 1

    return img

#-------------------------------------------------------------------------------
def ouvrir(fichier):
    """
    Ouvre le fichier et charge l'image au format dict-img.
    :param fichier: str (Chemin d’accès du fichier)
    :return img = {"meta" : {"titre":"titre",
                             "extension":".ppm",
                             "col" : 2,
                             "lig" : 3
                             "mod" : ""},
                   "pixel" : [(255, 255, 255), (253, 0, 34)], [(233, 0, 0), ...}
    """
    if fichier == "images/":
        return False
    else :
        filename, file_extension = os.path.splitext(fichier)
        img = {"meta" : {"titre": filename,
                         "extension": file_extension,
                         "col" : None,
                         "lig" : None,
                         "mod" : ""},
               "pix" : []}

        if file_extension == ".pbm":
            img = readPBM(fichier, img)
        elif file_extension == ".pgm":
            img =readPGM(fichier, img)
        elif file_extension == ".ppm":
            img = readPPM(fichier, img)
        else:
            messagebox.showinfo("Erreur", "Le fichier n'existe pas ou le format est incompatible.")

        return img

#-------------------------------------------------------------------------------
def afficher(img):
    """
    Affiche l'image dans une fenêtre Tkinter.
    :param img = {"meta" : {"titre":"titre",
                            "extension":".ppm",
                            "col" : 2,
                            "lig" : 3
                            "mod" : ""},
                  "pix" : [(255, 255, 255), (253, 0, 34), (233, 0, 0), ...}
    """
    if img:
        col = img["meta"]["col"]
        lig = img["meta"]["lig"]
        nom = img["meta"]["titre"] + img["meta"]["extension"]

        t = 400//max(lig,col)

        fen = Tk.Tk()
        fen.title(nom + " " + str(col) + "x" + str(lig))
        can = Tk.Canvas(fen, width = col*t + 18, height = lig*t + 18, bg = 'white')
        can.pack(side = Tk.TOP, padx = 5, pady = 5)

        for y in range(lig) :
            for x in range(col) :
                r, v, b = img["pix"][y][x]
                color = '#%02x%02x%02x' % (int(r),int(v),int(b))
                can.create_rectangle(10+x*t, 10+y*t, 10+(x+1)*t, 10+(y+1)*t, outline = color, fill = color)

        fen.mainloop()
    else:
        messagebox.showinfo("Erreur", "L'image ne peut pas être affichée.")

#-------------------------------------------------------------------------------
def comparer(img1, img2):
    """
    Affiche deux images côte à côte dans une fenêtre Tkinter.
    :param img = {"meta" : {"titre":"titre",
                            "extension":".ppm",
                            "col" : 2,
                            "lig" : 3
                            "mod" : ""},
                  "pix" : [(255, 255, 255), (253, 0, 34), (233, 0, 0), ...}
    """
    if img1 and img2:
        col1 = img1["meta"]["col"]
        lig1 = img1["meta"]["lig"]

        col2 = img2["meta"]["col"]
        lig2 = img2["meta"]["lig"]

        t = 400//max(lig1, col1)
        ligmax = max(lig1, lig2)

        fen = Tk.Tk()
        fen.title(img1["meta"]["titre"] + img1["meta"]["extension"] + " " + str(col1) + "x" + str(lig1) + " " + img2["meta"]["mod"])
        can = Tk.Canvas(fen, width = (col1 + col2)*t + 18 + 10, height = ligmax*t + 18, bg = 'white')
        can.pack(side = Tk.TOP, padx = 5, pady = 5)

        for y in range(lig1) :
            for x in range(col1) :
                r, v, b = img1["pix"][y][x]
                color = '#%02x%02x%02x' % (int(r),int(v),int(b))
                can.create_rectangle(10+x*t, 10+y*t, 10+(x+1)*t, 10+(y+1)*t, outline = color, fill = color)
        for y in range(lig2) :
            for x in range(col2) :
                r, v, b = img2["pix"][y][x]
                color = '#%02x%02x%02x' % (int(r),int(v),int(b))
                can.create_rectangle(10+(x+col1)*t+10, 10+y*t, 10+(x+col1+1)*t+10, 10+(y+1)*t, outline = color, fill = color)
        fen.mainloop()
    elif not img1:
        messagebox.showinfo("Erreur", "L'image originale ne peut pas être affichée.")
    elif not img2:
        messagebox.showinfo("Erreur", "L'image transformée ne peut pas être affichée.")


#-------------------------------------------------------------------------------
def sauver(img):
    """
    Enregistre l'image au format .pbm, .pgm ou .ppm.
    :param img = {"meta" : {"titre":"titre",
                            "extension":".ppm",
                            "col" : 2,
                            "lig" : 3
                            "mod" : ""},
                  "pix" : [(255, 255, 255), (253, 0, 34), (233, 0, 0), ...}
    """
    col = img["meta"]["col"]
    lig = img["meta"]["lig"]
    img_format = {".pbm":'P1', ".pgm":'P2', ".ppm":'P3'}[img["meta"]["extension"]]
    pix = img["pix"]
    nom = img["meta"]["titre"] + "_modifie" + img["meta"]["extension"]

    with open(nom, 'w') as f :
        f.write(img_format + '\n' + str(col) + '\n' + str(lig) + '\n')

        if img_format in ["P2", "P3"]:
            f.write('255\n')

        if img_format == "P1":
            for y in range(lig):
                for x in range(col):
                    val = pix[y][x][0]
                    if val == 0:
                        f.write(' 1')
                    else:
                        f.write(' 0')
                f.write('\n')

        if img_format == "P2":
            for y in range(lig):
                for x in range(col):
                    val = str(pix[y][x][0])
                    f.write(' '*(4-len(val))+val)
                f.write('\n')

        elif img_format == "P3":
            for y in range(lig):
                for x in range(col):
                    for i in range(3):
                        val = str(pix[y][x][i])
                        f.write(' '*(4-len(val))+val)
                f.write('\n')
        f.close()

#-------------------------------------------------------------------------------
if __name__ == '__main__':
    # Ne s'éxecute que s'il s'agit du fichier principal.
    # Le code ne s'exécute pas s'il est appelé comme module par un autre fichier.
##    img = ouvrir("images/salva.pbm")
    img = ouvrir("images/monty_python.jpg")
    afficher(img)


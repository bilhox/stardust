# -*- coding:Utf-8 -*-
#------------------------------------------------------------------------------
# Author:  M. SALVA
# Name:    main.py
# Purpose: Logiciel de traitement d'image au format PBM, PGM ou PPM
# Created: 25/11/2020
# Python:  3.4.5
# Modules: traitement, support
# Licence: Creative Commons BY NC SA
#-------------------------------------------------------------------------------

from support import *

def symHori(img):
    """
    Symétrie axe horizontale
    :param img : Dict : {"meta" : {"titre" : "titre", ...},
                         "pix" : [(255, 255, 255), (253, 0, 34), (233, 0, 0), ...]}
    :return: img
    """
    col = img["meta"]["col"]
    lig = img["meta"]["lig"]
    pix = img["pix"]

    newpix = []
    for y in range(lig-1, -1, -1):
        newpix.append(pix[y])

    img["pix"] = newpix
    img["meta"]["mod"]="Symétrie horizontale"
    print("Symétrie horizontale")
    return img

def symVert(img):
    # A compléter !!!!
    return img

def conversion_ppm_en_pgm(image_data):
    """
    image_data correspond à la DATA du fichier , c'est à dire le dictionnaire avec les pixels et la meta (voir le fichier world)
    Avec image_data['pix'] , on récupère le tableau de pixels sous la forme , par exemple :
    
    tab = [
        [3 , 5 , 6],
        [5 , 7 , 7]]
        
    Avant d'itérer dans le tableau , on va créer un tableau vide qui représente le futur tableau de pixels .
    Quand on va itérer dans le tableau , nous allons faire deux boucles 'for' , une qui itère dans toute les lignes du tableau (y) en créant
    de nouvelle ligne pour le tableau final, et une autre qui va itérer dans la ligne (x) , ce qui arrive au fait que dans les deux boucles ,
    pour récupérer le pixel , on fait image_data['pix'][y][x] , quand on va récupérer le pixel , on aura un tuple avec 3 valeurs (RGB) qui sont les valeurs des couleurs .
    Avec ces trois valeurs , on calcule la moyenne . Ce résultat sera append à la ligne du tableau final .
    Enfin , pour finaliser , il faut changer de tableau celui du dictionnaire par le tableau final , et renvoyer le dictionnaire mis à jour .
    
    """
    for y in range(image_data):
        for x in range(image_data):
            pass
    #faire une moyenne des 3 pixels et arrondir a un entier

#-------------------------------------------------------------------------------
if __name__ == '__main__':
    img = ouvrir("images/salva.ppm")
    img2 = symHori(img)
    sauver(img2)
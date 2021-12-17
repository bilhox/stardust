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

def symHori(image_data):
    """
    Symétrie axe horizontale
    :param img : Dict : {"meta" : {"titre" : "titre", ...},
                         "pix" : [(255, 255, 255), (253, 0, 34), (233, 0, 0), ...]}
    :return: img
    """
    col = image_data["meta"]["col"]
    lig = image_data["meta"]["lig"]
    pix = image_data["pix"]

    newpix = []
    for y in range(lig-1, -1, -1):
        newpix.append(pix[y])

    image_data["pix"] = newpix
    image_data["meta"]["mod"]="Symétrie horizontale"
    print("Symétrie horizontale")
    return image_data

def symVert(image_data):
    """
    Symétrie axe verticale
    :param img : Dict : {"meta" : {"titre" : "titre", ...},
                         "pix" : [(255, 255, 255), (253, 0, 34), (233, 0, 0), ...]}
    :return: img
    """
    col = image_data["meta"]["col"]
    lig = image_data["meta"]["lig"]
    pix = image_data["pix"]

    newpix = []

    for li in pix:
        li.reverse()
        newpix.append(li)
    
    image_data["pix"] = newpix
    image_data["meta"]["mod"]="Symétrie verticale"
    print("Symétrie verticale")
    return image_data


def rotation180(img):
    """
    Rotation 180 degrès
    :param img : Dict : {"meta" : {"titre" : "titre", ...},
                         "pix" : [(255, 255, 255), (253, 0, 34), (233, 0, 0), ...]}
    :return: img
    """
    col = img["meta"]["col"]
    lig = img["meta"]["lig"]
    pix = img["pix"]

    newpix = []

    img2 = symHori(img)
    img2 = symVert(img2)
    newpix.append(img2)


    img2["meta"]["mod"]="Rotation a 180 degrès"
    return img2





#-------------------------------------------------------------------------------
if __name__ == '__main__':
    img = ouvrir("images/salva.ppm")
    img2 = symHori(img)
    sauver(img2)

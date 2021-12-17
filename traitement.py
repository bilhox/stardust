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
    return image_data


def rotation180(image_data):
    """
    Rotation 180 degrès
    :param img : Dict : {"meta" : {"titre" : "titre", ...},
                         "pix" : [(255, 255, 255), (253, 0, 34), (233, 0, 0), ...]}
    :return: img
    """
    col = image_data["meta"]["col"]
    lig = image_data["meta"]["lig"]
    pix = image_data["pix"]

    newpix = []

    img2 = symHori(image_data)
    img2 = symVert(img2)
    newpix.append(img2)


    img2["meta"]["mod"]="Rotation a 180 degrès"
    return img2

def rotation90(image_data):
    """
    Rotation 90 degrès
    :param img : Dict : {"meta" : {"titre" : "titre", ...},
                         "pix" : [(255, 255, 255), (253, 0, 34), (233, 0, 0), ...]}
    :return: img
    """
  
    col = image_data["meta"]["col"]
    lig = image_data["meta"]["lig"]
    pix = image_data["pix"]

    newpix = []

    for x in range(col):
        ligne = []
        for y in range(lig-1 , -1 , -1):
            ligne.append(pix[y][x])
        newpix.append(ligne)

    final_img_data = image_data.copy()

    final_img_data["pix"] = newpix
    final_img_data["meta"]["mod"]="Rotation a 90 degrès"
    final_img_data["meta"]["col"] = lig
    final_img_data["meta"]["lig"] = col
    return final_img_data

def conversion_ppm_en_pgm(image_data : dict):
     
    tab = []
    for y in image_data["pix"]:
        ligne = []
        for rgb in y:
            moyenne_rgb = int((rgb[0]+rgb[1]+rgb[2])/3)
            new_rgb = (moyenne_rgb , moyenne_rgb , moyenne_rgb)
            ligne.append(new_rgb)
        
        tab.append(ligne)
    
    final_image_data = image_data.copy()
    final_image_data["pix"] = tab
    final_image_data["meta"]["extension"] = ".pgm"

    return final_image_data

def bitmap_conversion(image_data , black_level : int):
    tab = []
    for y in image_data["pix"]:
        ligne = []
        for rgb in y:
            somme_rgb = int((rgb[0]+rgb[1]+rgb[2]))
            if somme_rgb <= black_level :
                ligne.append((0 , 0 , 0))
            else:
                ligne.append((255 , 255 , 255))
        
        tab.append(ligne) 
    
    final_image_data = image_data.copy()
    final_image_data["pix"] = tab
    final_image_data["meta"]["extension"] = ".pbm"
    
    return final_image_data
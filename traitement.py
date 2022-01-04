from math import *
from decimal import *
from image import *

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

    final_image_data = image_data.copy()
    final_image_data["pix"] = newpix
    final_image_data["meta"]["mod"]="Symétrie horizontale"
    return final_image_data

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
        
    final_image_data = image_data.copy()
    
    final_image_data["pix"] = newpix
    final_image_data["meta"]["mod"]="Symétrie verticale"
    return final_image_data


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
    # newpix.append(img2)


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
    final_image_data["meta"]["mod"]="Conversion to pgm"

    return final_image_data

def bitmap_conversion(image_data , intensity : int):
         
    black_level = (intensity / 100) * (3*255)
    
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
    final_image_data["meta"]["mod"]="Conversion to pbm"
    
    return final_image_data

def luminosity(image_data , intensity : int):
    
    new_pixtab = []
    
    for y in image_data["pix"]:
        ligne = []
        for pixel in y:
            hsl = Image.rgb_to_hsl(pixel)
            hsl[2] = intensity
            new_rgb = Image.hsl_to_rgb(hsl)
            ligne.append(new_rgb)
        new_pixtab.append(ligne)
    
    final_image_data = image_data.copy()
    final_image_data["pix"] = new_pixtab
    
    final_image_data["meta"]["mod"]="Brightness modification"
    
    return final_image_data

def saturation(image_data , intensity : int):
    
    new_pixtab = []
    
    if intensity > 100:
        intensity = 100
    elif intensity < 0:
        intensity = 100
    
    for y in image_data["pix"]:
        ligne = []
        for pixel in y:
            hsl = Image.rgb_to_hsl(pixel)
            hsl[1] = intensity
            new_rgb = Image.hsl_to_rgb(hsl)
            ligne.append(new_rgb)
        new_pixtab.append(ligne)
    
    final_image_data = image_data.copy()
    final_image_data["pix"] = new_pixtab
    
    final_image_data["meta"]["mod"]="Saturation modification"
    
    return final_image_data

def rotation(image_data , degree):
    
    pixtab = []
    center = [image_data["meta"]["lig"] // 2 , image_data["meta"]["col"] // 2]
    
    size = [0,0]
    
    for y , ligne in enumerate(image_data["pix"]):
        
        for x , pixel in enumerate(ligne):
            
            new_coord = [int((center[0] - x) * cos(degree)) , int((center[1] - y) * sin(degree))]
            pixtab.append({"rgb":pixel , "coord":new_coord})
            
            if new_coord[1] > size[1]:
                size[1] = new_coord[1]
            elif new_coord[0] > size[0]:
                size[0] = new_coord[0]
    
    new_pix = [[0]*size[0]]*size[1]
    
    for pixel_data in pixtab:
        
        print(pixel_data["coord"][1],pixel_data["coord"][0])
        new_pix[pixel_data["coord"][1]][pixel_data["coord"][0]] = pixel_data["rgb"]
    
    final_image_data = image_data.copy()
    final_image_data["pix"] = new_pix
    final_image_data["meta"]["mod"]="Rotation"
    final_image_data["meta"]["col"] = size[0]
    final_image_data["meta"]["lig"] = size[1]
    
    return final_image_data

def resize_image(image_data , size : list):
    width = size[0]
    height = size[1]
    
    new_pix = [0]*height
    
    # Variable qui correspond au coef d'aggrandissement / rétrécissement => [coef_x , coef_y]
    coef = [width / image_data["meta"]["col"] , height / image_data["meta"]["lig"]]
    
    # itération dans chaque ligne du tableau
    for y , line in enumerate(image_data["pix"]):
        
        if coef[1] >= 1:
            #Si le coef est supérieur ou égal à 1 alors :
            # - Calcul des coordonées du début du pixel et de sa fin (On arrondi à l'entier le plus proche)
            # - Comme ça , si end_y - new_y est égal à 2 ou plus , on ajoute une deux fois le pixel , soit deux fois la ligne
            new_y = ceil(y*coef[1]) if (y*coef[1]) % 1 >= 0.5 else floor(y*coef[1])
            end_y = ceil((y+1)*coef[1]) if ((y+1)*coef[1]) % 1 >= 0.5 else floor((y+1)*coef[1])
            
            lenght_yPix = end_y - new_y
            
            for h in range(lenght_yPix):
                    
                ligne = [0]*width
                
                for x , pixel in enumerate(line):
                    
                    if coef[0] >= 1:
                        #Si le coef est supérieur ou égal à 1 alors :
                        # - Calcul des coordonées du début du pixel et de sa fin (On arrondi à l'entier le plus proche)
                        # - Comme ça , si end_x - new_x est égal à 2 ou plus , on ajoute une deux fois le pixel , soit deux fois la ligne
                        new_x = ceil(x*coef[0]) if (x*coef[0]) % 1 >= 0.5 else floor(x*coef[0])
                        end_x = ceil((x+1)*coef[0]) if ((x+1)*coef[0]) % 1 >= 0.5 else floor((x+1)*coef[0])
                        
                        lenght_xPix = end_x - new_x
                        
                        for i in range(lenght_xPix):
                            ligne[new_x+i] = pixel
                    
                    else:
                        # Si le coef est inférieur à 1 alors:
                        # - Calcul des coordonées du pixel
                        # - Si plusieurs pixels ont les mêmes coordonées , alors on fait leur moyenne
                        # Pour ce cas si , le tableau de pixel est déjà préremplis avec des 0
                        # Si la valeur n'est pas 0 , donc un pixel , alors on fait la moyenne avec le pixel en attente d'être ajouter
                        new_x = floor(x*coef[0])
                        
                        if ligne[new_x] != 0:
                            pix = ligne[new_x]
                            ligne[new_x] = [(pix[0]+pixel[0])//2,(pix[1]+pixel[1])//2,(pix[1]+pixel[1])//2]
                        else:
                            ligne[new_x] = pixel
            
                new_pix[new_y+h] = ligne
            
        else:
            # Si le coef est inférieur à 1 alors:
            # - Calcul des coordonées du pixel
            # - Si plusieurs pixels ont les mêmes coordonées , alors on fait leur moyenne
            # Pour ce cas si , le tableau de pixel est déjà préremplis avec des 0
            # Si la valeur n'est pas 0 , donc une ligne de pixel , alors on fait la moyenne en itérant dans la ligne
            new_y = floor(y*coef[1])
                   
            ligne = [0]*width
            
            for x , pixel in enumerate(line):
                
                if coef[0] >= 1:
                    new_x = ceil(x*coef[0]) if (x*coef[0]) % 1 >= 0.5 else floor(x*coef[0])
                    end_x = ceil((x+1)*coef[0]) if ((x+1)*coef[0]) % 1 >= 0.5 else floor((x+1)*coef[0])
                    
                    lenght_xPix = end_x - new_x
                    
                    for i in range(lenght_xPix):
                        ligne[new_x+i] = pixel
                
                else:
                    new_x = floor(x*coef[0])
                    end_x = ceil((x+1)*coef[0]) if ((x+1)*coef[0]) % 1 >= 0.5 else floor((x+1)*coef[0])
                    
                    if ligne[new_x] != 0:
                        pix = ligne[new_x]
                        ligne[new_x] = [(pix[0]+pixel[0])//2,(pix[1]+pixel[1])//2,(pix[1]+pixel[1])//2]
                    else:
                        ligne[new_x] = pixel
                
            if new_pix[new_y] != 0:
                for index , pix in enumerate(new_pix[new_y]):
                    new_pix[new_y][index] = [(pix[0]+ligne[index][0])//2,(pix[1]+ligne[index][1])//2,(pix[1]+ligne[index][1])//2]
            else:
                new_pix[new_y] = ligne       
        
    final_image_data = image_data.copy()
    final_image_data["meta"]["lig"] = height
    final_image_data["meta"]["col"] = width
    final_image_data["pix"] = new_pix
    
    return final_image_data            
            
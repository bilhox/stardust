from math import *


def red(image_data):
     
     new_pixtab = []
    
     for y in image_data["pix"]:
          ligne = []
          for pixel in y:
               new_rgb = (255 , pixel[1] , pixel[2])
               ligne.append(new_rgb)
          new_pixtab.append(ligne)
     
     final_image_data = image_data.copy()
     final_image_data["pix"] = new_pixtab
     
     final_image_data["meta"]["mod"]="Filter red"
     
     return final_image_data

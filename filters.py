from math import *
from traitement import *

def red(image_data):
     
     new_pixtab = []
    
     for y in image_data["pix"]:
          ligne = []
          for pixel in y:
               new_rgb = (255 , pixel[1] , pixel[2])
               ligne.append(new_rgb)
          new_pixtab.append(ligne)
     
     final_image_data = deepcopy(image_data)
     final_image_data["pix"] = new_pixtab
     
     final_image_data["meta"]["mod"]="Filter red"
     
     return final_image_data

def blue(image_data):
     
     new_pixtab = []

     for y in image_data["pix"]:
          ligne = []
          for pixel in y:
               new_rgb = (110, pixel[1], pixel[2])
               ligne.append(new_rgb)
          new_pixtab.append(ligne)

     final_image_data = deepcopy(image_data)
     final_image_data["pix"] = new_pixtab

     final_image_data["meta"]["mod"] = "Filter blue"
     return final_image_data
          

def pink(image_data):

     new_pixtab = []

     for y in image_data["pix"]:
          ligne = []
          for pixel in y:
              new_rgb = (pixel[1], 110, 125)
              ligne.append(new_rgb)
          new_pixtab.append(ligne)

     final_image_data = deepcopy(image_data)
     final_image_data["pix"] = new_pixtab

     final_image_data["meta"]["mod"] = "Filter pink"
     return final_image_data


def greenPurple(image_data):

     new_pixtab = []

     for y in image_data["pix"]:
          ligne = []
          for pixel in y:
              new_rgb = (110, pixel[1], 150)
              ligne.append(new_rgb)
          new_pixtab.append(ligne)

     final_image_data = deepcopy(image_data)
     final_image_data["pix"] = new_pixtab

     final_image_data["meta"]["mod"] = "Filter blue2"
     return final_image_data


def greenBrown(image_data):

     new_pixtab = []

     for y in image_data["pix"]:
          ligne = []
          for pixel in y:
              new_rgb = (90, pixel[1], 17)
              ligne.append(new_rgb)
          new_pixtab.append(ligne)

     final_image_data = deepcopy(image_data)
     final_image_data["pix"] = new_pixtab

     final_image_data["meta"]["mod"] = "Filter brown"
     return final_image_data

def contour(image_data):
     
     new_pixtab = []
     
     for y in range(1,image_data["meta"]["lig"]-1):
          line = []
          for x in range(1,image_data["meta"]["col"]-1):
               a = image_data["pix"][y-1][x-1]
               b = image_data["pix"][y+1][x+1]
               c = image_data["pix"][y+1][x-1]
               d = image_data["pix"][y-1][x+1]
               if image_data["meta"]["extension"] in [".pgm",".pbm"]:
                    a = a[0]
                    b = b[0]
                    c = c[0]
                    d = d[0]
               else:
                    
                    a = int((a[0]+a[1]+a[2])/3)
                    b = int((b[0]+b[1]+b[2])/3)
                    c = int((c[0]+c[1]+c[2])/3)
                    d = int((d[0]+d[1]+d[2])/3)
               
               diff = (a-b)**2+(c-d)**2
               if diff < 10000:
                    line.append([0,0,0])
               else:
                    line.append([255,255,255])
          new_pixtab.append(line)
     
     black_line = [[0,0,0]]*(image_data["meta"]["col"]-2)
     
     new_pixtab.insert(0 , black_line)
     new_pixtab.insert(image_data["meta"]["lig"]-1 , black_line)
     
     for line in new_pixtab:
          line.insert(0 , [0,0,0])
          line.insert(image_data["meta"]["col"]-1 , [0,0,0])
     
     final_image_data = deepcopy(image_data)
     final_image_data["pix"] = new_pixtab
     
     return final_image_data

import pygame
import os
import support

from math import *
from pygame.locals import *


class Image():
     
     def __init__(self, pos : tuple):
     
          self.name = ""
          self.path = ""
          self.pos = pos
          self.image_loaded = False
          self.image_data = {}
          
          self.image_data_backup = []
     
     def load(self , path):
          
          self.path = path
          filepath , file_extension = os.path.splitext(self.path)
          self.name = os.path.basename(self.path)
          self.image_data = {"meta" : {"titre": filepath,
                         "extension": file_extension,
                         "col" : None,
                         "lig" : None,
                         "mod" : "",
                         "readable" : True},
               "pix" : []}
          
          if file_extension == ".pgm":
               self.image_data = support.readPGM(self.path,self.image_data)
          elif file_extension == ".pbm":
               self.image_data = support.readPBM(self.path,self.image_data)
          elif file_extension == ".ppm":
               self.image_data = support.readPPM(self.path,self.image_data)
          else:
               self.texture = pygame.image.load(self.path)
               self.texture.convert_alpha()
               self.image_data["readable"] = False
               
               self.rect = self.texture.get_rect()
               self.rect.x , self.rect.y = self.pos[0] , self.pos[1]
               
               self.image_loaded = True
               
               return
          
          self.texture = pygame.Surface([self.image_data["meta"]["col"] , self.image_data["meta"]["lig"]])
          
          for y in range(self.image_data["meta"]["lig"]):
               
               for x in range(self.image_data["meta"]["col"]):
                    
                    self.texture.set_at([x , y] , self.image_data["pix"][y][x])
          
          self.rect = self.texture.get_rect()
          self.rect.x , self.rect.y = self.pos[0] , self.pos[1]
          
          self.image_loaded = True
     
     def load_by_data(self , image_data : dict , save=True):
          
          if save:
               self.image_data_backup.append(self.image_data.copy())
               if len(self.image_data_backup) == 5:
                    self.image_data_backup.pop(0)
          
          self.image_data = image_data.copy()
          
          self.texture = pygame.Surface([self.image_data["meta"]["col"] , self.image_data["meta"]["lig"]])
          
          for y in range(self.image_data["meta"]["lig"]):
               
               for x in range(self.image_data["meta"]["col"]):
                    self.texture.set_at([x , y] , self.image_data["pix"][y][x])
                         
          
          self.rect = self.texture.get_rect()
          self.rect.x , self.rect.y = self.pos[0] , self.pos[1]
          
          self.image_loaded = True
     
     def save(self):
          
          col = self.image_data["meta"]["col"]
          lig = self.image_data["meta"]["lig"]
          img_format = {".pbm":'P1', ".pgm":'P2', ".ppm":'P3'}[self.image_data["meta"]["extension"]]
          pix = self.image_data["pix"]
          nom = self.image_data["meta"]["titre"] + "_modifie" + self.image_data["meta"]["extension"]

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
     
     @staticmethod
     def rgb_to_hsl(rgb : list):
          
          r = rgb[0] / 255
          g = rgb[1] / 255
          b = rgb[2] / 255
          
          cMin = min([r , g , b])
          cMax = max([r , g , b])
          
          luminance = (cMax + cMin) / 2
          saturation = 0
          hue = 0
          
          if not cMax == cMin:
               if luminance <= 0.5:
                    saturation = (cMax - cMin) / (cMin + cMax)
               elif luminance > 0.5:
                    saturation = (cMax - cMin) / (2 - cMin - cMax)
               
               if cMax == r:
                    hue = (g - b)/(cMax - cMin)
               elif cMax == g:
                    hue = 2 + (b - r)/(cMax - cMin)
               elif cMax == b:
                    hue = 4 + (r - g)/(cMax - cMin)
               
               if hue < 0:
                    hue += 360
                    
               hue = hue * 60
          
          return [hue , saturation * 100 , luminance * 100]

     @staticmethod
     def hsl_to_rgb(hsl : list):
          
          hue = hsl[0]
          saturation = hsl[1] / 100
          luminance = hsl[2] / 100
          
          if saturation == 0:
               r , g , b = int(luminance * 255) , int(luminance * 255) , int(luminance * 255)
               return [r , g , b]
          
          t1 = 0
          
          if luminance < 0.5:
               t1 = luminance * (1 + saturation)
          else:
               t1 = luminance + saturation - (luminance * saturation)
          
          t2 = 2 * luminance - t1
          
          hue = hue / 360
          
          rgbBis = [hue + 0.3333 , hue , hue - 0.3333]
          
          for index in range(3):
               if rgbBis[index] > 1:
                    rgbBis[index] -= 1
               elif rgbBis[index] < 0:
                    rgbBis[index] += 1
          
          rgb = []
          
          for value in rgbBis:
               if 6*value < 1:
                    final_color = t2 + (t1 - t2)
               elif 2*value < 1:
                    final_color = t1
               elif 3*value < 2:
                    final_color = t2 + (t1 - t2) * (0.6666 - value) * 6
               else:
                    final_color = t2
               
               rgb.append(final_color)
          
          return [int(rgb[0]*255) , int(rgb[1]*255) , int(rgb[2]*255)]
     
     @staticmethod
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

     @staticmethod
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

     @staticmethod
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

          img2 = Image.symHori(image_data)
          img2 = Image.symVert(img2)
          # newpix.append(img2)


          img2["meta"]["mod"]="Rotation a 180 degrès"
          return img2

     @staticmethod
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

     @staticmethod
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

     @staticmethod
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

     @staticmethod
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

     @staticmethod
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

     @staticmethod
     def rotation(image_data , degree):
     
          raise NotImplementedError("Rotation function not implemented !")
     
          # pixtab = []
          # centerx = image_data["meta"]["lig"] // 2
          # centery = image_data["meta"]["col"] // 2
          
          
          
          # final_image_data = image_data.copy()
          # # final_image_data["pix"] = new_pix
          # final_image_data["meta"]["mod"]="Rotation"
          # final_image_data["meta"]["col"] = size[0]
          # final_image_data["meta"]["lig"] = size[1]
          
          # return final_image_data
     
     
     def display(self , surface : pygame.Surface , centered=False):
          
          try:
               if not centered:
                    surface.blit(self.texture , [self.rect.x, self.rect.y])
               else:
                    surface.blit(self.texture , [surface.get_rect().width // 2 - self.rect.width // 2, surface.get_rect().height // 2 - self.rect.height // 2])
          except:
               pass

class Img_displayer():
     
     def __init__(self, pos : list , size : list):
          
          self.rect = Rect(pos , size)
          
          self.surface = pygame.Surface(self.rect.size)
          
          self.image = Image([0,0])
          self.zoom = 3
          self.zooms = [0.25 , 0.5 , 0.75 , 1 , 1.25 , 1.5 , 1.75 , 2 , 2.5 , 3 , 3.5 , 4 , 4.5 , 5 , 7.5 , 10 , 15 , 20]
     
     def event_handler(self , event : pygame.event.Event , offset_detection=[0,0]):
               
          if event.type == MOUSEBUTTONDOWN:
               
               if event.button == 4 and offset_detection[0] < event.pos[0] < self.rect.right + offset_detection[0] and offset_detection[1] < event.pos[1] < self.rect.right + offset_detection[1]:
                    self.zoom += 1
                    if self.zoom > 17:
                         self.zoom = 17
               
               if event.button == 5 and offset_detection[0] < event.pos[0] < self.rect.right + offset_detection[0] and offset_detection[1] < event.pos[1] < self.rect.right + offset_detection[1]:
                    self.zoom -= 1 
                    if self.zoom < 0:
                         self.zoom = 0
     
     def resize(self):
          
          final_zoom = 3
          
          
          
          if max(self.image.rect.size) == self.image.rect.width:
               
               if self.image.rect.width > self.rect.width:
                    for z in range(3 , 0 , -1):
                         final_zoom -= 1
                         if self.image.rect.width * self.zooms[final_zoom] < self.rect.width:
                              self.zoom = final_zoom
                              return
               else:
                    for z in range(0 , 14 , 1):
                         final_zoom += 1
                         if round((self.image.rect.width * self.zooms[final_zoom]) / self.rect.width , 2) > 0.7:
                              self.zoom = final_zoom
                              return
                         
          elif max(self.image.rect.size) == self.image.rect.height:
               
               if self.image.rect.height > self.rect.height:
                    for z in range(3 , 0 , -1):
                         final_zoom -= 1
                         if self.image.rect.height * self.zooms[final_zoom] < self.rect.height:
                              self.zoom = final_zoom
                              return
               else:
                    for z in range(0 , 14 , 1):
                         final_zoom += 1
                         if round((self.image.rect.height * self.zooms[final_zoom]) / self.rect.height , 2) > 0.7:
                              self.zoom = final_zoom
                              return
          
          self.zoom = final_zoom            
          
     
     def display(self , surface : pygame.Surface):
          
          final_surface = self.surface.copy()
          if self.image.image_loaded:
               image = pygame.transform.scale(self.image.texture, [self.image.rect.width*self.zooms[self.zoom] , self.image.rect.height*self.zooms[self.zoom]])
               final_surface.blit(image , [self.rect.width // 2 - image.get_rect().width // 2 , self.rect.height // 2 - image.get_rect().height // 2 ])
          surface.blit(final_surface , [self.rect.x , self.rect.y])
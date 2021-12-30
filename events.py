import pygame
import traitement

from ui import *
from pygame.locals import *

app = None

def undo():
     try:
          backup = app.panels["Img displayer"].img_displayer.image.image_data_backup.pop()
          app.panels["Img displayer"].img_displayer.image.load_by_data(backup , False)
     except:
          pass
     
     
def add_file():
     image = Image([0,0])
     try:
          image.load(app.ui["entry_img1"].stringValue)
          height = len(app.panels["File list"].files)
          selector = Image_selector([0,height * 26],[app.panels["File list"].rect.width - 20 , 26],{"stringvalue":image.name , "padding left":20} , image)
          selector.target = load_image
          app.panels["File list"].files.append(selector)
     except:
          pass


def load_image(image):
     
     app.panels["Img displayer"].img_displayer.image = image 
     app.panels["Img displayer"].img_displayer.resize()

def remove_ffl(selector):
     
     index = app.panels["File list"].files.index(selector)
     app.panels["File list"].files.remove(selector)
     
     if app.panels["File list"].files == []:
          app.panels["Img displayer"].img_displayer.image = Image([0,0])
     else :
          try:
               app.panels["Img displayer"].img_displayer.image = app.panels["File list"].files[index].value
               app.panels["Img displayer"].img_displayer.resize()
          except:
               app.panels["Img displayer"].img_displayer.image = app.panels["File list"].files[index - 1].value
               app.panels["Img displayer"].img_displayer.resize()

def sym_hori():
     
     try:
          image_data = traitement.symHori(app.panels["Img displayer"].img_displayer.image.image_data)
          app.panels["Img displayer"].img_displayer.image.load_by_data(image_data)
     except:
          pass
          

def sym_vert():
     
     try:
          image_data = traitement.symVert(app.panels["Img displayer"].img_displayer.image.image_data)
          app.panels["Img displayer"].img_displayer.image.load_by_data(image_data)
     except:
          pass

def rot_180():
     
     try:
          image_data = traitement.rotation180(app.panels["Img displayer"].img_displayer.image.image_data)
          app.panels["Img displayer"].img_displayer.image.load_by_data(image_data)
     except:
          pass
          

def rot_90():
     
     try:
          image_data = traitement.rotation90(app.panels["Img displayer"].img_displayer.image.image_data)
          app.panels["Img displayer"].img_displayer.image.load_by_data(image_data)
     except:
          pass

def pgm_conv():
     
     try:
          image_data = traitement.conversion_ppm_en_pgm(app.panels["Img displayer"].img_displayer.image.image_data)
          app.panels["Img displayer"].img_displayer.image.load_by_data(image_data)
     except:
          pass

def pbm_conv():
     
     try:
          int_conv = int(app.ui["entry_intConvPBM"].stringValue)
          image_data = traitement.bitmap_conversion(app.panels["Img displayer"].img_displayer.image.image_data , int_conv)
          app.panels["Img displayer"].img_displayer.image.load_by_data(image_data)
     except:
          pass

def luminosity():
     
     try:
          luminance = int(app.ui["entry_luminance"].stringValue)
          image_data = traitement.luminosity(app.panels["Img displayer"].img_displayer.image.image_data , luminance)
          app.panels["Img displayer"].img_displayer.image.load_by_data(image_data)
     except:
          pass

def extend(package):
     
     if package.case:
          package.case = 0
     else:
          package.case = 1
     
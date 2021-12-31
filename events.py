import pygame
import traitement

from ui import *
from image import *
from pygame.locals import *

app = None

def open_window(window):
     
     filtre = pygame.Surface(app.screen.get_rect().size , SRCALPHA)
     filtre.fill([0, 0, 0 , 64])
     
     app.screen.blit(filtre , [0,0])
     
     window.opened = True
     app.is_window_open = True

def close_window(window):
     
     window.opened = False
     app.is_window_open = False


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
          oc = ""
          oc_number = 0
          for select in app.panels["File list"].files:
               if select.value.name == image.name:
                    oc_number += 1
          
          if oc_number != 0:
               oc = f" ( {oc_number} )"
          selector = Image_selector([0,height * 20],[app.panels["File list"].rect.width - 20 , 20],{"stringvalue":image.name+oc , "padding left":20 , "color":[255 , 255 , 255]} , image)
          
          textures = [pygame.Surface([1,1] , SRCALPHA),pygame.Surface([1,1] , SRCALPHA),pygame.Surface([1,1]) , SRCALPHA]
          
          textures[0].fill([18, 12, 54, 0])
          textures[1].fill([58, 42, 142, 0.60*128])
          textures[2].fill([58, 42, 142, 1*128])
          
          selector.load_textures(textures)
          
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
          image_data = Image.symHori(app.panels["Img displayer"].img_displayer.image.image_data)
          app.panels["Img displayer"].img_displayer.image.load_by_data(image_data)
     except:
          pass
          

def sym_vert():
     
     try:
          image_data = Image.symVert(app.panels["Img displayer"].img_displayer.image.image_data)
          app.panels["Img displayer"].img_displayer.image.load_by_data(image_data)
     except:
          pass

def rot_180():
     
     try:
          image_data = Image.rotation180(app.panels["Img displayer"].img_displayer.image.image_data)
          app.panels["Img displayer"].img_displayer.image.load_by_data(image_data)
     except:
          pass
          

def rot_90():
     
     try:
          image_data = Image.rotation90(app.panels["Img displayer"].img_displayer.image.image_data)
          app.panels["Img displayer"].img_displayer.image.load_by_data(image_data)
     except:
          pass

def pgm_conv():
     
     try:
          image_data = Image.conversion_ppm_en_pgm(app.panels["Img displayer"].img_displayer.image.image_data)
          app.panels["Img displayer"].img_displayer.image.load_by_data(image_data)
     except:
          pass

def pbm_conv():
     
     try:
          int_conv = int(app.ui["entry_intConvPBM"].stringValue)
          image_data = Image.bitmap_conversion(app.panels["Img displayer"].img_displayer.image.image_data , int_conv)
          app.panels["Img displayer"].img_displayer.image.load_by_data(image_data)
     except:
          pass

def luminosity():
     
     try:
          luminance = int(app.ui["entry_luminance"].stringValue)
          image_data = Image.luminosity(app.panels["Img displayer"].img_displayer.image.image_data , luminance)
          app.panels["Img displayer"].img_displayer.image.load_by_data(image_data)
     except:
          pass

def saturation():
     
     try:
          int_saturation = int(app.ui["entry_saturation"].stringValue)
          image_data = Image.saturation(app.panels["Img displayer"].img_displayer.image.image_data , int_saturation)
          app.panels["Img displayer"].img_displayer.image.load_by_data(image_data)
     except:
          pass
     
def rotation():
     
     try:
          degree = int(app.ui["entry_rotation"].stringValue)
          image_data = Image.rotation(app.panels["Img displayer"].img_displayer.image.image_data , degree)
          app.panels["Img displayer"].img_displayer.image.load_by_data(image_data)
     except:
          pass

def extend(package):
     
     if package.case:
          package.case = 0
     else:
          package.case = 1
     
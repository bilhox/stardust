import pygame
import traitement
import filters

from ui import *
from image import *
from pygame.locals import *

app = None

def open_window(window):
     
     filtre = pygame.Surface(app.screen.get_rect().size , SRCALPHA)
     filtre.fill([0, 0, 0 , 128])
     
     app.screen.blit(filtre , [0,0])
     
     window.opened = True
     app.is_window_open = True
     app.current_window = window

def close_window(window):
     
     window.opened = False
     app.is_window_open = False
     app.current_window = None


def undo():
     try:
          backup = app.panels["Img displayer"].img_displayer.image.image_data_backup.pop()
          app.panels["Img displayer"].img_displayer.image.load_by_data(backup , False)
     except:
          pass

def search_files():

     try:
          path = app.current_window.components["entry_folderPath"].stringValue
          file_list = os.listdir(path)
          image_list = []
          
          for file_path in file_list:
               if os.path.splitext(file_path)[1].lower() in [".png" , ".jpg" , ".ppm" , ".pbm" , ".pgm"]:
                    image_list.append(file_path)
          
          if len(app.current_window.components["FileList_fileFounded"].files) != 0:
               app.current_window.components["FileList_fileFounded"].files = []
          
          for file in image_list:
               height = len(app.current_window.components["FileList_fileFounded"].files)
               selector = File_selector([0,height * 20],[app.current_window.components["FileList_fileFounded"].rect.width - 20 , 20],{"stringvalue":file , "padding left":20 , "color":[255 , 255 , 255]} , path+"\\"+file)
               
               textures = [pygame.Surface([1,1] , SRCALPHA),pygame.Surface([1,1] , SRCALPHA),pygame.Surface([1,1]) , SRCALPHA]
               
               textures[0].fill([18, 12, 54, 0])
               textures[1].fill([58, 42, 142, 0.60*128])
               textures[2].fill([58, 42, 142, 1*128])
               
               selector.load_textures(textures)
               
               app.current_window.components["FileList_fileFounded"].files.append(selector)
     except:
          pass
     
def add_file():
     image = Image([0,0])
     
     try:
          selector = None
          for select in app.current_window.components["FileList_fileFounded"].files:
               if select.selected:
                    selector = select
          
          if selector == None:
               return
               
          image.load(selector.value)
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
          
          close_window(app.current_window)
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
          app.panels["Img displayer"].img_displayer.image.load_by_data(image_data , False)
     except:
          pass
          

def sym_vert():
     
     try:
          image_data = Image.symVert(app.panels["Img displayer"].img_displayer.image.image_data)
          app.panels["Img displayer"].img_displayer.image.load_by_data(image_data , False)
     except:
          pass

def rot_180():
     
     try:
          image_data = Image.rotation180(app.panels["Img displayer"].img_displayer.image.image_data)
          app.panels["Img displayer"].img_displayer.image.load_by_data(image_data , False)
     except:
          pass
          

def rot_90():
     
     try:
          image_data = Image.rotation90(app.panels["Img displayer"].img_displayer.image.image_data)
          app.panels["Img displayer"].img_displayer.image.load_by_data(image_data , False)
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
          int_conv = int(app.panels["Tool panel"].panels["main tools"].components["entry_intConvPBM"].stringValue)
          image_data = Image.bitmap_conversion(app.panels["Img displayer"].img_displayer.image.image_data , int_conv)
          app.panels["Img displayer"].img_displayer.image.load_by_data(image_data)
     except:
          pass

def luminosity():
     
     try:
          luminance = int(app.panels["Tool panel"].panels["main tools"].components["entry_luminance"].stringValue)
          image_data = filters.red(app.panels["Img displayer"].img_displayer.image.image_data , luminance)
          app.panels["Img displayer"].img_displayer.image.load_by_data(image_data)
     except:
          pass

def saturation():
     
     try:
          int_saturation = int(app.panels["Tool panel"].panels["main tools"].components["entry_saturation"].stringValue)
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

def resize_image():
     
     new_size = [int(app.panels["Tool panel"].panels["main tools"].components["entry_xSize"].stringValue) , int(app.panels["Tool panel"].panels["main tools"].components["entry_ySize"].stringValue)]
     image_data = traitement.resize_image(app.panels["Img displayer"].img_displayer.image.image_data , new_size)
     app.panels["Img displayer"].img_displayer.image.load_by_data(image_data)

def extend(package):
     
     if package.case:
          package.case = 0
     else:
          package.case = 1
     
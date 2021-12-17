
import pygame
import components
import traitement


def load_image(app):
          
          app.canva_components["toile"].image.path = app.packages["traitement"].components["entry_img1"].stringValue
          try:
               app.canva_components["toile"].image.load()
               app.canva_components["toile"].resize()
               app.file_founded = True
          except FileNotFoundError as error:
               print(error)
               app.file_founded = False
          except pygame.error as pygame_error:
               print(pygame_error)
               app.file_founded = False

def reset_image(app):
     
     app.canva_components["toile"].image = components.Image("image" , "" , app.canva_components["toile"].image.pos)

def sym_hori(app):
     
     try:
          image_data = traitement.symHori(app.canva_components["toile"].image.image_data)
          app.canva_components["toile"].image.load_by_data(image_data)
     except:
          pass
          

def sym_vert(app):
     
     try:
          image_data = traitement.symVert(app.canva_components["toile"].image.image_data)
          app.canva_components["toile"].image.load_by_data(image_data)
     except:
          pass

def rot_180(app):
     
     try:
          image_data = traitement.rotation180(app.canva_components["toile"].image.image_data)
          app.canva_components["toile"].image.load_by_data(image_data)
     except:
          pass
          

def rot_90(app):
     
     try:
          image_data = traitement.rotation90(app.canva_components["toile"].image.image_data)
          app.canva_components["toile"].image.load_by_data(image_data)
     except:
          pass

def pgm_conv(app):
     
     try:
          image_data = traitement.conversion_ppm_en_pgm(app.canva_components["toile"].image.image_data)
          app.canva_components["toile"].image.load_by_data(image_data)
     except:
          pass

def pbm_conv(app):
     
     try:
          image_data = traitement.bitmap_conversion(app.canva_components["toile"].image.image_data)
          app.canva_components["toile"].image.load_by_data(image_data)
     except:
          pass

def extend(package):
     
     if package.case:
          package.case = 0
     else:
          package.case = 1
     
import numpy as np
import cv2

def rellenar(img):
   '''
   Recibe una imagen binaria, devuelve la misma imagen con
   las formas huecas rellenas.
   '''
   img_flood_fill = img.copy().astype('uint8')
   h, w = img.shape[:2]
   mask = np.zeros((h+2, w+2), np.uint8)
   cv2.floodFill(img_flood_fill, mask, (0,0), 255)
   img_flood_fill_inv = cv2.bitwise_not(img_flood_fill)
   img_fh = img | img_flood_fill_inv
   return img_fh 
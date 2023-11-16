import numpy as np
import cv2

def calcular_factor_forma(img):
   '''
   Recibe una sub-imagen y devuelve su factor de forma
   '''
   ext_cont, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   area = cv2.contourArea(ext_cont[0])
   perimeter = cv2.arcLength(ext_cont[0], True)
   rho = 4 * np.pi * area /(perimeter ** 2)
   return rho
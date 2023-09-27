from argparse import ArgumentParser
import numpy as np
import cv2

parser = ArgumentParser()
parser.add_argument(
        'Imgs',
         nargs='+',
         help='Path de las imágenes')

args = parser.parse_args()

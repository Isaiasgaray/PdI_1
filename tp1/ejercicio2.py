import cv2
import numpy as np
from math import dist
from argparse import ArgumentParser
from os.path import basename
# import matplotlib.pyplot as plt

parser = ArgumentParser()
parser.add_argument(
        'Imgs',
        nargs='+',
        help='Path de las imágenes')

args = parser.parse_args()

def procesar_formulario(path):

    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        return None

    UMBRAL = 118
    MAX_COLS = 400
    MAX_ROWS = 800

    img_binaria = img < UMBRAL

    cols = np.sum(img_binaria, 0)
    rows = np.sum(img_binaria, 1)

    cols_idx = np.argwhere(cols > MAX_COLS)
    rows_idx = np.argwhere(rows > MAX_ROWS)

    _, c2, c3 = cols_idx[:, 0]
    _, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11 = rows_idx[:, 0]

    coordenadas = {
    'nombre': (r2, r3),
    'edad': (r3, r4),
    'mail': (r4, r5),
    'legajo': (r5, r6),
    'pregunta1': (r7, r8),
    'pregunta2': (r8, r9),
    'pregunta3': (r9, r10),
    'comentarios': (r10, r11)
    }

    img_dict = dict()

    for key, (start_row, end_row) in coordenadas.items():
        img_dict[key] = [img_binaria[start_row + 2: end_row - 2, c2 + 2:c3 - 2], 0]

    return img_dict

def contar_espacios(stats):
    stats_sort = stats[stats[:, 0].argsort()][1:, :]

    espacios = 0
    DISTANCIA_MAX = 9

    for i in range(len(stats_sort) - 1):
        primer_punto = (stats_sort[i][0] + stats_sort[i][2], 0)
        segundo_punto = (stats_sort[i + 1][0], 0)

        if dist(primer_punto, segundo_punto) >= DISTANCIA_MAX:
            espacios += 1

    return espacios

def connected_components(img):
    return cv2.connectedComponentsWithStats(
                img[0].astype(np.uint8),
                8,
                cv2.CV_32S)

def validar_nombre(img_dict):
    num_labels, _, stats, _ = connected_components(img_dict['nombre'])
    espacios = contar_espacios(stats)

    if espacios > 0 and (num_labels + espacios - 1) <= 25:
        img_dict['nombre'][1] = 1

def validar_edad(img_dict):
    num_labels, _, stats, _ = connected_components(img_dict['edad'])
    espacios = contar_espacios(stats)

    if (num_labels - 1 + espacios) in [2, 3]:
        img_dict['edad'][1] = 1

def validar_mail(img_dict):
    num_labels, _, stats, _ = connected_components(img_dict['mail'])
    espacios = contar_espacios(stats)

    if num_labels - 1 and espacios == 0 and num_labels - 1 <= 25:
        img_dict['mail'][1] = 1

def validar_legajo(img_dict):
    num_labels, _, stats, _ = connected_components(img_dict['legajo'])
    espacios = contar_espacios(stats)

    if espacios == 0 and num_labels - 1 == 8:
        img_dict['legajo'][1] = 1

def validar_preguntas(img_dict):
    keys = [f'pregunta{i}' for i in range(1, 4)]

    for key in keys:
        num_l, *_ = connected_components(img_dict[key])
        
        if num_l == 3:
            img_dict[key][1] = 1

def validar_comentarios(img_dict):
    num_labels, _, stats, _ = connected_components(img_dict['comentarios'])
    espacios = contar_espacios(stats)

    if num_labels - 1 and (num_labels - 1 + espacios) <= 25:
        img_dict['comentarios'][1] = 1


def validar_imagen(img_dict):
    funciones = [validar_nombre, validar_edad, validar_mail,
                 validar_legajo, validar_preguntas, validar_comentarios]
    
    for funcion in funciones:
        funcion(img_dict)

    for key, (_, val2) in img_dict.items():
        print(f'{key.capitalize() + ":":<20} {"OK" if val2 else "MAL"}')

for path in args.Imgs:
    img = procesar_formulario(path)

    if img:
        print(basename(path))
        print('=' * 24)
        validar_imagen(img)

    print()
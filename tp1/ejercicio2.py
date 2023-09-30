# from argparse import ArgumentParser
# import numpy as np
# import cv2

# parser = ArgumentParser()
# parser.add_argument(
#         'Imgs',
#          nargs='+',
#          help='Path de las imágenes')

# args = parser.parse_args()

import cv2
import numpy as np
import matplotlib.pyplot as plt


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


img1 = procesar_formulario('img/formulario_04.png')

plt.imshow(img1['pregunta1'][0], cmap='gray'), plt.show(block=False)

num_labels, *_ = cv2.connectedComponentsWithStats(img1['pregunta2'][0].astype(np.uint8), 8, cv2.CV_32S)

# im_color = cv2.applyColorMap(np.uint8(255/num_labels*labels), cv2.COLORMAP_JET)

#for st in stats:
#    cv2.rectangle(im_color,(st[0],st[1]),(st[0]+st[2],st[1]+st[3]),color=(0,255,0),thickness=1)

# plt.imshow(im_color), plt.show(block=False)
num_labels

def validar_preguntas(img_dict):
    keys = [f'pregunta{i}' for i in range(1, 4)]

    for key in keys:
        num_l, *_ = cv2.connectedComponentsWithStats(
                        img_dict[key][0].astype(np.uint8),
                        8,
                        cv2.CV_32S)
        
        if num_l == 3:
            img_dict[key][1] = 1


validar_preguntas(img1)

img1['pregunta1'][1]
img1['pregunta2'][1]
img1['pregunta3'][1]

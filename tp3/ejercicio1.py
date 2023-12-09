import matplotlib.pyplot as plt
from pathlib import Path
from src import imutils
import cv2

# path_videos = [f'videos/tirada_{i}.mp4' for i in range(1, 5)]

def crear_mascara_dados(frame_hsv, umbral_matiz, umbral_intensidad):
    '''
    Recibe un frame de los dados con mapa de colores HSV y
    los umbrales para los canales H y S, devuelve la máscara
    para de los dados para el frame recibido
    '''

    h, s, _ = cv2.split(frame_hsv)

    h_umbralado = (h > umbral_matiz).astype('uint8')
    s_umbralado = (s > umbral_intensidad).astype('uint8')

    return cv2.bitwise_and(h_umbralado, s_umbralado)

PATH = 'videos/tirada_1.mp4'

cap, width, height, fps, _ = imutils.leer_video(PATH)

# Los frames se leen en BGR
# entonces setemos la constante
# para el color azul

DADOS_C = (255, 0, 0)
TEXTO_C = (255, 255, 255)

frame_numero = 1

# Basename del archivo
# Path(PATH).name

out = cv2.VideoWriter(f'{Path(PATH).stem}_out.mp4',
                      cv2.VideoWriter_fourcc(*'mp4v'),
                      fps,
                      (int(width/3),
                       int(height/3)))


frames_consecutivos = 0
centroides_anteriores = list()

while (cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        
        frame = cv2.resize(frame, dsize=(int(width/3), int(height/3)))
        frame_gris = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        frame_hsv  = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

        UMBRAL_H = 100
        UMBRAL_S = 100

        mask_dados = crear_mascara_dados(frame_hsv,
                                         UMBRAL_H,
                                         UMBRAL_S)

        # if frame_numero < 75:
        #     frame_numero += 1
        #     continue

        elemento_estructural = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 2))
        img_cierre = cv2.morphologyEx(mask_dados, cv2.MORPH_CLOSE, elemento_estructural)
    
        # cv2.imshow('Frame', mask_dados)
        # ax = plt.subplot(221)
        # plt.imshow(cv2.morphologyEx(mask_dados, cv2.MORPH_CLOSE, elemento_estructural))
        # plt.title(frame_numero)
        # plt.subplot(222, sharex=ax, sharey=ax)
        # plt.imshow(mask_dados)
        # plt.subplot(223, sharex=ax, sharey=ax)
        # plt.imshow(mask_h)
        # plt.subplot(224, sharex=ax, sharey=ax)
        # plt.imshow(mask_s)
        # plt.show()
        
        n, labels, stats, centroids = cv2.connectedComponentsWithStats(img_cierre)
        cant_dados = 0
        posibles_dados = list()
        UMBRAL_DIF = .2
        centroides_actuales   = list()

        # Filtramos los dados por área y factor de forma
        for i in range(1, n):

            img_bool = (labels == i).astype('uint8')

            if stats[i][cv2.CC_STAT_AREA] < 300:
                continue

            rho = imutils.calcular_factor_forma(img_bool)

            if rho < 0.50:
                continue

            # plt.imshow(img_bin, cmap='gray')
            # plt.title(f'diff_x: {dif_x}, diff_y: {dif_y} rho: {rho}')
            # plt.show()

            posibles_dados.append((stats[i], img_bool))
            centroides_actuales.append(centroids[i])

            cant_dados += 1

        resultados = [
            abs(dado_act[0] - dado_prev[0]) < 0.6
            for dado_act, dado_prev in 
            zip(centroides_actuales, centroides_anteriores)]

        
        if len(resultados) == 5 and all(resultados):
            frames_consecutivos += 1
        else:
            frames_consecutivos = 0

        # if any(dado[2] for dado in posibles_dados):
        #     frames_consecutivos += 1
        # else:
        #     frames_consecutivos = 0

        if cant_dados == 5 and frames_consecutivos >= 2:
            for dado in posibles_dados:

                n = imutils.contar_contornos(dado[1])

                imutils.graficar_caja(
                            frame,
                            dado[0],
                            (255, 0, 0),
                            thickness=2,
                            text=str(n - 1),
                            fontScale=.7,
                            color_text=TEXTO_C)

        cv2.imshow(f'frame', frame)
        out.write(frame)
        # plt.imshow(frame)
        # plt.title(f'{frame_numero} - {centroides_actuales[0]} {centroides_actuales[0].shape} {type(centroides_actuales[0])}')
        # plt.show()

        frame_numero += 1
        centroides_anteriores = centroides_actuales

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()

# Gráficas para el informe
# =========================
'''
cap, width, height, fps, _ = imutils.leer_video('videos/tirada_1.mp4')

frame_numero = 1
while (cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break
        
    if frame_numero != 75:
        frame_numero += 1
        continue
    
    frame = cv2.resize(frame, dsize=(int(width/3), int(height/3)))
    frame_hsv  = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    h, s, _ = cv2.split(frame_hsv)

    mask_h = (h > 100).astype('uint8')

    mask_s = (s > 100).astype('uint8')

    mask_dados = cv2.bitwise_and(mask_h, mask_s)

    elemento_estructural = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 2))
    img_cierre = cv2.morphologyEx(mask_dados, cv2.MORPH_CLOSE, elemento_estructural)

    ax = plt.subplot(141)
    plt.imshow(frame_hsv)
    plt.title('Frame en HSV')
    plt.subplot(142, sharex=ax, sharey=ax)
    plt.imshow(mask_h, cmap='gray')
    plt.title('Filtrado por matiz')
    plt.subplot(143, sharex=ax, sharey=ax)
    plt.imshow(mask_s, cmap='gray')
    plt.title('Filtrado por saturación')
    plt.subplot(144, sharex=ax, sharey=ax)
    plt.imshow(mask_dados, cmap='gray')
    plt.title('Intersección')
    ax.axes.get_xaxis().set_ticks([])
    ax.axes.get_yaxis().set_ticks([])
    plt.show()

    ax = plt.subplot(141)
    plt.imshow(mask_h, cmap='gray')
    plt.title('Filtrado por matiz')
    plt.subplot(142, sharex=ax, sharey=ax)
    plt.imshow(mask_s, cmap='gray')
    plt.title('Filtrado por saturación')
    plt.subplot(143, sharex=ax, sharey=ax)
    plt.imshow(mask_dados, cmap='gray')
    plt.title('Intersección')
    plt.subplot(144, sharex=ax, sharey=ax)
    plt.imshow(img_cierre, cmap='gray')
    plt.title('Operación de clausura')
    ax.axes.get_xaxis().set_ticks([])
    ax.axes.get_yaxis().set_ticks([])
    plt.show()
        
    frame_numero += 1

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
    else:
        break
'''
# =========================
import matplotlib.pyplot as plt
from src.pars import parser
from pathlib import Path
from src import imutils
import cv2

# Variabes gloables
# =========================

# Variables para setear 
# colores del procesamiento
DADOS_C = (255, 0, 0)
TEXTO_C = (255, 255, 255)

# Variables para filtrar los dados
AREA_MIN = 300
UMBRAL_H = 100
UMBRAL_S = 100
RHO_TH = 0.50

# Factor para escalar las
# dimensiones de los videos 
FACTOR = 1/3

# Tamaño del elemento estructural    
K_SIZE = (3, 2)

# Umbral para las diferencias 
# en los centroides
UMBRAL_DIF = 0.6

# Funciones auxiliares
# =========================

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

def procesar_frame(frame):
    '''
    Recibe un frame escalado, devuelve
    una imagen binaria de este frame 
    con los dados segmentados.
    '''
    frame_hsv  = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    mask_dados = crear_mascara_dados(frame_hsv,
                                     UMBRAL_H,
                                     UMBRAL_S)

    elemento_estructural = cv2.getStructuringElement(
                                        cv2.MORPH_RECT,
                                        K_SIZE)
    
    return cv2.morphologyEx(mask_dados,
                            cv2.MORPH_CLOSE,
                            elemento_estructural)
   

def filtrar_dados(n, labels, stats, centroids):
    '''
    Recibe el output de connectedComponentsWithStats,
    devuelve una lista de posibles dados y otra con 
    los centroides de esos dados.
    '''
    
    posibles_dados       = list()
    centroides_actuales  = list()

    for i in range(1, n):

        img_bool = (labels == i).astype('uint8')

        if stats[i][cv2.CC_STAT_AREA] < AREA_MIN:
            continue

        rho = imutils.calcular_factor_forma(img_bool)

        if rho < RHO_TH:
            continue

        posibles_dados.append((stats[i], img_bool))
        centroides_actuales.append(centroids[i])

    return posibles_dados, centroides_actuales

def graficar_dados(tuplas_dados, frame, dados_c, texto_c):
    '''
    Función para graficar los bounding box
    y números de cada dado
    '''
    for tupla in tuplas_dados:
        stats_dado, dado_bool = tupla

        n = imutils.contar_contornos(dado_bool)

        imutils.graficar_caja(
                    frame,
                    stats_dado,
                    dados_c,
                    thickness=2,
                    text=str(n - 1),
                    fontScale=.7,
                    color_text=texto_c)

def procesar_video(path):
    '''
    Recibe un path a un video, lo procesa y 
    muestra por pantalla, guarda una copia del video.
    '''
    cap, width, height, fps, _ = imutils.leer_video(path)

    file_name   = Path(path).name
    file_output = f'videos/{Path(path).stem}_out.mp4'

    ANCHO_E = int(width  * FACTOR)
    LARGO_E = int(height * FACTOR)
    DIM_E   = (ANCHO_E, LARGO_E)

    out = cv2.VideoWriter(file_output,
                         cv2.VideoWriter_fourcc(*'mp4v'),
                         fps, DIM_E)

    frames_consecutivos   = 0
    centroides_anteriores = list()

    while (cap.isOpened()):
        ret, frame = cap.read()

        if not ret:
            break

        frame = cv2.resize(frame, dsize=DIM_E)
        frame_proc = procesar_frame(frame)

        n, labels, stats, centroids = \
                cv2.connectedComponentsWithStats(frame_proc)
        
        centroides_actuales = list()

        dados, centroides_actuales = filtrar_dados(n,
                                                   labels, 
                                                   stats,
                                                   centroids)

        resultados = [
            abs(dado_act[0] - dado_prev[0]) < UMBRAL_DIF
            for dado_act, dado_prev in 
            zip(centroides_actuales, centroides_anteriores)]

        if len(resultados) == 5 and all(resultados):
            frames_consecutivos += 1
        else:
            frames_consecutivos = 0

        if frames_consecutivos >= 2:
            graficar_dados(dados,
                        frame,
                        DADOS_C,
                        TEXTO_C)
            
        cv2.imshow(f'{file_name}', frame)
        out.write(frame)

        centroides_anteriores = centroides_actuales

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Función principal
# =========================

def main():
    args = parser.parse_args()

    for path in args.Videos:
        procesar_video(path)

if __name__ == '__main__':
    main()

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
'''
# =========================
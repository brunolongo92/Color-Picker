import cv2
import numpy as np
import matplotlib.pyplot as plt
import colorsys
import webcolors

# Función para encontrar el color más cercano usando la distancia Euclidiana
def closest_colour(requested_colour):
    min_colours = {}
    for name in webcolors.names("css3"):  # Usamos CSS3_HEX_TO_NAMES para obtener el color en formato hexadecimal
        r_c, g_c, b_c = webcolors.name_to_rgb(name)  # Convertimos el color hex a RGB
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name  # Calculamos la distancia
    return min_colours[min(min_colours.keys())]  # Devolvemos el nombre del color más cercano

# Función para capturar el color al hacer clic en la imagen
colores_seleccionados = []

def seleccionar_color(event, x, y, flags, param):
    global colores_seleccionados
    if event == cv2.EVENT_LBUTTONDOWN:  # Si se hace clic izquierdo
        color_bgr = frame[y, x]  # Captura el color en formato BGR
        color_rgb = tuple(color_bgr[::-1])  # Convertir de BGR a RGB
        colores_seleccionados.append(color_rgb)  # Guardar el color
        nombre_color = closest_colour(color_rgb)  # Obtener el nombre del color más cercano
        print(f"Color seleccionado (RGB): {color_rgb} -> Nombre aproximado: {nombre_color}")

# Función para generar combinaciones estéticas
def generar_colores_esteticos(color_rgb):
    r, g, b = [x / 255.0 for x in color_rgb]  # Normalizar RGB a [0, 1]
    h, l, s = colorsys.rgb_to_hls(r, g, b)  # Convertir a HLS (tono, luminosidad, saturación)

    # Generar combinaciones
    complementario = colorsys.hls_to_rgb((h + 0.5) % 1, l, s)
    analogos = [
        colorsys.hls_to_rgb((h - 0.1) % 1, l, s),
        colorsys.hls_to_rgb((h + 0.1) % 1, l, s),
    ]
    triadicos = [
        colorsys.hls_to_rgb((h + 1/3) % 1, l, s),
        colorsys.hls_to_rgb((h + 2/3) % 1, l, s),
    ]

    # Convertir los resultados a RGB [0, 255]
    colores = {
        "original": color_rgb,
        "complementario": [int(x * 255) for x in complementario],
        "analogos": [[int(x * 255) for x in color] for color in analogos],
        "triadicos": [[int(x * 255) for x in color] for color in triadicos],
    }
    return colores

# Abrir la cámara del dispositivo
cap = cv2.VideoCapture(0)  # El índice '0' es para la cámara por defecto
if not cap.isOpened():
    print("No se pudo abrir la cámara.")
    exit()

# Mostrar el video y capturar colores
while True:
    ret, frame = cap.read()  # Captura un frame de la cámara
    if not ret:
        print("No se pudo recibir el frame.")
        break

    cv2.imshow('Seleccionar Color (Cámara)', frame)
    cv2.setMouseCallback('Seleccionar Color (Cámara)', seleccionar_color)

    # Si el usuario presiona 'q', sale del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()  # Liberar la cámara
cv2.destroyAllWindows()

# Generar y mostrar combinaciones para cada color seleccionado
if colores_seleccionados:
    for i, color in enumerate(colores_seleccionados):
        combinaciones = generar_colores_esteticos(color)

        # Crear una barra de colores para mostrar
        fig, ax = plt.subplots(1, 5, figsize=(15, 3))
        ax[0].imshow([[combinaciones["original"]]])
        ax[0].set_title(f"Original\n{closest_colour(color)}")
        ax[1].imshow([[combinaciones["complementario"]]])
        ax[1].set_title(f"Complementario\n{closest_colour(combinaciones['complementario'])}")
        ax[2].imshow([[combinaciones["analogos"][0]]])
        ax[2].set_title(f"Análogo 1\n{closest_colour(combinaciones['analogos'][0])}")
        ax[3].imshow([[combinaciones["analogos"][1]]])
        ax[3].set_title(f"Análogo 2\n{closest_colour(combinaciones['analogos'][1])}")
        ax[4].imshow([[combinaciones["triadicos"][0]]])
        ax[4].set_title(f"Triádico 1\n{closest_colour(combinaciones['triadicos'][0])}")
        ax[4].imshow([[combinaciones["triadicos"][1]]])
        ax[4].set_title(f"Triádico 2\n{closest_colour(combinaciones['triadicos'][1])}")

        for axis in ax:
            axis.axis('off')

        plt.suptitle(f"Combinaciones para el color {color}")
        plt.show()
else:
    print("No se seleccionaron colores.")

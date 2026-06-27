import ctypes
import os
import time
import pygame
from pygame.locals import *

class Registro(ctypes.Structure):
    _fields_ = [
        ("id", ctypes.c_ubyte),
        ("valor", ctypes.c_byte)
    ]

def Load_Image(sFile, transp=False):
    try: 
        image = pygame.image.load(sFile)
    except pygame.error as message:
        raise SystemExit(message)
    image = image.convert()
    if transp:
        color = image.get_at((0, 0))
        image.set_colorkey(color, RLEACCEL)
    return image

def Pinta_Data():
    sc.blit(Img, (0, 0))
    nDX = 15
    y_centro = 82  # Línea base en el centro exacto de la pantalla (165 / 2)
    nX = 0
    
    for nT in aT:
        # Colores basados en el valor real original recibido
        if nT < 10: nRGB = (0, 0, 255)
        elif 10 <= nT <= 25: nRGB = (0, 255, 0)
        else: nRGB = (255, 0, 0)
        
        # Mapeo de altura proporcional (máximo 70px hacia arriba o hacia abajo)
        # Rango original de c_byte: -128 a 127
        altura_pixels = int(nT * 70 / 127)
        
        # Dibujar desde el centro de la pantalla hacia arriba (si es +) o hacia abajo (si es -)
        pygame.draw.line(sc, nRGB, (nX + nDX, y_centro), (nX + nDX, y_centro - altura_pixels), 10)
        nX = nX + 12
        
    for nX in range(0, 29):
        aT[nX] = aT[nX + 1]
    return

def nFh_Head():
    nFh.write(' Data Logger de Temperaturas ' + '\n')
    nFh.write('-----------------------------' + '\n')
    nFh.write('Fecha: 06-04-2011' + '\n')
    nFh.write('Temperaturas.................' + '\n')
    nFh.write('-----------------------------' + '\n')
    return

while True:
    try:
        id_filtrar = int(input("Ingrese el 'ID' a filtrar y graficar (1 a 5): "))
        if 1 <= id_filtrar <= 5:
            break
        print("ID inválido. Debe ser un número entre 1 y 5.")
    except ValueError:
        print("Por favor, ingrese un número entero válido.")

archivo_binario = "datos_estructurados.bin"
tamano_registro = ctypes.sizeof(Registro)
registro_aux = Registro()

nRes = (475, 165)
nFh = open('tempe.txt', 'w')
aT = [0 for i in range(30)]

pygame.init()
sc = pygame.display.set_mode(nRes)
pygame.display.set_caption(f"Graficando ID: {id_filtrar}")

try:
    Img = Load_Image('Fondo_1.png')
except SystemExit:
    Img = pygame.Surface(nRes)
    Img.fill((30, 30, 30))

nFh_Head()

if os.path.exists(archivo_binario):
    f_bin = open(archivo_binario, "rb")
else:
    print(f"Esperando que se genere '{archivo_binario}'...")
    while not os.path.exists(archivo_binario):
        time.sleep(0.5)
    f_bin = open(archivo_binario, "rb")

lOk = True
while lOk:
    datos = f_bin.read(tamano_registro)
    
    if not datos:
        f_bin.seek(0)
        datos = f_bin.read(tamano_registro)

    if datos:
        ctypes.memmove(ctypes.byref(registro_aux), datos, tamano_registro)
        
        if registro_aux.id == id_filtrar:
            valor_real = registro_aux.valor  # Mantiene el signo nativo (-128 a 127)
            
            aT[29] = valor_real
            nFh.write(str(valor_real) + '\n')
            
            Pinta_Data()
            pygame.display.flip()
            time.sleep(0.1)

    ev = pygame.event.get()
    for e in ev:
        if e.type == pygame.QUIT:
            lOk = False

nFh.write('-----[EOF]-' + '\n')
f_bin.close()
nFh.close()
pygame.quit()
import pygame
import time
import random as RA
import serial
import numpy as num
import matplotlib.pyplot as plt
import matplotlib as mpl
from pygame.locals import RLEACCEL

def Load_Image(sFile,transp=False):
  try: image = pygame.image.load(sFile), 
  except pygame.error as message:
     raise SystemExit(message)
  image = image.convert()
  if transp:
   color = image.get_at((0,0))
   image.set_colorkey(color,RLEACCEL)
  return image

def Pinta_Data():
   sc.blit(Img,(0,0))
   nDX = 15; nDY = 39 ; nX = 0 ; nRGB = (0,0,0)
   for nT in aT:
    if nT < 10: nRGB = (0,0,255)
    if nT >= 10 and nT <= 25: nRGB = (0,255,0)
    if nT > 25: nRGB = (255,0,0)
    pygame.draw.line(sc,nRGB,(nX+nDX,nDY*4),(nX+nDX,(nDY-nT)*4),10)
    nX = nX + 12
   for nX in range(0,29):
    aT[nX] = aT[nX+1]
   return

def nFh_Head():
  nFh.write(' Data Logger de Temperaturas ' + '\n' )
  nFh.write('-----------------------------' + '\n' )
  nFh.write('Fecha: 06-04-2011' + '\n' )
  nFh.write('Temperaturas.................' + '\n' )
  nFh.write('-----------------------------' + '\n' )
  return

ser = serial.Serial('COM2')
ser.baudrate = 2400
nRes = (475,165) ; Fps = pygame.time.Clock()
nFh = open('tempe.txt','w')
aT = [ 0 for i in range(30) ] # 30 Samples.- aT = [0] * 30
pygame.init()
sc = pygame.display.set_mode(nRes)
Img = Load_Image('base.jpg')
nFh_Head()
lOk = True
while lOk:
 nData = int(ser.readline()[:-2])
 #nData = RA.randint(3,33)
 aT[29] = nData
 ev = pygame.event.get()
 for e in ev:
  if e.type == pygame.QUIT: lOk = False
 Pinta_Data()
 nFh.write(str(nData) + '\n' )
 pygame.display.flip()
#Fps.tick(150)
#time.sleep(.250)
nFh.write('---------[EOF]---------' + '\n' )
ser.close()
nFh.close()
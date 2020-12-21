import pygame
import numpy as np
import time

pygame.init()

#Pantalla
width, height = 680, 680
screen = pygame.display.set_mode((height, width))
#Color de fondo
bg = 25, 25, 25
screen.fill(bg)

#Celdas
nxC, nyC = 50,50
dimcW = width/nxC
dimcH = height/nyC

#Estados de las celdas. Vivas=1, Muertas=0
gameState = np.zeros((nxC, nyC))

gameState[int(nxC/2), 0] = 1

#Control de ejecución de juego
pauseExect = True

rules = list(np.binary_repr(99, width=8))
rules.reverse()

for y in range(0, nyC):
    for x in range(0, nxC):

        #Polígono de cada celda
        poly = [
            (x     * dimcW, y     * dimcH),
            ((x+1) * dimcW, y     * dimcH),
            ((x+1) * dimcW, (y+1) * dimcH),
            (x     * dimcW, (y+1) * dimcH)
        ]

        #Dibujo de la celda
        pygame.draw.polygon(screen, (128,128,128), poly, 1)

y = 0

while y < nyC:

    newGameState = np.copy(gameState)

    time.sleep(0.1)

    #Registrando eventos del teclado y ratón
    ev = pygame.event.get()

    for event in ev:
        #Se presiona una tecla
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect

        #Se presiona el ratón
        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimcW)), int(np.floor(posY / dimcH))
            newGameState[celX, celY] = not mouseClick[2]
    
    for x in range(0, nxC):

        if not pauseExect:

            ruleIdx = 4*gameState[(x-1)%nxC, y] + \
                      2*gameState[x        , y] + \
                      1*gameState[(x+1)%nxC, y]

            newGameState[x, (y+1)%nyC] = rules[int(ruleIdx)]

        #Polígono de cada celda
        poly = [
            (x     * dimcW, y     * dimcH),
            ((x+1) * dimcW, y     * dimcH),
            ((x+1) * dimcW, (y+1) * dimcH),
            (x     * dimcW, (y+1) * dimcH)
        ]

        #Dibujo de la celda
        if newGameState[x, y] == 1:
            pygame.draw.polygon(screen, (255,255,255), poly, 0)

    if not pauseExect:
        y = (y+1)

    if  y == nxC:
        pauseExect = True

    #Actualizando el juego
    gameState = np.copy(newGameState)

    pygame.display.flip()


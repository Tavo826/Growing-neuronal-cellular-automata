import pygame
import numpy as np
import time

pygame.init()

#Pantalla
width, height = 900, 680
screen = pygame.display.set_mode((height, width))
#Color de fondo
bg = 25, 25, 25
screen.fill(bg)

#Celdas
nxC, nyC = 50, 50
dimcW = width/nxC
dimcH = height/nyC

#Estados de las celdas. Vivas=1, Muertas=0
gameState = np.zeros((nxC, nyC))

#Autómata palo
gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1

#Autómata movil
gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 23] = 1

#Control de ejecución de juego
pauseExect = False

while True:

    newGameState = np.copy(gameState)

    screen.fill(bg)
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
    
    #Rejilla
    for y in range(0, nxC):
        for x in range(0, nyC):

            if not pauseExect:

                #Calculando el número de vecinos cercanos
                n_neigh = gameState[(x-1) % nxC, (y-1) % nyC] + \
                          gameState[x     % nxC, (y-1) % nyC] + \
                          gameState[(x+1) % nxC, (y-1) % nyC] + \
                          gameState[(x-1) % nxC,     y % nyC] + \
                          gameState[(x+1) % nxC,     y % nyC] + \
                          gameState[(x-1) % nxC, (y+1) % nyC] + \
                          gameState[x     % nxC, (y+1) % nyC] + \
                          gameState[(x+1) % nxC, (y+1) % nyC]

                # Regla 1: Una célula muerta con exactamente 3 vecinas vivas, revive
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1

                # Regal 2: Una célula viva con menos de 2 o más de 3 vecinas vivas, muere
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

            #Polígono de cada celda
            poly = [
                (x     * dimcW, y     * dimcH),
                ((x+1) * dimcW, y     * dimcH),
                ((x+1) * dimcW, (y+1) * dimcH),
                (x     * dimcW, (y+1) * dimcH)
            ]

            #Dibujo de la celda
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128,128,128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255,255,255), poly, 0)

    #Actualizando el juego
    gameState = np.copy(newGameState)

    pygame.display.flip()


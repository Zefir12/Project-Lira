from functions import *
import decimal

pygame.init()
pygame.font.init()
obraz = pygame.display.set_mode([900, 900])


def losowando(frequency, sizex, sizey, mapseed=1, offsetx=0, offsety=0):
    value = []
    gen = OpenSimplex(seed=mapseed)
    for y in range(sizex):
        value.append([0] * sizey)
        for x in range(sizey):
            nx = (x + offsetx) / sizex
            ny = (y + offsety) / sizey
            value[y][x] = [noise(frequency * nx, frequency * ny, gen),
                           noise(frequency/8 * nx, frequency/8 * ny, gen)]
    return value

map = losowando(40, 400, 400)
rozmiar = 2

while True:
    mouse = pygame.mouse.get_pos()
    redraw_game(0, 0, 0, obraz)
    #pygame.draw.line(obraz, [0, 180, 0], [0,0], [900,900], 60)
    i, ii = 0, 0

    for t1 in map:
        for value in t1:
            if value[0] < 0.13:
                pygame.draw.rect(obraz, [2, 0, 200], [i*rozmiar, ii*rozmiar, rozmiar, rozmiar])
            ii += 1
        i += 1
        ii = 0
    off()
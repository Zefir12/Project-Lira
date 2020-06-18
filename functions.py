import pygame
import sys
from opensimplex import OpenSimplex


def noise(nx, ny, gen):
    return gen.noise2d(nx, ny) / 2.0 + 0.5


def losowando(frequency, sizex, sizey, mapseed=1, offsetx=0, offsety=0):
    value = []
    gen = OpenSimplex(seed=mapseed)
    for y in range(sizex):
        value.append([0] * sizey)
        for x in range(sizey):
            nx = (x + offsetx) / sizex
            ny = (y + offsety) / sizey
            value[y][x] = noise(frequency * nx, frequency * ny, gen)
    return value


def sztuczny_monitor(wymiar_x, wymiar_y, obraz, map, ekran, multer):
    for bx in range(round_up(wymiar_x/(8*map.scale))+2):
        for by in range(round_up(wymiar_y/(8*map.scale))+2):
            position = (-(bx + round_up(map.OfPo[0]/(8*map.scale))) + round_up(wymiar_x/(8*map.scale) + (ekran[0] - wymiar_x)/(16*map.scale)),
                        -(by + round_up(map.OfPo[1]/(8*map.scale))) + round_up(wymiar_y/(8*map.scale) + (ekran[1] - wymiar_y)/(16*map.scale)))
            if position in map.chunklist:
                map.chunklist[position].draw()
                map.chunklist[position].draw_shade(ekran, multer)
                map.chunklist[position].draw_small_squares()
    pygame.draw.rect(obraz, [200, 0, 200], [(ekran[0] - wymiar_x)/2, (ekran[1] - wymiar_y)/2, wymiar_x, wymiar_y], 5)


def napisy(co, x, y, czcionka, obraz, kolor=(0, 0, 0)):
    nazwa = str(co)
    kolor_napisu = kolor
    label2 = czcionka.render(nazwa, 1, kolor_napisu)
    obraz.blit(label2, [x, y])


def check_distance_between_rects(rect1, rect2):
    prawo = rect2[0] - (rect1[0] + rect1[2])
    lewo = rect1[0] - (rect2[0] + rect2[2])
    dol = rect2[1] - (rect1[1] + rect1[3])
    gora = rect1[1] - (rect2[1] + rect2[3])

    return [prawo, lewo, dol, gora]


def redraw_game(r, g, b, obraz, image=False, x=0, y=0):
    if image is False:
        pygame.Surface.fill(obraz, [r, g, b])
    else:
        obraz.blit(image, [x, y])


def off():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
    pygame.display.flip()
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        return False
    else:
        return True


def round_up(number):
    res = round(number)
    if number - res == 0:
        return res
    elif number - res > 0:
        return res + 1
    else:
        return res


def switch(value):
    if value:
        return False
    else:
        return True


def moving(x, y, speed):
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        x += speed
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        x -= speed
    if pygame.key.get_pressed()[pygame.K_UP]:
        y += speed
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        y -= speed
    return x, y
from functions import *
from map import Map
import pickle
from config import Config as cfg
from client import Client
import random
import time
from smallSquare import SmallSquare
import json
import os.path
from os import path

user = 'MapViever'
color = [random.randint(0, 250), 200, 80]

client = Client(user, "192.168.0.5")
client.connect()

stgs = cfg['Settings']
rendr = cfg['Rendering']
devOp = cfg['developerOptions']

map = Map('Land', 0, 0)
map.users_visible_chunks[user] = []

pygame.init()
pygame.font.init()
pygame.display.set_caption(f'{user}')
clock = pygame.time.Clock()
flags = pygame.RESIZABLE
obraz = pygame.display.set_mode([stgs['EkranWidth'], stgs['EkranHeigth']], flags)
czcionka = pygame.font.Font("Czcionki/Montserrat-ExtraBold.otf", 10)
czcionkaBIG = pygame.font.Font("Czcionki/Montserrat-ExtraBold.otf", 40)


ekran = [stgs['EkranWidth'], stgs['EkranHeigth']]
instructions = None
ofpo = [0, 0]
scale = 30
frames = 0
top_fps = 0
map_holding = False
tempMAPoffset = 0
a = time.time()
back = pygame.Surface(ekran)
pygame.Surface.fill(back, [10, 10, 50])
back = back.convert()


while True:
    obraz.blit(back, [0, 0])
    #obraz.fill([10, 10, 50])
    clock.tick(60)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    executable = {'id': client.id[0], 'name': user, 'mouse': mouse, 'color': color, 'map_scale': scale, 'ofpo': ofpo, 'orders': {'create_chunk': [], 'load_chunk': [], "add_tree": []}, 'send_chunks': []}
    position = (round_up(((mouse[0] - ofpo[0])/(8*scale))-1), round_up(((mouse[1] - ofpo[1])/(8*scale))-1))
    pointer = (round_up(((mouse[0] - ofpo[0]) / scale) - 1) - (position[0] * 8), round_up(((mouse[1] - ofpo[1]) / scale) - 1) - (position[1] * 8))
    small_pointer = (round_up(((mouse[0] - ofpo[0]) / (scale / 4)) - 1) - (position[0] * 32) - (pointer[0] * 4), round_up(((mouse[1] - ofpo[1]) / (scale / 4)) - 1) - (position[1] * 32) - (pointer[1] * 4))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.ACTIVEEVENT:
            pass
        if event.type == pygame.VIDEORESIZE:
            stgs['EkranHigh'] = event.h
            stgs['EkranWidth'] = event.w
            ekran = [stgs['EkranWidth'], stgs['EkranHigh']]
            obraz = pygame.display.set_mode([stgs['EkranWidth'], stgs['EkranHigh']], flags)
            back = pygame.Surface(ekran)
            pygame.Surface.fill(back, [10, 10, 50])
            back = back.convert()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 5 and scale > 1:
                scale -= 1
                map.update_scales(scale)
                map.find_chunks_visible_on_monitor(ekran, user, ofpo, scale)
                map.update_ofpos_visible_on_monitor(ofpo, user)
                map.update_squares_positions_visible_on_monitor(user)
                map.update_squares_if_visible_on_monitor(ekran, devOp['small_squares_optimalisation'], user)
                map.update_all_small_squares_positions_visible_on_monitor(user)

            if event.button == 4:
                scale += 1
                map.update_scales(scale)
                ofpo[0] = ofpo[0] + (stgs['EkranWidth']/2 - mouse[0])/2
                ofpo[1] = ofpo[1] + (stgs['EkranHigh'] / 2 - mouse[1])/2
                map.find_chunks_visible_on_monitor(ekran, user, ofpo, scale)
                map.update_ofpos_visible_on_monitor(ofpo, user)
                map.update_squares_positions_visible_on_monitor(user)
                map.update_squares_if_visible_on_monitor(ekran, devOp['small_squares_optimalisation'], user)
                map.update_all_small_squares_positions_visible_on_monitor(user)

            if event.button == 1:
                if position not in map.chunklist:
                    executable['orders']['load_chunk'].append(position)

            if event.button == 3:
                map_holding = True
                tempMAPoffset = [ofpo[0] - mouse[0], ofpo[1] - mouse[1]]

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                map_holding = False

        if event.type == pygame.KEYDOWN:
            print(event)
            if event.unicode == 'm':
                rendr['drawterrain'] = switch(rendr['drawterrain'])
            if event.key == 292:
                if flags == pygame.RESIZABLE | pygame.FULLSCREEN:
                    flags = pygame.RESIZABLE
                else:
                    flags = pygame.RESIZABLE | pygame.FULLSCREEN
                obraz = pygame.display.set_mode([stgs['EkranWidth'], stgs['EkranHigh']], flags)
            if event.unicode == 'v':
                map.visualize_chunks()
                rendr['shadow_depth'] += 1
            if event.unicode == 'f':
                map.stabilize_every_chunk_v2()
            if event.unicode == 'd':
                devOp['splaszcz_drzewa'] = switch(devOp['splaszcz_drzewa'])
            if event.unicode == 'q':
                devOp['small_squares_optimalisation'] = switch(devOp['small_squares_optimalisation'])
            if event.unicode == 'n':
                rendr['drawshades'] = switch(rendr['drawshades'])
            if event.unicode == 'x':
               devOp['map_spawning_Viever'] = switch(devOp['map_spawning_Viever'])
            if event.unicode == 'j':
                devOp['growing_trees'] = switch(devOp['growing_trees'])

    if map_holding:
        ofpo = [tempMAPoffset[0] + mouse[0], tempMAPoffset[1] + mouse[1]]
        map.find_chunks_visible_on_monitor(ekran, user, ofpo, scale)
        map.update_ofpos_visible_on_monitor(ofpo, user)
        map.update_squares_positions_visible_on_monitor(user)
        map.update_squares_if_visible_on_monitor(ekran, devOp['small_squares_optimalisation'], user)
        map.update_all_small_squares_positions_visible_on_monitor(user)

    if rendr['drawshades']:
        map.draw_chunks_shades_visible_on_monitor(ekran, user, rendr['shadow_depth'])

    if rendr['drawterrain']:
        if scale == 1:
            map.draw_chunks_visualization_visible_on_monitor(user)
        else:
            map.draw_chunks_visible_on_monitor(user)
        if scale >= 4:
            map.draw_small_squares_visible_on_monitor(user)
            map.update_all_small_squares_positions_visible_on_monitor(user)

    if devOp['highlight_chunk']:
        if position in map.chunklist:
            map.chunklist[position].draw_chunk_border()
            if pointer in map.chunklist[position].square_table:
                map.chunklist[position].square_table[pointer].draw_square_border()

    if devOp['growing_trees']:
        lista_trees = map.growing_trees()
        for tree in lista_trees:
            if tree[0] in map.chunklist:
                if tree[1] in map.chunklist[tree[0]].square_table:
                    if tree[2] in map.chunklist[tree[0]].square_table[tree[1]].small_squares:
                        new_tree = (tree[2][0] + random.choice([-1, 0, 1]), tree[2][1] + random.choice([-1, 0, 1]))
                        if new_tree not in map.chunklist[tree[0]].square_table[tree[1]].small_squares:
                            licznik = 0
                            for x in range(0, 3):
                                for y in range(0, 3):
                                    if (x-1, y-1) in map.chunklist[tree[0]].square_table[tree[1]].small_squares:
                                        licznik += 1
                            if licznik < 2:
                                executable['orders']['add_tree'].append([tree[0], tree[1], new_tree])
                            if licznik >= 2:
                                if random.choice([True]):
                                    map.chunklist[tree[0]].square_table[tree[1]].small_squares.pop(tree[2])

    if rendr['drawsmallshades']:
        if scale >= 4:
            if not devOp['splaszcz_drzewa']:
                map.draw_small_squares_shade_visible_on_monitor(ekran, 0.8, user)
                map.draw_small_squares_shade_top_visible_on_monitor(user)

    if devOp['id-squares-visible']:
        map.draw_squares_idds_visible_on_monitor(ofpo, czcionka, user)
    if devOp['draw-chunk-borders']:
        map.draw_chunk_borders_visible_on_monitor(user)
    if devOp['highlight_chunk']:
        if position in map.chunklist:
            if pointer in map.chunklist[position].square_table:
                if small_pointer in map.chunklist[position].square_table[pointer].small_squares:
                    map.chunklist[position].square_table[pointer].small_squares[small_pointer].draw_tree_outline(ekran, 0.8)
                    map.chunklist[position].square_table[pointer].small_squares[small_pointer].draw_small_square_border()
                    if click[0]:
                        map.chunklist[position].square_table[pointer].small_squares[small_pointer].value2 *= 1.7
                    if click[2]:
                        map.chunklist[position].square_table[pointer].small_squares[small_pointer].value2 *= 0.7
                else:
                    if click[0]:
                        executable['orders']['add_tree'].append([position, pointer, small_pointer])

    if devOp['sztuczny_monitor']:
        sztuczny_monitor(900, 900, obraz, map, ekran, rendr['shadow_depth'])
    if devOp['show_fps']:
        if a - time.time() <= - 0.5:
            a = time.time()
            top_fps = frames*2
            frames = 0
        else:
            frames += 1
        napisy(top_fps, 0, 0, czcionkaBIG, obraz, kolor=(200, 0, 0))

    if devOp['show_ekran_sectors']:
        pygame.draw.line(obraz, [200, 0, 0], [ekran[0]/2, 0], [ekran[0]/2, ekran[1]])
        pygame.draw.line(obraz, [200, 0, 0], [0, ekran[1]/2], [ekran[0], ekran[1]/2])

    if instructions is not None:
        for cc in instructions:
            if 'mouse' in instructions[int(cc)]:
                x_y = instructions[int(cc)]['mouse']
                ofpox = instructions[int(cc)]['ofpo']
                if 'color' in instructions[int(cc)]:
                    if instructions[int(cc)]['id'] != client.id[0]:
                        pygame.draw.circle(obraz, instructions[int(cc)]['color'], [x_y[0] + int(ofpo[0]-ofpox[0]), x_y[1] + int(ofpo[1]-ofpox[1])], int(2*(instructions[int(cc)]['map_scale']+3)), 3)
                    else:
                        pygame.draw.circle(obraz, [255, 0, 0], [mouse[0], mouse[1]], int(2 * (scale + 3)), 3)
            if 'orders' in instructions[int(cc)]:
                if len(instructions[int(cc)]['send_chunks']) > 0:
                    for chunk in instructions[int(cc)]['send_chunks']:
                        if (chunk['x'], chunk['y']) not in map.chunklist:
                                map.chunklist[(chunk['x'], chunk['y'])] = map.load_chunk(chunk, ofpo, obraz, scale)
                                map.stabilize_chunk((chunk['x'], chunk['y']))
                                map.find_chunks_visible_on_monitor(ekran, user, ofpo, scale)
                                map.update_ofpos_visible_on_monitor(ofpo, user)
                                map.update_squares_positions_visible_on_monitor(user)
                if len(instructions[int(cc)]["orders"]['add_tree']) > 0:
                    for tree in instructions[int(cc)]["orders"]['add_tree']:
                        if tree[0] in map.chunklist:
                            map.chunklist[tree[0]].square_table[tree[1]].small_squares[tree[2]] = SmallSquare(tree[2][0], tree[2][1], [random.randint(0, 100), round(0.5 * 80), round(0.5 * 25)], tree[1], tree[0], 0.5, random.randint(3, 6)/10)
                            map.chunklist[tree[0]].square_table[tree[1]].small_squares[tree[2]].scale = scale
                            map.chunklist[tree[0]].square_table[tree[1]].small_squares[tree[2]].obraz = obraz
                            map.chunklist[tree[0]].square_table[tree[1]].small_squares[tree[2]].rodzaj = 'Tree'
                            map.update_ofpos(ofpo)
                            map.update_scales(scale)
                            map.update_all_small_squares_positions_visible_on_monitor(user)

    pygame.display.update()
    instructions = client.send(pickle.dumps(executable), False)

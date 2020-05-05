from functions import *
from map import Map
import pickle
from config import ClientSettings
from client import Client
import random
import time


user = 'MapViever'
color = [random.randint(0, 250), 200, 80]

CS = ClientSettings()
client = Client(user, "192.168.0.7")
client.connect()


pygame.init()
pygame.font.init()
pygame.display.set_caption(u'Map Viever')
clock = pygame.time.Clock()
flags = pygame.RESIZABLE
obraz = pygame.display.set_mode([CS.EkranWidth, CS.EkranHigh], flags)
czcionka = pygame.font.Font("Czcionki/Montserrat-ExtraBold.otf", 10)
czcionkaBIG = pygame.font.Font("Czcionki/Montserrat-ExtraBold.otf", 40)


map = Map('Land', 0)
map.OfPo = [CS.EkranWidth/2, CS.EkranHigh/2]
ekran = [CS.EkranWidth, CS.EkranHigh]
instructions = None
frames = 0
top_fps = 0
a = time.time()
back = pygame.Surface((ekran))
pygame.Surface.fill(back, [0, 0, 0])
back = back.convert()

while True:
    mouse = pygame.mouse.get_pos()
    executable = {'id': client.id[0], 'name': user, 'mouse': mouse, 'color': color, 'map_scale': map.scale, 'ofpo': map.OfPo, 'orders': {'create_chunk': [], 'create_forest': []}}
    #clock.tick(60)
    position = (round_up(((mouse[0] - map.OfPo[0])/(8*map.scale))-1), round_up(((mouse[1] - map.OfPo[1])/(8*map.scale))-1))
    pointer = (round_up(((mouse[0] - map.OfPo[0]) / map.scale) - 1) - (position[0] * 8),
               round_up(((mouse[1] - map.OfPo[1]) / map.scale) - 1) - (position[1] * 8))
    small_pointer = (round_up(((mouse[0] - map.OfPo[0]) / (map.scale / 4)) - 1) - (position[0] * 32) - (pointer[0] * 4),
                     round_up(((mouse[1] - map.OfPo[1]) / (map.scale / 4)) - 1) - (position[1] * 32) - (pointer[1] * 4))

    obraz.blit(back, [0, 0])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.ACTIVEEVENT:
            print(event)
        if event.type == pygame.VIDEORESIZE:
            CS.EkranHigh = event.h
            CS.EkranWidth = event.w
            ekran = [CS.EkranWidth, CS.EkranHigh]
            obraz = pygame.display.set_mode([CS.EkranWidth, CS.EkranHigh], flags)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 5 and map.scale > 1:
                map.scale -= 1
                map.update_scales(map.scale)
                map.find_chunks_visible_on_monitor(ekran, user)
                map.update_ofpos_visible_on_monitor(map.OfPo, user)
                map.update_squares_positions_visible_on_monitor(user)
                map.update_squares_if_visible_on_monitor(ekran,
                                                         CS.developerOptions['small_squares_optimalisation'], user)

            if event.button == 4:
                map.scale += 1
                map.update_scales(map.scale)
                map.OfPo[0] = map.OfPo[0] + (CS.EkranWidth/2 - mouse[0])/2
                map.OfPo[1] = map.OfPo[1] + (CS.EkranHigh / 2 - mouse[1])/2
                map.find_chunks_visible_on_monitor(ekran, user)
                map.update_ofpos_visible_on_monitor(map.OfPo, user)
                map.update_squares_positions_visible_on_monitor(user)
                map.update_squares_if_visible_on_monitor(ekran,
                                                         CS.developerOptions['small_squares_optimalisation'], user)

            if event.button == 1:
                if position not in map.chunklist:
                    executable['orders']['create_chunk'].append(position)
                else:
                    if CS.developerOptions['spawn_trees_on_click']:
                        executable['orders']['create_forest'].append(position)
                map.update_squares_if_visible_on_monitor(ekran, CS.developerOptions['small_squares_optimalisation'], user)


            if event.button == 3:
                CS.map_holding = True
                tempMAPoffset = [map.OfPo[0] - mouse[0], map.OfPo[1] - mouse[1]]

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                CS.map_holding = False

        if event.type == pygame.KEYDOWN:
            print(event)
            if event.unicode == 'm':
                CS.drawterrain = switch(CS.drawterrain)
            if event.key == 27:
                print(pygame.display.set_gamma(0.01, 0.2, 0.4))
                print('xd')
            if event.key == 292:
                if flags == pygame.RESIZABLE | pygame.FULLSCREEN:
                    flags = pygame.RESIZABLE
                else:
                    flags = pygame.RESIZABLE | pygame.FULLSCREEN
                obraz = pygame.display.set_mode([CS.EkranWidth, CS.EkranHigh], flags)
            if event.unicode == 'v':
                map.visualize_chunks()
            if event.unicode == 'f':
                map.stabilize_every_chunk_v2()
            if event.unicode == 'd':
                CS.developerOptions['splaszcz_drzewa'] = switch(CS.developerOptions['splaszcz_drzewa'])
            if event.unicode == 'q':
                CS.developerOptions['small_squares_optimalisation'] = switch(CS.developerOptions['small_squares_optimalisation'])
            if event.unicode == 'n':
                CS.drawshades = switch(CS.drawshades)
            if event.unicode == 'x':
                CS.developerOptions['map_spawning_Viever'] = switch(CS.developerOptions['map_spawning_Viever'])

    if CS.map_holding:
        map.OfPo = [tempMAPoffset[0] + mouse[0], tempMAPoffset[1] + mouse[1]]
        map.find_chunks_visible_on_monitor(ekran, user)
        map.update_ofpos_visible_on_monitor(map.OfPo, user)
        map.update_squares_positions_visible_on_monitor(user)
        map.update_squares_if_visible_on_monitor(ekran, CS.developerOptions['small_squares_optimalisation'], user)
        map.update_all_small_squares_positions_visible_on_monitor(user)

    if CS.drawshades:
        map.draw_chunks_shades_visible_on_monitor(ekran, user, CS.shadow_depth)

    if CS.drawterrain:
        if map.scale == 1:
            map.draw_chunks_visualization_visible_on_monitor(user)
        else:
            map.draw_chunks_visible_on_monitor(user)
        if map.scale >= 4:
            map.draw_small_squares_visible_on_monitor(user)
            if CS.developerOptions['splaszcz_drzewa']:
                map.draw_small_squares_visible_on_monitor(user)
            map.update_all_small_squares_positions_visible_on_monitor(user)

    if CS.developerOptions['highlight_chunk']:
        if position in map.chunklist:
            map.chunklist[position].draw_chunk_border()
            if pointer in map.chunklist[position].square_table:
                map.chunklist[position].square_table[pointer].draw_square_border()

    if CS.drawsmallshades:
        if map.scale >= 4:
            if not CS.developerOptions['splaszcz_drzewa']:
                map.draw_small_squares_shade_visible_on_monitor(ekran, 0.8, user)
                map.draw_small_squares_shade_top_visible_on_monitor(user)

    if CS.developerOptions['id-squares-visible']:
        map.draw_squares_idds_visible_on_monitor(map.OfPo, czcionka, user)
    if CS.developerOptions['draw-chunk-borders']:
        map.draw_chunk_borders_visible_on_monitor(user)
    if CS.developerOptions['highlight_chunk']:
        if position in map.chunklist:
            if pointer in map.chunklist[position].square_table:
                if small_pointer in map.chunklist[position].square_table[pointer].small_squares:
                    map.chunklist[position].square_table[pointer].small_squares[small_pointer].draw_tree_outline(ekran, 0.8)
                    map.chunklist[position].square_table[pointer].small_squares[small_pointer].draw_small_square_border()
    if CS.developerOptions['sztuczny_monitor']:
        sztuczny_monitor(900, 900, obraz, map, ekran, CS.shadow_depth)
    if CS.developerOptions['show_fps']:
        if a - time.time() <= - 0.5:
            a = time.time()
            top_fps = frames*2
            frames = 0
        else:
            frames += 1
        napisy(top_fps, 0, 0, czcionkaBIG, obraz, kolor=(200, 0, 0))

    if CS.developerOptions['show_ekran_sectors']:
        pygame.draw.line(obraz, [200, 0, 0], [ekran[0]/2, 0], [ekran[0]/2, ekran[1]])
        pygame.draw.line(obraz, [200, 0, 0], [0, ekran[1]/2], [ekran[0], ekran[1]/2])

    if instructions is not None:
        for cc in instructions:
            if 'mouse' in instructions[int(cc)]:
                x_y = instructions[int(cc)]['mouse']
                ofpo = instructions[int(cc)]['ofpo']
                if 'color' in instructions[int(cc)]:
                    if instructions[int(cc)]['id'] != client.id[0]:
                        pygame.draw.circle(obraz, instructions[int(cc)]['color'], [x_y[0] + int(map.OfPo[0]-ofpo[0]), x_y[1] + int(map.OfPo[1]-ofpo[1])], int(2*(instructions[int(cc)]['map_scale']+3)), 3)
                    else:
                        pygame.draw.circle(obraz, [255, 0, 0], [mouse[0], mouse[1]], int(2 * (map.scale + 3)), 3)
            if 'orders' in instructions[int(cc)]:
                if len(instructions[int(cc)]['orders']['create_chunk']) > 0:
                    for position in instructions[int(cc)]['orders']['create_chunk']:
                        if position not in map.chunklist:
                            map.chunklist[position] = map.create_chunk(position[0], position[1], position, obraz)
                            map.chunklist[position].update_obraz(obraz)
                            map.stabilize_chunk(position)
                            map.find_chunks_visible_on_monitor(ekran, user)
                            map.update_ofpos_visible_on_monitor(map.OfPo, user)
                            map.update_squares_positions_visible_on_monitor(user)
                if len(instructions[int(cc)]['orders']['create_forest']) > 0:
                    for position in instructions[int(cc)]['orders']['create_forest']:
                        if position in map.chunklist:
                            for b in map.chunklist[position].square_table:
                                map.chunklist[position].square_table[b].create_small_squares(obraz)
                            map.find_chunks_visible_on_monitor(ekran, user)
                            map.update_ofpos_visible_on_monitor(map.OfPo, user)
                            map.update_squares_positions_visible_on_monitor(user)

    pygame.display.update()
    instructions = client.send(pickle.dumps(executable), False)

from functions import *
from map import Map
import pickle
from config import ClientSettings
from client import Client

user = 'MapViever'
color = [20, 200, 80]

CS = ClientSettings()



pygame.init()
pygame.font.init()
pygame.display.set_caption(u'Map Viever')
clock = pygame.time.Clock()
obraz = pygame.display.set_mode([CS.EkranWidth, CS.EkranHigh])
czcionka = pygame.font.Font("Czcionki/Montserrat-ExtraBold.otf", 10)


map = Map('Land', 0)
map.OfPo = [CS.EkranWidth/2, CS.EkranHigh/2]
ekran = [CS.EkranWidth, CS.EkranHigh]




while True:
    mouse = pygame.mouse.get_pos()
    clock.tick(60)
    position = (round_up(((mouse[0] - map.OfPo[0])/(8*map.scale))-1), round_up(((mouse[1] - map.OfPo[1])/(8*map.scale))-1))
    redraw_game(0, 30, 60, obraz)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 5 and map.scale > 1:
                map.scale -= 1
                map.update_scales(map.scale)
                map.find_chunks_visible_on_monitor(ekran, user)
                map.update_ofpos_visible_on_monitor(map.OfPo, user)
                map.update_squares_positions_visible_on_monitor(user)

            if event.button == 4:
                map.scale += 1
                map.update_scales(map.scale)
                map.OfPo[0] = map.OfPo[0] + (CS.EkranWidth/2 - mouse[0])/2
                map.OfPo[1] = map.OfPo[1] + (CS.EkranHigh / 2 - mouse[1])/2
                map.find_chunks_visible_on_monitor(ekran, user)
                map.update_ofpos_visible_on_monitor(map.OfPo, user)
                map.update_squares_positions_visible_on_monitor(user)

            if event.button == 1:
                if position not in map.chunklist:
                    map.chunklist[position] = map.create_chunk(position[0], position[1], position, obraz)
                    map.chunklist[position].update_obraz(obraz)
                    map.stabilize_chunk(position)
                    map.find_chunks_visible_on_monitor(ekran, user)
                    map.update_ofpos_visible_on_monitor(map.OfPo, user)
                    map.update_squares_positions_visible_on_monitor(user)
                else:
                    for b in map.chunklist[position].square_table:
                        map.chunklist[position].square_table[b].create_small_squares(obraz)
                    map.find_chunks_visible_on_monitor(ekran, user)
                    map.update_ofpos_visible_on_monitor(map.OfPo, user)
                    map.update_squares_positions_visible_on_monitor(user)

            if event.button == 3:
                CS.map_holding = True
                tempMAPoffset = [map.OfPo[0] - mouse[0], map.OfPo[1] - mouse[1]]

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                CS.map_holding = False

        if event.type == pygame.KEYDOWN:
            if event.unicode == 'm':
                CS.drawterrain = switch(CS.drawterrain)
            if event.unicode == 'v':
                map.visualize_chunks()
            if event.unicode == 'f':
                map.stabilize_every_chunk_v2()
            if event.unicode == 'd':
                CS.developerOptions['splaszcz_drzewa'] = switch(CS.developerOptions['splaszcz_drzewa'])
            if event.unicode == 'n':
                CS.drawshades = switch(CS.drawshades)
            if event.unicode == 'x':
                CS.developerOptions['map_spawning_Viever'] = switch(CS.developerOptions['map_spawning_Viever'])

    if CS.map_holding:
        map.OfPo = [tempMAPoffset[0] + mouse[0], tempMAPoffset[1] + mouse[1]]
        map.find_chunks_visible_on_monitor(ekran, user)
        map.update_ofpos_visible_on_monitor(map.OfPo, user)
        map.update_squares_positions_visible_on_monitor(user)
        map.update_all_small_squares_positions_visible_on_monitor(user)

    if CS.drawshades:
        map.draw_chunks_shades_visible_on_monitor(ekran, user, CS.shadow_depth)

    if CS.drawterrain:
        if map.scale == 1:
            map.draw_chunks_visualization_visible_on_monitor(user)
        else:
            map.draw_chunks_visible_on_monitor(user)
        if map.scale >= 4:
            #map.draw_small_squares_visible_on_monitor(user)
            map.update_all_small_squares_positions_visible_on_monitor(user)

    if CS.drawsmallshades:
        if map.scale >= 4:

            map.draw_small_squares_shade_visible_on_monitor(ekran, 0.8, user)
            map.draw_small_squares_shade_top_visible_on_monitor(user)

    if CS.developerOptions['map_spawning_Viever']:
        pygame.draw.circle(obraz, [170, 20, 20], [mouse[0], mouse[1]], 30*map.scale, 3)
        for b in range(16):
            b -= 8
            for bb in range(16):
                bb -= 8
                if (position[0] + b, position[1] + bb) not in map.chunklist:
                    map.chunklist[(position[0] + b, position[1] + bb)] = map.create_chunk(position[0] + b, position[1] + bb, [position[0] + b, position[1] + bb])
                    map.stabilize_chunk((position[0] + b, position[1] + bb))
                    map.chunklist[position].update_obraz(obraz)
        map.visualize_chunks()
        map.find_chunks_visible_on_monitor(ekran, user)
        map.update_ofpos_visible_on_monitor(map.OfPo, user)
        map.update_squares_positions_visible_on_monitor(user)

    if CS.developerOptions['id-squares-visible']:
        map.draw_squares_idds_visible_on_monitor(map.OfPo, czcionka, user)
    if CS.developerOptions['draw-chunk-borders']:
        map.draw_chunk_borders_visible_on_monitor(user)
    if CS.developerOptions['highlight_chunk']:
        if position in map.chunklist:
            map.chunklist[position].draw_chunk_border()
    if CS.developerOptions['sztuczny_monitor']:
        sztuczny_monitor(900, 900, obraz, map, ekran, CS.shadow_depth)
    pygame.display.flip()


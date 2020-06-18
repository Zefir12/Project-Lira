import pygame
from functions import napisy
from opensimplex import OpenSimplex
from chunk import Chunk
from square import Square
from smallSquare import SmallSquare
from functions import noise, round_up
import json


class Map:
    def __init__(self, name, identyfikator, seed):
        self.name = name
        self.identyfikator = identyfikator
        self.chunklist = {}
        self.generated_chunks = []
        self.chunks_saved_into_files = []
        self.map_seed = seed
        self.users_visible_chunks = {}
        self.players = {}

    def create_chunk(self, position_x, position_y, frequency=1, size_x=8, size_y=8):
        chunk = Chunk(position_x, position_y)
        gen = OpenSimplex(seed=self.map_seed)
        for y in range(size_x):
            for x in range(size_y):
                nx = (x + (position_x * size_x)) / size_x
                ny = (y + (position_y * size_y)) / size_y
                value = noise(frequency * nx, frequency * ny, gen) * 0.1
                value += noise(frequency * nx / 9, frequency * ny / 9, gen) * 0.6
                value += noise(frequency * nx / 3, frequency * ny / 3, gen) * 0.3
                value = round(value, 4)
                if value < 0.5:
                    chunk.square_table[(x, y)] = Square(x, y, [round(value * 25), round(value * 255), round(value * 25)], (position_x, position_y), value)
                    for yy in range(int(size_x/2)):
                        for xx in range(int(size_y/2)):
                            nxx = (xx/4 + (position_x * size_x) + (x * size_x/8)) / size_x
                            nyy = (yy/4 + (position_y * size_y) + (y * size_y/8)) / size_y
                            valuee = noise(frequency/7 * nxx, frequency/7 * nyy, gen)*0.7
                            valuee += noise(frequency * nxx, frequency*3 * nyy, gen)*0.2
                            valuee += noise(frequency * 6 * nxx, frequency * nyy, gen) * 0.1
                            valuee += noise(frequency * 60 * nxx, frequency * 60 * nyy, gen) * 0.2
                            valuee += noise(frequency * 200 * nxx, frequency * 200 * nyy, gen) * 0.1

                            valuee = round(valuee, 4)
                            value2 = round(noise(frequency*200 * nxx, frequency*200 * nyy, gen), 4)
                            valuewater = round(noise(frequency/2 * nxx, frequency/2 * nyy, gen), 4)

                            if valuee < 0.5:
                                chunk.square_table[(x, y)].small_squares[(xx, yy)] = SmallSquare(xx, yy, [round(value * 25), round(valuee * 70) + 10, round(value * 25)], (x, y), (position_x, position_y), valuee, value2)
                                chunk.square_table[(x, y)].small_squares[(xx, yy)].rodzaj = 'Tree'
                            if valuewater < 0.26:
                                chunk.square_table[(x, y)].small_squares[(xx, yy)] = SmallSquare(xx, yy, [10, 10, round(250*valuewater)], (x, y), (position_x, position_y), valuee, value2)
                                chunk.square_table[(x, y)].small_squares[(xx, yy)].rodzaj = 'Water'
        return chunk

    def load_chunk(self, json, ofpo, obraz, scale):
        chunk = Chunk(json['x'], json['y'])
        chunk.ofpo = ofpo
        chunk.scale = scale
        chunk.obraz = obraz
        chunk.neighbourChunks = [(json['x'], json['y'] + 1), (json['x'] + 1, json['y']), (json['x'], json['y'] - 1), (json['x'] - 1, json['y'])]
        for idSq in json['s_t']:
            square = json['s_t'][idSq]
            chunk.square_table[(square['x'], square['y'])] = Square(square['x'], square['y'], square['c'], (json['x'], json['y']), square['v'])
            chunk.square_table[(square['x'], square['y'])].neighbours = square['n']
            chunk.square_table[(square['x'], square['y'])].ofpo = ofpo
            chunk.square_table[(square['x'], square['y'])].scale = scale
            chunk.square_table[(square['x'], square['y'])].obraz = obraz
            for idSm in square['s_s']:
                small = square['s_s'][idSm]
                chunk.square_table[(square['x'], square['y'])].small_squares[(small['x'], small['y'])] = SmallSquare(small['x'], small['y'], small['c'], (square['x'], square['y']), (json['x'], json['y']), small['v'], small['v2'])
                chunk.square_table[(square['x'], square['y'])].small_squares[(small['x'], small['y'])].rodzaj = small['r']
                chunk.square_table[(square['x'], square['y'])].small_squares[(small['x'], small['y'])].neighbours = small['n']
                chunk.square_table[(square['x'], square['y'])].small_squares[(small['x'], small['y'])].ofpo = ofpo
                chunk.square_table[(square['x'], square['y'])].small_squares[(small['x'], small['y'])].scale = scale
                chunk.square_table[(square['x'], square['y'])].small_squares[(small['x'], small['y'])].obraz = obraz
        return chunk

    def stabilize_chunk(self, ids):
        for b in self.chunklist[ids].square_table:
            if (b[0], b[1] + 1) in self.chunklist[ids].square_table:
                self.chunklist[ids].square_table[b].neighbours[0] = True
            if (b[0] + 1, b[1]) in self.chunklist[ids].square_table:
                self.chunklist[ids].square_table[b].neighbours[1] = True
            if (b[0], b[1] - 1) in self.chunklist[ids].square_table:
                self.chunklist[ids].square_table[b].neighbours[2] = True
            if (b[0] - 1, b[1]) in self.chunklist[ids].square_table:
                self.chunklist[ids].square_table[b].neighbours[3] = True

    def stabilize_chunk_v2(self, ids):
        for bro in self.chunklist[ids].neighbourChunks:
            if bro in self.chunklist:
                if (bro[0], bro[1]) == (ids[0], ids[1] + 1):
                    for b in range(8):
                        if (b, 0) in self.chunklist[bro].square_table and (b, 7) in self.chunklist[ids].square_table:
                            self.chunklist[bro].square_table[(b, 0)].neighbours[2] = True
                            self.chunklist[ids].square_table[(b, 7)].neighbours[0] = True
                if (bro[0], bro[1]) == (ids[0] + 1, ids[1]):
                    for b in range(8):
                        if (0, b) in self.chunklist[bro].square_table and (7, b) in self.chunklist[ids].square_table:
                            self.chunklist[bro].square_table[(0, b)].neighbours[3] = True
                            self.chunklist[ids].square_table[(7, b)].neighbours[1] = True

    def stabilize_every_chunk_v2(self):
        for b in self.chunklist:
            self.stabilize_chunk_v2(b)

    def update_scales(self, scale):
        for b in self.chunklist:
            self.chunklist[b].update_scale(scale)

    def update_ofpos(self, ofpo):
        for b in self.chunklist:
            self.chunklist[b].update_ofpo(ofpo)

    def update_squares_positions(self):
        for b in self.chunklist:
            self.chunklist[b].update_squares_positions()

    def find_chunks_visible_on_monitor(self, ekran, user, ofpo, scale):
        list_chunks = []
        for bx in range(round_up(ekran[0]/(8*scale))+1):
            for by in range(round_up(ekran[1]/(8*scale))+1):
                list_chunks.append((-(bx + round_up(ofpo[0]/(8*scale))) + round_up(ekran[0]/(8*scale)),
                                    -(by + round_up(ofpo[1]/(8*scale))) + round_up(ekran[1]/(8*scale))))
        self.users_visible_chunks[user] = list_chunks

    def update_scales_visible_on_monitor(self, scale, user):
        for position in self.users_visible_chunks[user]:
            if position in self.chunklist:
                self.chunklist[position].update_scale(scale)

    def update_ofpos_visible_on_monitor(self, ofpo, user):
        for position in self.users_visible_chunks[user]:
            if position in self.chunklist:
                self.chunklist[position].update_ofpo(ofpo)

    def update_squares_positions_visible_on_monitor(self, user):
        for position in self.users_visible_chunks[user]:
            if position in self.chunklist:
                self.chunklist[position].update_squares_positions()

    def update_squares_if_visible_on_monitor(self, ekran, switch, user):
        for position in self.users_visible_chunks[user]:
            if position in self.chunklist:
                self.chunklist[position].update_squares_visible_on_screen(ekran, switch)

    def draw_chunks_visible_on_monitor(self, user):
        for position in self.users_visible_chunks[user]:
            if position in self.chunklist:
                self.chunklist[position].draw()

    def draw_chunks_shades_visible_on_monitor(self, ekran, user, multer):
        for position in self.users_visible_chunks[user]:
            if position in self.chunklist:
                self.chunklist[position].draw_shade(ekran, multer)

    def draw_small_squares_shade_visible_on_monitor(self, ekran, multer, user):
        for position in self.users_visible_chunks[user]:
            if position in self.chunklist:
                self.chunklist[position].draw_small_squares_shade(ekran, multer)

    def draw_small_squares_shade_top_visible_on_monitor(self, user):
        for position in self.users_visible_chunks[user]:
            if position in self.chunklist:
                self.chunklist[position].draw_small_squares_shade_top()

    def visualize_chunks(self):
        for b in self.chunklist:
            if self.chunklist[b].chunk_visualization is None:
                self.chunklist[b].visualize_chunk()

    def draw_chunks_visualization_visible_on_monitor(self, user):
        for position in self.users_visible_chunks[user]:
            if position in self.chunklist:
                self.chunklist[position].draw_chunk_visualization()

    def draw_squares_idds_visible_on_monitor(self, ofpo, czcionka, user):
        for position in self.users_visible_chunks[user]:
            if position in self.chunklist:
                self.chunklist[position].draw_square_idd(ofpo, czcionka)

    def draw_chunk_borders_visible_on_monitor(self, user):
        for position in self.users_visible_chunks[user]:
            if position in self.chunklist:
                self.chunklist[position].draw_chunk_border()

    def draw_small_squares_visible_on_monitor(self, user):
        for position in self.users_visible_chunks[user]:
            if position in self.chunklist:
                self.chunklist[position].draw_small_squares()

    def update_all_small_squares_positions_visible_on_monitor(self, user):
        for position in self.users_visible_chunks[user]:
            if position in self.chunklist:
                self.chunklist[position].update_small_squares_positions()

    def growing_trees(self):
        lista_drzew = []
        for position in self.chunklist:
            for square in self.chunklist[position].square_table:
                for ssquare in self.chunklist[position].square_table[square].small_squares:
                    tree = self.chunklist[position].square_table[square].small_squares[ssquare].grow_tree()
                    if tree:
                        lista_drzew.append(tree)
        return lista_drzew


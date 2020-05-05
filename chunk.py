import pygame
from functions import napisy


class Chunk:
    def __init__(self, x, y, ids, scale, obraz):
        self.x = x
        self.y = y
        self.ids = ids
        self.square_table = {}
        self.stabilized = False
        self.chunk_visualization = None
        self.neighbourChunks = [(ids[0], ids[1] + 1), (ids[0] + 1, ids[1]), (ids[0], ids[1] - 1), (ids[0] - 1, ids[1])]
        self.scale = scale
        self.obraz = obraz
        self.ofpo = [0, 0]

    def update_obraz(self, obraz):
        self.obraz = obraz
        for b in self.square_table:
            self.square_table[b].update_obraz(obraz)

    def update_scale(self, scale):
        self.scale = scale
        for b in self.square_table:
            self.square_table[b].update_scale(scale)

    def update_ofpo(self, ofpo):
        self.ofpo = ofpo
        for b in self.square_table:
            self.square_table[b].update_ofpo(ofpo)

    def draw(self):
        for square in self.square_table:
            self.square_table[square].draw()

    def draw_shade(self, ekran, multer):
        for square in self.square_table:
            self.square_table[square].draw_shade(ekran, multer)

    def update_squares_visible_on_screen(self, ekran, switch):
        for square in self.square_table:
            self.square_table[square].update_visible_on_scrren(ekran, switch)

    def visualize_chunk(self):
        temp = 0
        if len(self.square_table) > 20:
            for b in self.square_table:
                temp += self.square_table[b].value
            color = temp/len(self.square_table)
            self.chunk_visualization = [20, color*255, 20]

    def draw_chunk_visualization(self):
        if self.chunk_visualization is not None:
            pygame.draw.rect(self.obraz, self.chunk_visualization, [(self.x * self.scale * 8) + self.ofpo[0], (self.y * self.scale * 8) + self.ofpo[1], self.scale * 8, self.scale * 8])

    def update_squares_positions(self):
        for b in self.square_table:
            self.square_table[b].update_position()

    def draw_chunk_border(self):
        pygame.draw.rect(self.obraz, [0, 0, 0], [(self.x * self.scale * 8) + self.ofpo[0], (self.y * self.scale * 8) + self.ofpo[1], self.scale * 8, self.scale * 8], 3)

    def draw_square_idd(self, ids, czcionka):
        for square in self.square_table:
            napisy(f'{self.square_table[square].idd}', (square[0]*self.scale) + (ids[0]*self.scale*8) + self.ofpo[0], (square[1]*self.scale) + (ids[1]*self.scale*8) + self.ofpo[1], czcionka, self.obraz)

    def draw_small_squares(self):
        for b in self.square_table:
            self.square_table[b].draw_small_squares()

    def update_small_squares_positions(self):
        for b in self.square_table:
            self.square_table[b].update_small_squares_positions()

    def draw_small_squares_shade(self, ekran, multer):
        for b in self.square_table:
            self.square_table[b].draw_small_squares_shade(ekran, multer)

    def draw_small_squares_shade_top(self):
        for b in self.square_table:
            self.square_table[b].draw_small_squares_shade_top()

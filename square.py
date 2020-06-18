import pygame
from smallSquare import SmallSquare
import random


class Square:
    def __init__(self, x, y, color, idChunk, value):
        self.x = x
        self.y = y
        self.value = value
        self.color = color
        self.idSquare = (x, y)
        self.idChunk = idChunk
        self.neighbours = [False, False, False, False]
        self.have_shade = True
        self.part_of_screen = [0, 0]
        self.position = [0, 0]
        self.visible_on_the_scrreen = True
        self.scale = None
        self.obraz = None
        self.ofpo = [0, 0]
        self.small_squares = {}

    def save_square_into_json(self):
        sqtable = {}
        for small in self.small_squares:
            sqtable[str(small)] = self.small_squares[small].save_small_into_json()

        return {'x': self.x,
                'y': self.y,
                'v': self.value,
                'c': self.color,
                'n': self.neighbours,
                's_s': sqtable}

    def update_obraz(self, obraz):
        self.obraz = obraz
        for b in self.small_squares:
            self.small_squares[b].update_obraz(obraz)

    def update_scale(self, scale):
        self.scale = scale
        for b in self.small_squares:
            self.small_squares[b].update_scale(scale)

    def update_ofpo(self, ofpo):
        self.ofpo = ofpo
        for b in self.small_squares:
            self.small_squares[b].update_ofpo(ofpo)

    def update_position(self):
        self.position = [(self.x * self.scale) + (self.idChunk[0] * self.scale * 8) + self.ofpo[0], (self.y * self.scale) + (self.idChunk[1] * self.scale * 8) + self.ofpo[1]]

    def update_visible_on_scrren(self, ekran, switch):
        if 0 - self.scale < self.position[0] < ekran[0] + self.scale and 0 - self.scale < self.position[1] < ekran[1] + self.scale:
            self.visible_on_the_scrreen = True
        else:
            self.visible_on_the_scrreen = False
        if not switch:
            self.visible_on_the_scrreen = True

    def draw(self):
        if self.visible_on_the_scrreen:
            pygame.draw.rect(self.obraz, self.color, [self.position[0], self.position[1], self.scale, self.scale])

    def draw_shade(self, Ekran, multer):
        if self.visible_on_the_scrreen:
            if self.have_shade:
                self.have_shade = False
                for b in self.neighbours:
                    if b is False:
                        self.have_shade = True

            if self.have_shade:
                if (self.x * self.scale) + (self.idChunk[0] * self.scale * 8) + self.ofpo[0] < Ekran[0] / 2:
                    self.part_of_screen[0] = 0
                else:
                    self.part_of_screen[0] = 1
                if (self.y * self.scale) + (self.idChunk[1] * self.scale * 8) + self.ofpo[1] < Ekran[1] / 2:
                    self.part_of_screen[1] = 0
                else:
                    self.part_of_screen[1] = 1

                self.UDP = [self.position[0] + self.scale, self.position[1] + self.scale]
                self.UDL = [self.position[0], self.position[1] + self.scale]
                self.UGP = [self.position[0] + self.scale, self.position[1]]
                self.UGL = [self.position[0], self.position[1]]

                self.Mult = self.scale / (1 + (2 * multer))
                self.Dx = (self.x * self.Mult) + (self.idChunk[0] * self.Mult * 8) + (self.ofpo[0] + (Ekran[0] * multer))/(1 + (2 * multer))
                self.Dy = (self.y * self.Mult) + (self.idChunk[1] * self.Mult * 8) + (self.ofpo[1] + (Ekran[1] * multer))/(1 + (2 * multer))

                self.DDP = [self.Dx + self.Mult, self.Dy + self.Mult]
                self.DDL = [self.Dx, self.Dy + self.Mult]
                self.DGP = [self.Dx + self.Mult, self.Dy]
                self.DGL = [self.Dx, self.Dy]

                if self.part_of_screen[0] == 0:
                    if not self.neighbours[1]:
                        pygame.draw.polygon(self.obraz, [20, 30, 30], [self.UGP, self.DGP, self.DDP, self.UDP])
                    if self.part_of_screen[1] == 0:
                        if not self.neighbours[0]:
                            pygame.draw.polygon(self.obraz, [10, 20, 30], [self.UDL, self.UDP, self.DDP, self.DDL])
                    else:
                        if not self.neighbours[2]:
                            pygame.draw.polygon(self.obraz, [10, 20, 20], [self.UGP, self.DGP, self.DGL, self.UGL])
                else:
                    if not self.neighbours[3]:
                        pygame.draw.polygon(self.obraz, [4, 10, 4], [self.UGL, self.DGL, self.DDL, self.UDL])
                    if self.part_of_screen[1] == 0:
                        if not self.neighbours[0]:
                            pygame.draw.polygon(self.obraz, [10, 20, 30], [self.UDL, self.UDP, self.DDP, self.DDL])
                    else:
                        if not self.neighbours[2]:
                            pygame.draw.polygon(self.obraz, [10, 20, 20], [self.UGP, self.DGP, self.DGL, self.UGL])

    def draw_square_border(self):
        pygame.draw.rect(self.obraz, [0, 0, 0], [(self.x * self.scale) + (self.idChunk[0] * self.scale*8) + self.ofpo[0], (self.y * self.scale) + (self.idChunk[1] * self.scale*8) + self.ofpo[1], self.scale, self.scale], 2)

    def create_small_squares(self, obraz):
        for x in range(4):
            for y in range(4):
                    a = random.randint(0, 1024)
                    if a > 1000:
                        self.small_squares[(x, y)] = SmallSquare(x, y, [0, 40 + a-1000, 0], self.idSquare, self.idChunk, self.value, self.scale, self.obraz)
        self.update_obraz(obraz)

    def draw_small_square(self, idx):
        self.small_squares[idx].draw()

    def draw_small_squares(self):
        if self.visible_on_the_scrreen:
            for b in self.small_squares:
                self.draw_small_square(b)

    def update_small_square_position(self, idx):
        self.small_squares[idx].update_position()

    def update_small_squares_positions(self):
        if self.visible_on_the_scrreen:
            for b in self.small_squares:
                self.update_small_square_position(b)

    def draw_small_square_shade(self, idx, ekran, multer):
        self.small_squares[idx].draw_shade(ekran, multer)

    def draw_small_squares_shade(self, ekran, multer):
        if self.visible_on_the_scrreen:
            if self.visible_on_the_scrreen:
                for b in self.small_squares:
                    self.draw_small_square_shade(b, ekran, multer)

    def draw_small_square_shade_top(self, idx):
        self.small_squares[idx].draw_shade_top()

    def draw_small_squares_shade_top(self):
        if self.visible_on_the_scrreen:
            for b in self.small_squares:
                self.draw_small_square_shade_top(b)
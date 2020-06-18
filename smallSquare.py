import pygame


class SmallSquare:
    def __init__(self, x, y, color, idSquare, idChunk, value, value2):
        self.x = x
        self.y = y
        self.value = value
        self.value2 = value2
        self.rodzaj = 'Tree'
        self.color = color
        self.idSquare = idSquare
        self.idChunk = idChunk
        self.idSmall = (x, y)
        self.part_of_screen = [0, 0]
        self.neighbours = [False, False, False, False]
        self.have_shade = None
        self.position = [0, 0]
        self.scale = None
        self.ofpo = [0, 0]
        self.obraz = None
        self.rect = [0, 0, 0, 0]

    def save_small_into_json(self):
        return {'x': self.x,
                'y': self.y,
                'v': self.value,
                'v2': self.value2,
                'r': self.rodzaj,
                'c': self.color,
                'n': self.neighbours,}

    def update_obraz(self, obraz):
        self.obraz = obraz

    def update_scale(self, scale):
        self.scale = scale

    def update_ofpo(self, ofpo):
        self.ofpo = ofpo

    def update_position(self):
        self.position = [(self.x * self.scale/4) + (self.idSquare[0] * self.scale) + (self.idChunk[0] * self.scale*8) + self.ofpo[0],
                         (self.y * self.scale/4) + (self.idSquare[1] * self.scale) + (self.idChunk[1] * self.scale*8) + self.ofpo[1]]

    def draw(self):
        self.rect = [self.position[0], self.position[1], self.scale / 4 + 1, self.scale / 4 + 1]
        pygame.draw.rect(self.obraz, self.color, self.rect)

    def draw_shade(self, ekran, multer):
        if self.rodzaj == 'Tree':
            self.skala = (self.scale / 4) * (multer/4)
            self.Ux = self.position[0] + ((self.position[0] - (ekran[0]/2))/((200+2300*self.value2)/self.scale)) + self.skala/multer
            self.Uy = self.position[1] + ((self.position[1] - (ekran[1]/2))/((200+2300*self.value2)/self.scale)) + self.skala/multer
            self.UGL = [self.Ux, self.Uy]
            self.UGP = [self.Ux + self.skala*3, self.Uy]
            self.UDL = [self.Ux, self.Uy + self.skala*3]
            self.UDP = [self.Ux + self.skala*3, self.Uy + self.skala*3]
            self.DGL = [self.position[0], self.position[1]]
            self.DGP = [self.position[0] + self.scale/4, self.position[1]]
            self.DDL = [self.position[0], self.position[1] + self.scale/4]
            self.DDP = [self.position[0] + self.scale/4, self.position[1] + self.scale/4]

            if not self.Ux < self.position[0]:
                pygame.draw.polygon(self.obraz, [self.color[0], self.color[1] - 10, self.color[2]],
                                    [self.UGL, self.UDL, self.DDL, self.DGL])
            if not self.UGP[0] > self.DGP[0]:
                pygame.draw.polygon(self.obraz, [self.color[0] + 10, self.color[1] + 30, self.color[2] + 10],
                                    [self.UGP, self.UDP, self.DDP, self.DGP])
            if not self.Uy < self.position[1]:
                pygame.draw.polygon(self.obraz, [self.color[0], self.color[1], self.color[2]],
                                    [self.UGP, self.UGL, self.DGL, self.DGP])
            if not self.UDL[1] > self.DDL[1]:
                pygame.draw.polygon(self.obraz, [self.color[0], self.color[1], self.color[2]],
                                    [self.UDP, self.UDL, self.DDL, self.DDP])

    def draw_shade_top(self):
        if self.rodzaj == 'Tree':
            pygame.draw.polygon(self.obraz, [self.color[0] + 5, self.color[1] + 20, self.color[2] + 5], [self.UGP, self.UGL, self.UDL, self.UDP])

    def draw_small_square_border(self):
        pygame.draw.rect(self.obraz, [0, 0, 0], [self.position[0], self.position[1], self.scale/4, self.scale/4], 2)

    def draw_tree_outline(self, ekran, multer):
        if self.rodzaj == 'Tree':
            self.skala = (self.scale / 4) * (multer/4)
            self.Ux = self.position[0] + ((self.position[0] - (ekran[0]/2))/((200 + 2300*self.value2)/self.scale)) + self.skala/multer
            self.Uy = self.position[1] + ((self.position[1] - (ekran[1]/2))/((200 + 2300*self.value2)/self.scale)) + self.skala/multer
            self.UGL = [self.Ux, self.Uy]
            self.UGP = [self.Ux + self.skala*3, self.Uy]
            self.UDL = [self.Ux, self.Uy + self.skala*3]
            self.UDP = [self.Ux + self.skala*3, self.Uy + self.skala*3]
            self.DGL = [self.position[0], self.position[1]]
            self.DGP = [self.position[0] + self.scale/4, self.position[1]]
            self.DDL = [self.position[0], self.position[1] + self.scale/4]
            self.DDP = [self.position[0] + self.scale/4, self.position[1] + self.scale/4]
            pygame.draw.polygon(self.obraz, [0, 0, 0], [self.UGP, self.UGL, self.UDL, self.UDP], 2)
            pygame.draw.line(self.obraz, [0, 0, 0], self.UGP, self.DGP, 2)
            pygame.draw.line(self.obraz, [0, 0, 0], self.UGL, self.DGL, 2)
            pygame.draw.line(self.obraz, [0, 0, 0], self.UDL, self.DDL, 2)
            pygame.draw.line(self.obraz, [0, 0, 0], self.UDP, self.DDP, 2)

    def grow_tree(self):
        if self.rodzaj == "Tree":
            if self.value2 > 0.1:
                self.value2 *= 0.94
                return False
            else:
                self.value2 = 1
                return [self.idChunk, self.idSquare, self.idSmall]


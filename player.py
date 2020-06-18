import pygame
from functions import check_distance_between_rects as checkD


class Player:
    def __init__(self, id, name, color, game):
        self.position = [0, 0]
        self.id = id
        self.name = name
        self.eq = []
        self.health_bar = 100
        self.armor = 0
        self.speed = 1
        self.color = color
        self.scale = 1
        self.game = game
        self.moving = [0, 0, 0, 0]
        self.blocked_moving = [0, 0, 0, 0]
        self.close_surroundings = []
        self.rect = [self.game.ekran[0]/2 + self.game.ofpo[0] + self.position[0], self.game.ekran[1]/2 + self.game.ofpo[1]+ self.position[1], self.scale/6, self.scale/6]

    def draw(self):
        self.rect = [self.game.ekran[0]/2 + self.game.ofpo[0] + self.position[0], self.game.ekran[1]/2 + self.game.ofpo[1]+ self.position[1], self.scale/6, self.scale/6]
        pygame.draw.rect(self.game.obraz, self.color, self.rect)
        pygame.draw.rect(self.game.obraz, [0, 0, 0], self.rect, 2)

    def move(self):
        if self.moving[0] and not self.blocked_moving[0]:
            self.position[1] -= self.speed
        if self.moving[1] and not self.blocked_moving[1]:
            self.position[1] += self.speed
        if self.moving[2] and not self.blocked_moving[2]:
            self.position[0] += self.speed
        if self.moving[3] and not self.blocked_moving[3]:
            self.position[0] -= self.speed

    def block_movement(self):
        self.blocked_moving = [0, 0, 0, 0]
        for rect in self.close_surroundings:
            dst = checkD(self.rect, rect)
            if dst[2] < 0 and dst[3] < 0:
                if 0 <= dst[0] < 1.8:
                    self.blocked_moving[2] = 1
                if 0 <= dst[1] < 1.8:
                    self.blocked_moving[3] = 1
            if dst[0] < 0 and dst[1] < 0:
                if 0 <= dst[2] < 1.8:
                    self.blocked_moving[1] = 1
                if 0 <= dst[3] < 1.8:
                    self.blocked_moving[0] = 1

    def get_close_surroundings(self, chunklist):
        self.close_surroundings = []
        for chunk in chunklist:
            if chunk in self.game.map.chunklist:
                for square in self.game.map.chunklist[chunk].square_table:
                    for smalsquare in self.game.map.chunklist[chunk].square_table[square].small_squares:
                        self.close_surroundings.append(self.game.map.chunklist[chunk].square_table[square].small_squares[smalsquare].rect)

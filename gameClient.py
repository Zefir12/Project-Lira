from functions import *
from map import Map
import pickle
from player import Player
from client import Client
import random
import time


pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
pygame.display.set_caption(f'Project: Lira')


class GameClient:
    def __init__(self):
        self.user = 'Zefir'
        self.color = [random.randint(0, 250), 200, 80]
        self.client = Client(self.user, "192.168.0.5")
        self.client.connect()
        self.map = Map('Land', 0, 0)
        self.map.users_visible_chunks[self.user] = []
        self.ekran = [900, 900]
        self.obraz = pygame.display.set_mode(self.ekran, pygame.RESIZABLE)
        self.instructions = None
        self.ofpo = [0, 0]
        self.scale = 100
        self.back = pygame.Surface(self.ekran)
        self.running = True
        self.events = []
        self.mouse = [0, 0]
        self.click = []
        self.executable = None
        self.player = None
        self.players = []
        self.renderDistance = 2

    def refill_background(self):
        self.back = pygame.Surface(self.ekran)
        pygame.Surface.fill(self.back, [10, 10, 50])
        self.back = self.back.convert()

    def redraw_background(self):
        self.obraz.blit(self.back, [0, 0])

    def get_events(self):
        self.events = pygame.event.get()

    def get_mouse_info(self):
        self.mouse = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()

    def move_map_to_player(self):
        self.ofpo[0] = -self.player.position[0]
        self.ofpo[1] = -self.player.position[1]

    def create_executable(self):
        self.executable = {'id': self.client.id[0], 'name': self.user, 'mouse': self.mouse, 'color': self.color, 'map_scale': self.scale, 'ofpo': self.ofpo, 'pPosition': self.player.position, 'orders': {'create_chunk': [], 'load_chunk': []}, 'send_chunks': []}


game = GameClient()
game.refill_background()
game.player = Player(game.client.id[0], game.user, game.color, game)
game.player.scale = game.scale

while game.running:
    game.redraw_background()
    clock.tick(60)
    game.get_events()
    game.get_mouse_info()
    game.create_executable()
    game.player.move()
    game.move_map_to_player()
    if 1 in game.player.moving:
        game.map.update_scales(game.scale)
        game.map.find_chunks_visible_on_monitor(game.ekran, game.user, game.ofpo, game.scale)
        game.map.update_ofpos_visible_on_monitor(game.ofpo, game.user)
        game.map.update_squares_positions_visible_on_monitor(game.user)
        game.map.update_squares_if_visible_on_monitor(game.ekran, True, game.user)

    position = (round_up(((game.mouse[0] - game.ofpo[0]) / (8 * game.scale)) - 1), round_up(((game.mouse[1] - game.ofpo[1]) / (8 * game.scale)) - 1))
    player_pos = (round_up(((game.ekran[0]/2 - game.ofpo[0]) / (8 * game.scale)) - 1), round_up(((game.ekran[1]/2  - game.ofpo[1]) / (8 * game.scale)) - 1))

    for evt in game.events:
        if evt.type == pygame.QUIT:
            sys.exit(0)
        if evt.type == pygame.VIDEORESIZE:
            game.ekran = [evt.w, evt.h]
            game.obraz = pygame.display.set_mode(game.ekran, pygame.RESIZABLE)
            game.refill_background()
        if evt.type == pygame.KEYDOWN:
            if evt.key == 119:
                game.player.moving[0] = 1
            if evt.key == 115:
                game.player.moving[1] = 1
            if evt.key == 100:
                game.player.moving[2] = 1
            if evt.key == 97:
                game.player.moving[3] = 1
        if evt.type == pygame.KEYUP:
            if evt.key == 119:
                game.player.moving[0] = 0
            if evt.key == 115:
                game.player.moving[1] = 0
            if evt.key == 100:
                game.player.moving[2] = 0
            if evt.key == 97:
                game.player.moving[3] = 0
        if evt.type == pygame.MOUSEBUTTONDOWN:
            if evt.button == 1:
                if position not in game.map.chunklist:
                    game.executable['orders']['load_chunk'].append(position)
        for x in range(game.renderDistance):
            for y in range(game.renderDistance):
                pos = (player_pos[0] + x -1, player_pos[1] + y -1)
                if pos not in game.map.chunklist:
                    game.executable['orders']['load_chunk'].append(pos)
    game.map.draw_chunks_shades_visible_on_monitor(game.ekran, game.user, 0.2)
    game.map.draw_chunks_visible_on_monitor(game.user)
    game.map.draw_small_squares_visible_on_monitor(game.user)
    game.player.get_close_surroundings(game.map.users_visible_chunks[game.user])
    game.player.block_movement()
    game.player.draw()
    game.map.update_all_small_squares_positions_visible_on_monitor(game.user)

    if game.instructions is not None:
        for cc in game.instructions:
            if 'orders' in game.instructions[int(cc)]:
                if len(game.instructions[int(cc)]['send_chunks']) > 0:
                    for chunk in game.instructions[int(cc)]['send_chunks']:
                        if (chunk['x'], chunk['y']) not in game.map.chunklist:
                                game.map.chunklist[(chunk['x'], chunk['y'])] = game.map.load_chunk(chunk, game.ofpo, game.obraz, game.scale)
                                game.map.stabilize_chunk((chunk['x'], chunk['y']))
                                game.map.find_chunks_visible_on_monitor(game.ekran, game.user, game.ofpo, game.scale)
                                game.map.update_ofpos_visible_on_monitor(game.ofpo, game.user)
                                game.map.update_squares_positions_visible_on_monitor(game.user)
            if 'ofpo' in game.instructions[int(cc)]:
                if game.instructions[int(cc)]['id'] != game.client.id[0]:
                    ofpoxd = game.instructions[int(cc)]['ofpo']
                    ppos = game.instructions[int(cc)]['pPosition']
                    pygame.draw.rect(game.obraz, game.instructions[int(cc)]['color'], [(game.ekran[0] / 2) + ppos[0] + game.ofpo[0], (game.ekran[1] / 2) + ppos[1] + game.ofpo[1], game.scale / 6, game.scale / 6])
                    pygame.draw.rect(game.obraz, [0, 0, 0], [(game.ekran[0] / 2) + ppos[0] + game.ofpo[0], (game.ekran[1] / 2) + ppos[1] + game.ofpo[1], game.scale / 6, game.scale / 6], 2)

    game.map.draw_small_squares_shade_visible_on_monitor(game.ekran, 0.8, game.user)
    game.map.draw_small_squares_shade_top_visible_on_monitor(game.user)

    pygame.display.update()
    game.instructions = game.client.send(pickle.dumps(game.executable), False)
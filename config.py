# Client Settings
class ClientSettings:
    def __init__(self):
        self.EkranWidth = 900
        self.EkranHigh = 900
        self.drawterrain = True
        self.drawshades = True
        self.drawsmallshades = True
        self.szachownica = True
        self.shadow_depth = 0.2
        self.optimalize_scrren_visibility = True
        self.sztuczne3d = True
        self.showId = False
        self.showidNeighbours = False
        self.watereffects = False
        self.drawChunkBorders = True
        self.cameraspeed = 10
        self.freecamera = False
        self.map_holding = False
        self.developerOptions = {'map_spawning_Viever': False,
                                 'id-squares-visible': False,
                                 'draw-chunk-borders': False,
                                 'highlight_chunk': True,
                                 'sztuczny_monitor': False,
                                 'splaszcz_drzewa': False,
                                 'spawn_trees_on_click': False,
                                 'show_fps': True,
                                 'show_ekran_sectors': False,
                                 'small_squares_optimalisation': True}

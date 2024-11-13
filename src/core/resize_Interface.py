
import pygame

class ResizeInterface:
    def __init__(self, game_base: object):
        self.game_base = game_base
        self.original_resolution = (self.game_base.width, self.game_base.height)

    def for_dimenssoes_tela(self, nova_res:tuple, res_original:tuple): 
        nova = nova_res
        original = res_original
        for borda in self.game_base.dimension_list_screen:
            borda_copy = borda.copy()
            x_ratio = nova[0] / original[0] 
            y_ratio = nova[1] / original[1]
            borda.x = borda_copy.x * x_ratio 
            borda.y = borda_copy.y * y_ratio
            borda.width = borda_copy.width * x_ratio
            borda.height = borda_copy.height * y_ratio
        self.game_base.largura = borda.width
        self.game_base.altura = borda.height

    def for_tela_inicial(self, nova_res:tuple, res_original:tuple):
        nova = nova_res
        original = res_original
        for tela in self.game_base.list_tela_inicial:
            tela_copy = tela.copy()
            x_ratio = nova[0] / original[0] 
            y_ratio = nova[1] / original[1]
            tela.x = tela_copy.x * x_ratio
            tela.y = tela_copy.y * y_ratio
            tela.width = tela_copy.width
            tela.height = tela_copy.height

    def for_pre_pos_start(self, nova_res:tuple, res_original:tuple):
        nova = nova_res
        original = res_original
        for start in self.game_base.list_pre_pos_start:
            start_copy = start.copy()
            x_ratio = nova[0] / original[0] 
            y_ratio = nova[1] / original[1]
            start.x = start_copy.x * x_ratio 
            start.y = start_copy.y * y_ratio

    def for_tela_config(self, nova_res:tuple, res_original:tuple):
        nova = nova_res
        original = res_original
        for config in self.game_base.list_tela_config:
            config_copy = config.copy()
            x_ratio = nova[0] / original[0] 
            y_ratio = nova[1] / original[1]
            config.x = config_copy.x * x_ratio 
            config.y = config_copy.y * y_ratio 
            config.width = config_copy.width * x_ratio
            config.height = config_copy.height * y_ratio
    
    def calculo_obter_proporcao(self, nova_resolucao:tuple):
        nova_res = nova_resolucao
        res_original = self.original_resolution
        
        if nova_res == res_original:
            self.game_base.vars_screen_dimensions()
            self.game_base.vars_tela_inicial()
            self.game_base.vars_tela_config()
            self.game_base.vars_pre_pos_start()
        else:
            self.for_dimenssoes_tela(nova_res=nova_res, res_original=res_original)
            self.for_tela_inicial(nova_res=nova_res, res_original=res_original)
            self.for_pre_pos_start(nova_res=nova_res, res_original=res_original)
            self.for_tela_config(nova_res=nova_res, res_original=res_original)
            self.game_base.list_tela_config[1] = pygame.Rect(0, 0, 0, 0)

    def calculo_obter_proporcao_blocos(self, nova_resolucao=tuple):
        nova_res = nova_resolucao 
        res_orginal = self.original_resolution

        bloco_rect = self.game_base.blocks.bloco_Rect
        lis_blocos = self.game_base.blocks.lis_blocos

        if nova_res != res_orginal:
            for rect in lis_blocos:
                rect.width += bloco_rect.width 
                rect.height += bloco_rect.height 
            self.game_base.blocks.dimensionamento_espaco_blocos += 9
            self.game_base.blocks.dimensionamento_largura_bloco += 8 # Para alterar e centralizar os valores seria recomnedado mudar o espaço_blocos de multiplicação para adição ou subtração.
            self.game_base.blocks.dimensionamento_altura_bloco += 8 # Para alterar e centralizar os valores seria recomnedado mudar o espaço_blocos de multiplicação para adição ou subtração.

        else:
            for rect in lis_blocos:
                rect.width -= bloco_rect.width 
                rect.height -= bloco_rect.height
            self.game_base.blocks.dimensionamento_espaco_blocos -= 9
            self.game_base.blocks.dimensionamento_largura_bloco -= 8 # Para alterar e centralizar os valores seria recomnedado mudar o espaço_blocos de multiplicação para adição ou subtração.
            self.game_base.blocks.dimensionamento_altura_bloco -= 8 # Para alterar e centralizar os valores seria recomnedado mudar o espaço_blocos de multiplicação para adição ou subtração.
        
        self.game_base.blocks.lis_blocos.clear()
        self.game_base.blocks.criar_blocos()

    # def calculo_obter_proporcao_blocos_gym(self, nova_resolucao=tuple):
    #     nova_res = nova_resolucao 
    #     res_orginal = self.original_resolution

    #     bloco_rect = self.game_base.blocks.bloco_Rect
    #     lis_blocos = self.game_base.blocks.lis_blocos

    #     if nova_res != res_orginal:
    #         for rect in lis_blocos:
    #             rect.width -= bloco_rect.width 
    #             rect.height -= bloco_rect.height 
    #         self.game_base.blocks.dimensionamento_espaco_blocos -= 5
    #         self.game_base.blocks.dimensionamento_largura_bloco -= 5 # Para alterar e centralizar os valores seria recomnedado mudar o espaço_blocos de multiplicação para adição ou subtração.
    #         self.game_base.blocks.dimensionamento_altura_bloco -= 5 # Para alterar e centralizar os valores seria recomnedado mudar o espaço_blocos de multiplicação para adição ou subtração.
        
    #     self.game_base.blocks.lis_blocos.clear()
    #     self.game_base.blocks.criar_blocos()

    def calculo_obter_proporcao_players(self, nova_resolucao=tuple):
        nova_res = nova_resolucao 
        res_orginal = self.original_resolution

        if nova_res != res_orginal:
            self.game_base.player.set_pos_y += 50
            self.game_base.player2.set_pos_y += 50
        else:
            self.game_base.player.set_pos_y -= 50
            self.game_base.player2.set_pos_y -= 50

    def calculo_obter_proporcao_bola(self, nova_resolucao=tuple):
        nova_res = nova_resolucao 
        res_orginal = self.original_resolution






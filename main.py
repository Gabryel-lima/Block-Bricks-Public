from __future__ import annotations # Evita erro de dupla importação, só para garantir.
#from depreciated.src.block_bricks import Game
from src.Block_Bricks import BlockBricks

def main_bot_train():
    jogo = BlockBricks()
    jogo.run()

def cprfi():

    def mainProfile():
        BlockBricks()

    import cProfile
    import pstats

    profile = cProfile.Profile()
    profile.enable()

    mainProfile()

    profile.disable()
    stats = pstats.Stats(profile)
    stats.strip_dirs()
    stats.sort_stats('calls')
    stats.print_stats()


def main():
    jogo = BlockBricks()
    jogo.run()


if __name__ == "__main__":
    main()
    #main_bot_train()

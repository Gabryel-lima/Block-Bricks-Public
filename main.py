from src.core.block_bricks import Game

def cprfi():

    def mainProfile():
        Game()

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
    jogo = Game()
    jogo.run()


if __name__ == "__main__":
    main()

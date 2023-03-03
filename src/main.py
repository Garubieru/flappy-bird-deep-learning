from modules.game import FlappyBird
from modules.neat_adapter import NeatAdapter


if __name__ == '__main__':
    configFile = 'config-feedfoward'
    neat = NeatAdapter(configFile)
    game = FlappyBird(400, 800, 5, neat)
    game.start()
    neat.startPopulation(game.run)

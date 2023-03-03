import os
import neat
from typing import Callable


class NeatAdapter:
    def __init__(self, configFileName: str) -> None:
        currentPath = os.getcwd()
        self.configFile = os.path.join(currentPath, configFileName)
        self._startConfig()

    def _startConfig(self) -> None:
        self.neatConfig = neat.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            self.configFile)

    def startPopulation(self, evalFunction: Callable) -> None:
        self.population = neat.Population(self.neatConfig)
        self._startReporter()
        winnerGenome = self.population.run(evalFunction, 50)
        print('\nWinner genome: {!s}'.format(winnerGenome))

    def _startReporter(self) -> None:
        self.population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        self.population.add_reporter(stats)

    def createSharingNetwork(self, genome):
        net = neat.nn.FeedForwardNetwork.create(genome, self.neatConfig)
        return net

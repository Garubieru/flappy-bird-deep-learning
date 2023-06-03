from entities.bird import Bird
from entities.pipe_column import PipeColumn
from pygame import Surface, font
from modules.neat_adapter import NeatAdapter
from typing import Any


class GameManager:
    def __init__(self, screen: Surface, birdSpeed: int, neat: NeatAdapter, birdFont: font.Font, initialBirdPosition: int) -> None:
        self._score = 0
        self._failed = False
        self.birds: dict[int, tuple[Bird, Any, Any]] = {}
        self.screen = screen
        self.birdSpeed = birdSpeed
        self.birdFont = birdFont
        self.neat = neat
        self.initialBirdPosition = initialBirdPosition

    def generateBirds(self, genomes: list[Any]) -> None:
        self.birdsQuantity = len(genomes)
        for index, genome in genomes:
            bird = Bird(id=index,
                        screen=self.screen,
                        speed=self.birdSpeed,
                        initialPosition=self.initialBirdPosition,
                        font=self.birdFont)
            genome.fitness = 0
            network = self.neat.createSharingNetwork(genome)
            self.birds[bird.id] = (
                bird,
                network,
                genome)

    def getBirds(self) -> list[Bird]:
        birdValues = list(self.birds.values())
        return list(map(lambda birdValues: birdValues[0], birdValues))

    def increaseScore(self, bird: Bird) -> None:
        bird.increaseScore()
        for birdData in self.birds.values():
            birdData[2].fitness += 5

    def calculateJump(self, bird: Bird, pipeColumn: PipeColumn) -> None:
        birdData = self.birds.get(bird.id)
        if (birdData is None):
            return
        birdNetwork = birdData[1]
        birdGenome = birdData[2]
        output = birdNetwork.activate(
            (bird.y,
             abs(bird.y - pipeColumn.validScorePosition[1][0]),
             abs(bird.y - pipeColumn.validScorePosition[1][1]),
             ))
        birdGenome.fitness += 0.5
        if output[0] > 0.5:
            bird.jump()

    def getBirdScore(self, bird: Bird) -> int:
        return bird.score

    def lose(self, bird: Bird) -> None:
        birdData = self.birds.get(bird.id)
        if (birdData is None):
            return
        birdData[2].fitness -= 1
        self.birds.pop(bird.id, None)

    def isGameOver(self) -> bool:
        return not self.birds

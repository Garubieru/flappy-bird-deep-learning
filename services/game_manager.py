from entities.bird import Bird
from pygame import Surface


class GameManager:
    def __init__(self, screen: Surface, birdSpeed: int) -> None:
        self._score = 0
        self._failed = False
        self.birds: dict[str, Bird] = {}
        self.screen = screen
        self.birdSpeed = birdSpeed

    def generateBirds(self, birdsQuantity) -> None:
        self.birdsQuantity = birdsQuantity
        for _ in range(birdsQuantity):
            bird = Bird(screen=self.screen, speed=self.birdSpeed)
            self.birds[bird.id] = bird

    def getBirds(self) -> list[Bird]:
        return list(self.birds.values())

    def increaseScore(self, bird: Bird) -> None:
        bird.increaseScore()

    def getBirdScore(self, bird: Bird) -> int:
        return bird.score

    def lose(self, bird: Bird) -> None:
        self.birds.pop(bird.id, None)

    def isGameOver(self) -> bool:
        return not self.birds

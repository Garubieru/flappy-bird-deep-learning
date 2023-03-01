
import pygame
from entities.pipe_column import PipeColumn
from entities.bird import Bird
from services.game_manager import GameManager


class PipeManager:
    def __init__(self,
                 screen: pygame.Surface,
                 pipeSpeed: int,
                 pipeRange: int,
                 pipeSpacing: int,
                 gameManager: GameManager) -> None:
        self.pipeSpeed = pipeSpeed
        self.pipeRange = pipeRange
        self.pipeSpacing = pipeSpacing
        self.screen = screen
        self.gameManager = gameManager
        self.pipes = [PipeColumn(
            self.screen, self.pipeSpeed, self.pipeRange)]

    def manage(self) -> None:
        self._generatePipe()
        self._removePipe()

        for pipe in self.pipes:
            pipe.move()

    def checkBirdCollision(self, bird):
        for pipe in self.pipes:
            pipe.show()
            if pipe.isBirdInValidPositionScore(bird):
                self.gameManager.increaseScore(bird)

            if pipe.isBirdColliding(bird):
                self.gameManager.lose(bird)

    def _generatePipe(self) -> None:
        if not self._isValidToGenerate():
            return
        self.pipes.insert(0, PipeColumn(
            self.screen, self.pipeSpeed, self.pipeRange))

    def _isValidToGenerate(self) -> bool:
        validPositionToGenerate = self.screen.get_width() - self.pipeSpacing
        return self.pipes[0].pipeRect.x <= validPositionToGenerate

    def _removePipe(self) -> None:
        pipesLength = len(self.pipes)
        lastPipeIndex = pipesLength - 1
        lastPipe = self.pipes[lastPipeIndex]

        if (lastPipe.isOffScreen()):
            self.pipes.pop(lastPipeIndex)

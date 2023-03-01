import pygame
import random
import math
import uuid
from entities.bird import Bird
from images.pipe import PIPE_IMAGE


class PipeColumn:
    def __init__(self, screen: pygame.Surface, speed: int, range: int) -> None:
        self.id = uuid.uuid4()
        self.screen = screen
        self.speed = speed
        self.range = range
        self.alreadyScored = False
        self._loadImage()
        self._generatePipePosition()

    def _loadImage(self) -> None:
        image = PIPE_IMAGE.convert_alpha()

        resizedImage = pygame.transform.scale(
            image, (image.get_width() * 2, self.screen.get_height()))
        self.pipe = resizedImage
        self.pipeRect = self.pipe.get_rect()
        self.bottomPipeMask = pygame.mask.from_surface(self.pipe)

        pipeImageCopy = self.pipe.copy()
        self.invertedPipe = pygame.transform.flip(pipeImageCopy, False, True)
        self.invertedPipeRect = self.invertedPipe.get_rect()
        self.topPipeMask = pygame.mask.from_surface(self.invertedPipe)

        self.pipeRects = [self.pipeRect, self.invertedPipeRect]

    def _generatePipePosition(self) -> None:
        pipeInitialX = self.screen.get_width() + self.pipeRect.width
        self.pipeRect.x = pipeInitialX
        self.invertedPipeRect.x = pipeInitialX

        floorPipeY = random.randint(240, 580)
        self.pipeRect.y = floorPipeY
        self.invertedPipeRect.y = floorPipeY - \
            (self.screen.get_height() + self.range)
        self.pipeValidScoreYRange = [
            self.pipeRect.y - self.range, self.pipeRect.y]

    def show(self) -> None:
        self.validScorePosition = (
            math.trunc(self.pipeRect.x + (self.pipeRect.width / 2)), self.pipeValidScoreYRange)
        self.screen.blit(self.pipe, self.pipeRect)
        self.screen.blit(self.invertedPipe, self.invertedPipeRect)

    def move(self) -> None:
        self.pipeRect.x -= self.speed
        self.invertedPipeRect.x -= self.speed

    def isOffScreen(self) -> bool:
        return self.getXPos() <= -self.pipeRect.width

    def isBirdInValidPositionScore(self, bird: Bird) -> bool:
        if (self.alreadyScored):
            return False

        validScoreMinY = self.validScorePosition[1][0]
        validScoreMaxY = self.validScorePosition[1][1]
        isValid = bird.x >= self.validScorePosition[0] and (
            bird.y >= validScoreMinY and bird.y <= validScoreMaxY)

        self.alreadyScored = isValid

        return isValid

    def isBirdColliding(self, bird: Bird) -> bool:
        birdMask = bird.birdMask

        bottomPipeOffset = (self.getXPos() - bird.x,
                            self.getYPos() - bird.y)

        topPipeOffset = (self.getInvertedXPos() - bird.x,
                         self.getInvertedYPos() - bird.y)

        topPipeOverlapPosition = birdMask.overlap(
            self.topPipeMask, topPipeOffset)
        bottomPipeOverlapPosition = birdMask.overlap(
            self.bottomPipeMask, bottomPipeOffset)

        isCollidingWithTopPipe = topPipeOverlapPosition is not None
        isCollidingWithBottomPipe = bottomPipeOverlapPosition is not None

        isColliding = isCollidingWithBottomPipe or isCollidingWithTopPipe

        return isColliding

    def getXPos(self) -> int:
        return self.pipeRect.x

    def getYPos(self) -> int:
        return self.pipeRect.y

    def getInvertedXPos(self) -> int:
        return self.invertedPipeRect.x

    def getInvertedYPos(self) -> int:
        return self.invertedPipeRect.y

import pygame
import math
from images.bird import BIRD_IMAGES
from uuid import uuid4


class Bird:
    def __init__(self, id: int, screen: pygame.Surface, speed: int, initialPosition: int, font: pygame.font.Font) -> None:
        self.id = id
        self.images = BIRD_IMAGES
        self.x = initialPosition
        self.y = math.trunc(screen.get_height() / 2)

        self.currentImage = 0.0
        self.screen = screen
        self.currentSpeed = speed
        self.SPEED = speed
        self.imageSpeed = self.SPEED / 100

        self.isBirdStopped = False
        self.isJumpAllowed = True
        self.score = 0
        self.font = font
        self.idText = self.font.render(str(self.id), True, (100, 255, 0))

        self.draw()

    def draw(self) -> None:
        self.birdSurface = self.images[0].convert_alpha()
        self.birdRect = self.birdSurface.get_rect()
        self.birdRect.x = self.x
        self.birdRect.y = self.y

    def jump(self) -> None:
        isOnTopScreenEdge = self.birdRect.y < self.birdRect.height + self.SPEED + 40
        if (isOnTopScreenEdge):
            self.currentSpeed += 0
        else:
            self.rotate = True
            self.currentSpeed = -self.SPEED

    def show(self) -> None:
        self.birdRect.y += self.currentSpeed
        self.currentSpeed += 1
        self.y = self.birdRect.y

        if self.currentSpeed > 0:
            self.rotate = False

        self.currentImage += self.imageSpeed
        self.birdSurface = self.images[math.trunc(
            self.currentImage) % 3].convert_alpha()
        self.birdMask = self.getMask()

        if self.rotate:
            self.birdSurface = pygame.transform.rotate(self.birdSurface, 20)
        else:
            self.birdSurface = pygame.transform.rotate(self.birdSurface, -20)
        self.screen.blit(self.birdSurface, self.birdRect)
        self.label()

    def getMask(self) -> pygame.Mask:
        return pygame.mask.from_surface(self.birdSurface)

    def increaseScore(self) -> None:
        self.score += 1

    def label(self) -> None:
        height = 20
        width = 60

        labelSurface = pygame.surface.Surface(
            (width, height))
        labelSurface.set_alpha(100)
        labelSurface.fill((0, 0, 0))

        labelRect = labelSurface.get_rect()
        labelRectX = self.x - \
            math.trunc(self.birdSurface.get_width() / 2) + 10
        labelRectY = self.y - self.birdSurface.get_height() - 20

        labelRect.x = labelRectX
        labelRect.y = labelRectY
        scoreText = self.font.render(str(self.score), True,
                                     (255, 255, 255)).convert_alpha()
        scoreTextRect = scoreText.get_rect()
        scoreTextRect.x = labelRectX + 40
        scoreTextRect.y = labelRectY

        idTextRect = self.idText.get_rect()
        idTextRect.x = scoreTextRect.x - 40
        idTextRect.y = scoreTextRect.y

        self.screen.blit(labelSurface, labelRect)
        self.screen.blit(scoreText, scoreTextRect)
        self.screen.blit(self.idText, idTextRect)

import pygame
import math
from images.bird import BIRD_IMAGES
from uuid import uuid4


class Bird:
    def __init__(self, screen: pygame.Surface, speed: int) -> None:
        self.id = str(uuid4())
        self.images = BIRD_IMAGES
        self.x = math.trunc(
            (screen.get_width() - self.images[0].get_width()) // 2) - 60
        self.y = math.trunc(screen.get_height() / 2)

        self.currentImage = 0.0
        self.screen = screen
        self.currentSpeed = speed
        self.SPEED = speed
        self.imageSpeed = self.SPEED / 100

        self.isBirdStopped = False
        self.isJumpAllowed = True
        self.score = 0
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

    def getMask(self) -> pygame.Mask:
        return pygame.mask.from_surface(self.birdSurface)

    def increaseScore(self) -> None:
        self.score += 1

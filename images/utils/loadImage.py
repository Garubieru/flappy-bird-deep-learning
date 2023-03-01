import pygame


def loadImage(path: str) -> pygame.Surface:
    image = pygame.image.load(path)
    return image

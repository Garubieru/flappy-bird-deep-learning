import pygame
import math
import uuid
from entities.bird import Bird
from services.game_manager import GameManager


class Floor:
    def __init__(self, screen: pygame.Surface, speed: int, gameManager: GameManager) -> None:
        image = pygame.image.load('src/assets/base.png')
        self.id = uuid.uuid4()
        self.screen = screen
        self.speed = speed
        self.gameManager = gameManager
        self.image = pygame.transform.scale(
            image, (screen.get_width(), image.get_height())).convert_alpha()
        self.y = screen.get_height() - self.image.get_height()
        self.x = 0
        self.draw()

    def draw(self) -> None:
        self.firstFloorRect = self._createFloor(True)
        self.secondFloorRect = self._createFloor(False)

        self.floors = [self.firstFloorRect, self.secondFloorRect]

    def show(self) -> None:
        floorOutsidePosition = -(math.trunc(self.image.get_width()))
        isFirstFloorOutside = self.firstFloorRect.left <= floorOutsidePosition
        isSecondFloorOutside = self.secondFloorRect.left <= floorOutsidePosition

        if isFirstFloorOutside:
            self.firstFloorRect.left = self.image.get_width()

        if isSecondFloorOutside:
            self.secondFloorRect.left = self.image.get_width()

        for floor in self.floors:
            floor.left -= self.speed
            self.screen.blit(self.image, floor)

    def _createFloor(self, isInitial: bool) -> pygame.Rect:
        floorRect = self.image.get_rect()
        floorRect.x = self.x if isInitial else self.image.get_width()
        floorRect.y = self.y
        return floorRect

    def checkBirdCollision(self, bird: Bird) -> bool:
        birdMask = bird.birdMask
        floorMask = pygame.mask.from_surface(self.image)

        firstFloorCollindingOffset = (self.firstFloorRect.x - bird.x,
                                      self.firstFloorRect.y - bird.y)
        secondFloorCollindingOffset = (self.secondFloorRect.x - bird.x,
                                       self.secondFloorRect.y - bird.y)
        firstFloorOverlapPosition = birdMask.overlap(
            floorMask, firstFloorCollindingOffset)
        secondFloorOverlapPosition = birdMask.overlap(
            floorMask, secondFloorCollindingOffset)

        isFirstFloorColliding = firstFloorOverlapPosition is not None
        isSecondFloorColliding = secondFloorOverlapPosition is not None

        isColliding = isFirstFloorColliding or isSecondFloorColliding

        if (isColliding):
            self.gameManager.lose(bird)

        return isColliding

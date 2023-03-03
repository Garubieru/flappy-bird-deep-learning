import pygame
from modules.neat_adapter import NeatAdapter
from entities.floor import Floor
from services.pipe_manager import PipeManager
from services.game_manager import GameManager


class FlappyBird:
    def __init__(self, width: int, height: int, gameSpeed: int, neat: NeatAdapter) -> None:
        self.width = width
        self.height = height
        self.gameSpeed = gameSpeed
        self.neat = neat

    def start(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.width, self.height))
        self.clock = pygame.time.Clock()

        self._setBg()
        self._setFont()

        self.birdSpeed = 11

    def _setBg(self) -> None:
        image = pygame.image.load('src/assets/background-day.png')
        self.backgroundImage = pygame.transform.scale(
            image, (self.width, self.height)).convert_alpha()

    def _setFont(self) -> None:
        self.font = pygame.font.Font('src/assets/fonts/flappy-bird.ttf', 80)
        self.birdFont = pygame.font.Font(
            'src/assets/fonts/flappy-bird.ttf', 30)

    def run(self, genomes, config) -> None:
        pipeSpacing = 225
        self.gameManager = GameManager(
            self.screen, self.birdSpeed, self.neat, self.birdFont, pipeSpacing)
        self.floor = Floor(screen=self.screen,
                           speed=self.gameSpeed, gameManager=self.gameManager)
        self.pipeManager = PipeManager(
            screen=self.screen, pipeSpeed=self.gameSpeed, pipeSpacing=pipeSpacing, pipeRange=165, gameManager=self.gameManager)

        self.gameManager.generateBirds(genomes)

        self.running = True
        while self.running:
            self._drawScreen()

            birds = self.gameManager.getBirds()
            for bird in birds:
                bird.show()

                self.pipeManager.checkBirdCollision(bird)

                self.gameManager.calculateJump(
                    bird, self.pipeManager.getFirstPipeColumn())

                self.floor.checkBirdCollision(bird)

            self.pipeManager.manage()
            self.floor.show()

            if (self.gameManager.isGameOver()):
                self._drawFont('Game Over')
                self.running = False
                break

            self.clock.tick(60)
            pygame.display.flip()

    def _drawScreen(self) -> None:
        self.screen.blit(self.backgroundImage, self.backgroundImage.get_rect())

    def _drawFont(self, text: str, color: tuple[int, int, int] = (255, 255, 255), YPosittion=20) -> None:
        fontImage = self.font.render(text, True, color).convert_alpha()
        fontImageShadow = self.font.render(
            text, True, (0, 0, 0)).convert_alpha()

        fontImageXPosition = ((self.screen.get_width() - fontImage.get_width()) //
                              2)
        fontRect = fontImage.get_rect()
        fontRect.x = fontImageXPosition
        fontRect.y = YPosittion

        offset = 3
        fontShadowRect = fontImageShadow.get_rect()
        fontShadowRect.x = fontRect.x + offset
        fontShadowRect.y = fontRect.y + offset

        self.screen.blit(fontImageShadow, fontShadowRect)
        self.screen.blit(fontImage, fontRect)

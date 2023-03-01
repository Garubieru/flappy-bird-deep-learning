import pygame
import random
from entities.bird import Bird
from entities.floor import Floor
from services.pipe_manager import PipeManager
from services.game_manager import GameManager


class FlappyBird:
    def __init__(self, width: int, height: int, gameSpeed: int) -> None:
        self.width = width
        self.height = height
        self.gameSpeed = gameSpeed

    def start(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.width, self.height))
        self.clock = pygame.time.Clock()

        self._setBg()
        self._setFont()

        self.birdSpeed = 10
        self.gameManager = GameManager(self.screen, self.birdSpeed)
        self.floor = Floor(screen=self.screen,
                           speed=self.gameSpeed, gameManager=self.gameManager)
        self.pipeManager = PipeManager(
            screen=self.screen, pipeSpeed=self.gameSpeed, pipeSpacing=225, pipeRange=150, gameManager=self.gameManager)

        self.running = True
        self._run()

    def _setBg(self) -> None:
        image = pygame.image.load('assets/background-day.png')
        self.backgroundImage = pygame.transform.scale(
            image, (self.width, self.height)).convert_alpha()

    def _setFont(self) -> None:
        self.font = pygame.font.Font('assets/fonts/flappy-bird.ttf', 80)

    def _run(self) -> None:
        self.gameManager.generateBirds(1)

        while self.running:
            self._drawScreen()
            self.clock.tick(60)

            birds = self.gameManager.getBirds()
            print(self.clock.get_fps())
            for bird in birds:
                # randomNumber = random.randrange(-20, 30)
                # if (randomNumber > 20):
                #     bird.jump()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            bird.jump()
                bird.show()
                self.pipeManager.checkBirdCollision(bird)
                self.floor.checkBirdCollision(bird)

                self._drawFont(
                    f'{self.gameManager.getBirdScore(bird)}')

            self.pipeManager.manage()
            self.floor.show()

            if (self.gameManager.isGameOver()):
                self._drawFont('Game Over')

            pygame.display.flip()

        pygame.quit()

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


if __name__ == '__main__':
    game = FlappyBird(400, 800, 5)
    game.start()

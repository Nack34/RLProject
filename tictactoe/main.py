import pygame # type: ignore
from pygame.locals import * # type: ignore

from screen_manager import ScreenManager
from tictactoe_manager import TictactoeManagerPVP, TictactoeManagerPVB
from constants import FPS, get_path, check_button



class GameManager:
    """Manages the game loop and main menu."""
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(get_path("sounds/loop.mp3"))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.4)
        pygame.display.set_caption("Tictactoe")
        self.screen_manager = ScreenManager()
        self.running = True
        self.music = True 

    def __toggle_music(self):
        if self.music: pygame.mixer.music.stop()
        else : pygame.mixer.music.play(-1)

        self.music = not self.music

    def __handle_menu_event(self, event):
        """Handles menu events."""
        if event.type == pygame.QUIT:
            self.running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if self.screen_manager.buttons["pvp"].checkForInput(event.pos):
                self.running = TictactoeManagerPVP(self.screen_manager).run()

            elif self.screen_manager.buttons["pvb"].checkForInput(event.pos):
                self.running = TictactoeManagerPVB(self.screen_manager).run()

            elif self.screen_manager.buttons["quit"].checkForInput(event.pos):
                self.running = False
            
            elif check_button(event,900, 500):
                self.__toggle_music()


    def run(self):
        """Runs the main game loop."""
        while self.running:

            mouse_pos = pygame.mouse.get_pos()
            self.screen_manager.draw_menu(mouse_pos, self.music)

            for event in pygame.event.get():
                self.__handle_menu_event(event)

            pygame.display.update()
            self.screen_manager.clock.tick(FPS)

        pygame.mixer.music.stop()
        pygame.quit()







if __name__ == "__main__":
    GameManager().run()

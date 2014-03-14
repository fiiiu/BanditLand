
import pygame


class GraphicalInterface():

    def __init__(self):
        pygame.init()
        size=width, height=500, 240
        self.screen=pygame.display.set_mode(size)
        self.create_screens()
    
    def create_screens(self):
        self.blockstart_screen=self.create_message_screen("Press SPACE to start block...")
        self.blockend_screen=self.create_message_screen("Ending block... Press SPACE to continue")

    def create_message_screen(self, text):
        message_screen=pygame.Surface(self.screen.get_size())
        message_screen=message_screen.convert()
        message_screen.fill((20, 20, 20))
        font=pygame.font.Font(None, 36)
        message_text=font.render(text, 1, (210, 210, 210))
        message_textpos=message_text.get_rect(centerx=message_screen.get_width()/2, centery=message_screen.get_height()/2)
        message_screen.blit(message_text, message_textpos)
        return message_screen

    def start_block(self, i):
        self.screen.blit(self.blockstart_screen, (0,0))
        pygame.display.flip()
        waiting=True
        while waiting:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting=False

    def end_block(self):
        self.screen.blit(self.blockend_screen, (0,0))
        pygame.display.flip()
        waiting=True
        while waiting:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting=False

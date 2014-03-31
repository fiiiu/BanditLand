
import pygame


class GraphicalInterface():

    def __init__(self):
        pygame.init()
        size=width, height=500, 240
        self.screen=pygame.display.set_mode(size)
        self.create_static_screens()
    
    def create_static_screens(self):
        self.blockstart_screen=self.create_message_screen("Press SPACE to start block...")
        self.blockend_screen=self.create_message_screen("Ending block... Press SPACE to continue")
        self.trial_screen=self.create_trial_screen()

    def create_message_screen(self, text):
        message_screen=pygame.Surface(self.screen.get_size())
        message_screen=message_screen.convert()
        message_screen.fill((20, 20, 20))
        font=pygame.font.Font(None, 36)
        message_text=font.render(text, 1, (210, 210, 210))
        message_textpos=message_text.get_rect(centerx=message_screen.get_width()/2, centery=message_screen.get_height()/2)
        message_screen.blit(message_text, message_textpos)
        return message_screen

    def create_trial_screen(self):
        trial_screen=pygame.Surface(self.screen.get_size())
        trial_screen=trial_screen.convert()
        trial_screen.fill((20, 20, 20))
        font=pygame.font.Font(None, 36)
        trial_text_A=font.render('A', 1, (210, 210, 210))
        trial_text_B=font.render('B', 1, (210, 210, 210))
        trial_textpos_A=trial_text_A.get_rect(centerx=trial_screen.get_width()/4, centery=trial_screen.get_height()/2)
        trial_textpos_B=trial_text_B.get_rect(centerx=3*trial_screen.get_width()/4, centery=trial_screen.get_height()/2)
        trial_screen.blit(trial_text_A, trial_textpos_A)        
        trial_screen.blit(trial_text_B, trial_textpos_B)
        return trial_screen

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

    def choice_screen(self):
        self.screen.blit(self.trial_screen, (0,0))
        pygame.display.flip()
        waiting=True
        while waiting:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        choice=0
                        waiting=False
                    if event.key == pygame.K_RIGHT:
                        choice=1
                        waiting=False
        return choice

    def feedback_screen(self, reward):
        feedback_screen=self.create_message_screen("Reward was {0}. SPACE to continue".format(reward))
        self.screen.blit(feedback_screen, (0,0))
        pygame.display.flip()
        waiting=True
        while waiting:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting=False
                    
    def metacognitive_screen(self, report_type):
        if report_type==0:
            return None
        elif report_type==1:
            metacognitive_screen=self.create_message_screen("MeTaCoGnItIoN! Left/Right to report")
            self.screen.blit(metacognitive_screen, (0,0))
            pygame.display.flip()
            waiting=True
            while waiting:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            report=0
                            waiting=False
                        if event.key == pygame.K_RIGHT:
                            report=1
                            waiting=False
            return report
        elif report_type==2:
            metacognitive_screen=self.create_message_screen("MeTaCoGnItIoN! Left/Right to report")
            self.screen.blit(metacognitive_screen, (0,0))
            pygame.display.flip()
            waiting=True
            while waiting:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            report=0
                            waiting=False
                        if event.key == pygame.K_RIGHT:
                            report=1
                            waiting=False
            return report

        
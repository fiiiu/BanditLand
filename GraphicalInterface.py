# -*- coding: utf-8 -*-

import sys
import pygame
import parameters


class GraphicalInterface():

    def __init__(self):
        pygame.init()
        size=width, height=800, 600
        self.screen=pygame.display.set_mode(size)
        #self.screen=pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.create_static_screens()

    
    def create_static_screens(self):
        self.blockstart_screen=self.create_message_screen("Press SPACE to start block...")
        self.blockend_screen=self.create_message_screen("Ending block... Press SPACE to continue")
        self.trial_screen=self.create_trial_progress_screen(0,0)
        self.reward_screens=[]
        for i in range(parameters.n_bandits):
            self.reward_screens.append([])
            for j in range(2):
                self.reward_screens[i].append(self.create_reward_screen(i,j))
        self.metacognitive_screens={}
        for condition in parameters.include_conditions:
            self.metacognitive_screens[condition]=self.create_metacognitive_screen(condition)

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
        #trial_screen.blit(trial_text_A, trial_textpos_A)        
        #trial_screen.blit(trial_text_B, trial_textpos_B)
        
        first_bandit_left=self.screen.get_width()/4-self.screen.get_width()*parameters.bandit_width/2
        first_bandit_top=self.screen.get_height()/4+self.screen.get_height()*parameters.bandit_height/2        
        second_bandit_left=3*self.screen.get_width()/4-self.screen.get_width()*parameters.bandit_width/2
        second_bandit_top=self.screen.get_height()/4+self.screen.get_height()*parameters.bandit_height/2        
        
        first_bandit_rect=pygame.Rect(first_bandit_left, first_bandit_top, \
                                self.screen.get_width()*parameters.bandit_width, self.screen.get_height()*parameters.bandit_height)
        second_bandit_rect=pygame.Rect(second_bandit_left, second_bandit_top, \
                                self.screen.get_width()*parameters.bandit_width, self.screen.get_height()*parameters.bandit_height)
        
        self.first_bandit=pygame.draw.rect(trial_screen, (255,0,0), first_bandit_rect)
        self.second_bandit=pygame.draw.rect(trial_screen, (0,0,255), second_bandit_rect)
        
        return trial_screen


    def create_trial_progress_screen(self, played, won):
        trial_progress_screen=self.create_trial_screen()

        outline_rect=pygame.Rect(self.screen.get_width()/4, self.screen.get_height()/8, \
                                 self.screen.get_width()*parameters.progress_width, \
                                 self.screen.get_height()*parameters.progress_height)

        trialnum_rect=pygame.Rect(self.screen.get_width()/4, self.screen.get_height()/8,\
                                  float(played)/parameters.n_trials*self.screen.get_width()*parameters.progress_width, \
                                  self.screen.get_height()*parameters.progress_height)
                

        # SUCIO LEER ACA DE PARAMETERS N_TRIALS!!!!
        progress_rect=pygame.Rect(self.screen.get_width()/4, self.screen.get_height()/8,\
                                  float(won)/parameters.n_trials*self.screen.get_width()*parameters.progress_width, \
                                  self.screen.get_height()*parameters.progress_height)
                
        self.outline=pygame.draw.rect(trial_progress_screen, (40,40,40), outline_rect)
        self.trialnum=pygame.draw.rect(trial_progress_screen, (0,100,0), trialnum_rect)
        self.progress=pygame.draw.rect(trial_progress_screen, (0,255,0), progress_rect)
        
        return trial_progress_screen


    def create_metacognitive_screen(self, report_type):

        if report_type == 0:
            return None
        elif report_type == 1:
            metacognitive_screen=self.create_trial_screen()
            font=pygame.font.Font(None, 36)
            metacog_text=font.render(u'¿Qué máquina paga más?', 1, (210, 210, 210))
            metacog_textpos=metacog_text.get_rect(centerx=metacognitive_screen.get_width()/2, centery=1*metacognitive_screen.get_height()/4)
            metacognitive_screen.blit(metacog_text, metacog_textpos)        
            return metacognitive_screen
        elif report_type == 2:
            metacognitive_screen=self.create_trial_screen()
            font=pygame.font.Font(None, 36)
            metacog_text=font.render(u'¿Qué máquina paga más?', 1, (210, 210, 210))
            metacog_textpos=metacog_text.get_rect(centerx=metacognitive_screen.get_width()/2, centery=0.3*metacognitive_screen.get_height())
            metacognitive_screen.blit(metacog_text, metacog_textpos)        
            metacog_text_conf=font.render(u'¿Con qué grado de seguridad?', 1, (210, 210, 210))
            metacog_textpos_conf=metacog_text_conf.get_rect(centerx=metacognitive_screen.get_width()/2, centery=0.7*metacognitive_screen.get_height())
            metacog_text_conf_a=font.render(u'alto', 1, (210, 210, 210))
            metacog_text_conf_b=font.render(u'bajo', 1, (210, 210, 210))
            metacog_textpos_conf_a=metacog_text_conf_a.get_rect(centerx=self.screen.get_width()*(0.25+parameters.progress_width)+40, \
                                                                centery=0.8*metacognitive_screen.get_height())
            metacog_textpos_conf_b=metacog_text_conf_b.get_rect(centerx=self.screen.get_width()/4-40, \
                                                                centery=0.8*metacognitive_screen.get_height())
            metacognitive_screen.blit(metacog_text_conf, metacog_textpos_conf)
            metacognitive_screen.blit(metacog_text_conf_a, metacog_textpos_conf_a)        
            metacognitive_screen.blit(metacog_text_conf_b, metacog_textpos_conf_b)                
            confidence_bar=pygame.Rect(self.screen.get_width()/4, self.screen.get_height()*0.77, \
                                 self.screen.get_width()*parameters.progress_width, \
                                 self.screen.get_height()*parameters.confidence_height)
            self.bar=pygame.draw.rect(metacognitive_screen, (80,0,80), confidence_bar)
            return metacognitive_screen


    def create_reward_screen(self, bandit, reward):
        reward_screen=self.create_trial_screen()
        if bandit==0:
            if reward==1:   
                pygame.draw.circle(reward_screen, (255,255,0), (self.first_bandit.centerx, int(self.first_bandit.bottom-2*parameters.reward_size*self.screen.get_width())),\
                                    int(self.screen.get_width()*parameters.reward_size))
            elif reward==0:
                pygame.draw.circle(reward_screen, (0,0,0), (self.first_bandit.centerx, int(self.first_bandit.bottom-2*parameters.reward_size*self.screen.get_width())),\
                                    int(self.screen.get_width()*parameters.reward_size))
        elif bandit==1:
            if reward==1:
                pygame.draw.circle(reward_screen, (255,255,0), (self.second_bandit.centerx, int(self.second_bandit.bottom-2*parameters.reward_size*self.screen.get_width())),\
                                    int(self.screen.get_width()*parameters.reward_size))
            elif reward==0:
                pygame.draw.circle(reward_screen, (0,0,0), (self.second_bandit.centerx, int(self.second_bandit.bottom-2*parameters.reward_size*self.screen.get_width())),\
                                    int(self.screen.get_width()*parameters.reward_size))

        return reward_screen



    def start_block(self, i):
        self.set_progress(0,0)
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

    def show_choice_screen(self):
        self.screen.blit(self.trial_screen, (0,0))
        pygame.display.flip()
        waiting=True
        while waiting:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        if self.first_bandit.collidepoint(pos):
                            choice=0
                            waiting=False
                        elif self.second_bandit.collidepoint(pos):
                            choice=1
                            waiting=False
                            
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_LEFT:
                        choice=0
                        waiting=False
                    elif event.key == pygame.K_RIGHT:
                        choice=1
                        waiting=False
        return choice

    def show_feedback_screen(self, choice, reward):
        self.screen.blit(self.reward_screens[choice][reward], (0,0))
        pygame.display.flip()
        pygame.time.delay(300)
                    
    def show_metacognitive_screen(self, report_type):
        if report_type==0:
            return None
        elif report_type==1:
            self.screen.blit(self.metacognitive_screens[report_type], (0,0))
            pygame.display.flip()
            waiting=True
            while waiting:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            pos = pygame.mouse.get_pos()
                            if self.first_bandit.collidepoint(pos):
                                report=0
                                waiting=False
                            elif self.second_bandit.collidepoint(pos):
                                report=1
                                waiting=False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            report=0
                            waiting=False
                        if event.key == pygame.K_RIGHT:
                            report=1
                            waiting=False
            
            if report==0:
                temporary_report=pygame.draw.rect(self.metacognitive_screens[report_type], (255,255,255), self.first_bandit)
            elif report==1:
                temporary_report=pygame.draw.rect(self.metacognitive_screens[report_type], (255,255,255), self.second_bandit)
            self.screen.blit(self.metacognitive_screens[report_type], (0,0))
            pygame.display.flip()
            pygame.time.delay(200)
            self.metacognitive_screens[report_type]=self.create_metacognitive_screen(report_type)
            return report

        elif report_type==2:
            self.screen.blit(self.metacognitive_screens[report_type], (0,0))
            pygame.display.flip()
            waiting_report=True
            while waiting_report:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            pos = pygame.mouse.get_pos()
                            if self.first_bandit.collidepoint(pos):
                                report=0
                                waiting_report=False
                            elif self.second_bandit.collidepoint(pos):
                                report=1
                                waiting_report=False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            report=0
                            waiting_report=False
                        if event.key == pygame.K_RIGHT:
                            report=1
                            waiting_report=False

            if report==0:
                temporary_report=pygame.draw.rect(self.metacognitive_screens[report_type], (255,255,255), self.first_bandit)
            elif report==1:
                temporary_report=pygame.draw.rect(self.metacognitive_screens[report_type], (255,255,255), self.second_bandit)
            self.screen.blit(self.metacognitive_screens[report_type], (0,0))
            pygame.display.flip()
            pygame.time.delay(200)
            self.metacognitive_screens[report_type]=self.create_metacognitive_screen(report_type)
            self.screen.blit(self.metacognitive_screens[report_type], (0,0))
            pygame.display.flip()

            waiting_confidence=True
            while waiting_confidence:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            pos = pygame.mouse.get_pos()
                            if self.bar.collidepoint(pos):
                                confidence=float(pos[0]-self.bar.left)/self.bar.width
                                waiting_confidence=False

            temporary_confidence=pygame.draw.rect(self.metacognitive_screens[report_type], (255,255,255),\
                                                  (pos[0]-5, self.bar.top, 10, self.bar.height))         
            self.screen.blit(self.metacognitive_screens[report_type], (0,0))
            pygame.display.flip()
            pygame.time.delay(200)
            self.metacognitive_screens[report_type]=self.create_metacognitive_screen(report_type)
            return (report, confidence)


    def set_progress(self, played, won):
        self.trial_screen=self.create_trial_progress_screen(played, won)
        


        
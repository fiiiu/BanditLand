# -*- coding: utf-8 -*-

import sys
import pygame
import parameters


class GraphicalInterface():

    def __init__(self):
        pygame.init()
        #if parameters.fullscreen:
            #self.screen=pygame.display.set_mode((0,0), pygame.FULLSCREEN)
            #pygame.mouse.set_visible(False)
        #else:
        size=width, height=800, 600
        self.window=pygame.display.set_mode(size)
        
        self.create_visual_elements()
        self.create_screens()


    def create_screens(self):
        self.trial_screen=TrialScreen(self.bandits, self.progress_bar)

    def create_visual_elements(self):
        window_rect=self.window.get_rect()
        #self.first_bandit, self.second_bandit
        self.bandits=self.create_bandits()
        self.progress_bar=ProgressBar((window_rect.width*parameters.progress_width, window_rect.height*parameters.progress_height),\
                                        (window_rect.width*0.25, window_rect.height*0.125))

    def create_bandits(self):
        window_rect=self.window.get_rect()
        first_bandit_left=int(window_rect.width*0.15)
        first_bandit_top=int(window_rect.height*0.25)
        second_bandit_left=int(window_rect.width*0.7)
        second_bandit_top=int(window_rect.height*0.25)
          
        size=[int(parameters.bandit_width*window_rect.width), int(parameters.bandit_height*window_rect.height)]
        
        fbs=BanditSprite(size, (first_bandit_left,first_bandit_top), (255,0,0))
        sbs=BanditSprite(size, (second_bandit_left,second_bandit_top), (0,0,255))

        return fbs, sbs

    def run(self):

        choice=self.show_choice_screen()
        self.show_feedback_screen(choice, 0)
        #self.first_bandit.reward(1)
        #self.show_choice_screen()
        
        # self.trial_screen.draw(self.window)
        # pygame.display.flip()
        # pygame.time.delay(1000) 
        # self.progress_bar.update(5,3)

        # self.trial_screen.draw(self.window)
        # pygame.display.flip()
        pygame.time.delay(1000) 


    def show_choice_screen(self):
            #self.screen.blit(self.trial_screen, (0,0))
            self.trial_screen.draw(self.window)
            pygame.display.flip()
            waiting=True
            while waiting:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            pos = pygame.mouse.get_pos()
                            #if self.first_bandit.collidepoint(pos):
                            if self.bandits[0].touched(pos):
                                choice=0
                                waiting=False
                            elif self.bandits[1].touched(pos):
                            #elif self.second_bandit.collidepoint(pos):
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
        #self.screen.blit(self.reward_screens[choice][reward], (0,0))
        self.bandits[choice].update(reward)
        self.trial_screen.draw(self.window)
        pygame.display.flip()
        pygame.time.delay(300)


### SCREENS

class TrialScreen(pygame.sprite.LayeredDirty):

        def __init__(self, bandits, progress_bar):
            pygame.sprite.LayeredDirty.__init__(self)

            self.add(bandits, progress_bar)


### SPRITES

class BanditSprite(pygame.sprite.DirtySprite):
    
    def __init__(self, size, pos, color):
        pygame.sprite.DirtySprite.__init__(self)
    
        self.image = pygame.Surface(size)
        self.rect=pygame.Rect(pos, size)
        #self.image = self.image.convert_alpha()
        width,height=size
      
        self.body=pygame.draw.rect(self.image, color, (0,0,0.6*width, height))
        pygame.draw.polygon(self.image, (150,150,0), [(self.body.right, self.body.centery),\
                                                                   (self.body.right+0.2*width, self.body.centery),\
                                                                   (self.body.right+0.2*width, self.body.top+0.05*height),\
                                                                   (self.body.right+0.15*width, self.body.top+0.05*height),\
                                                                   (self.body.right+0.15*width, self.body.centery-0.05*height),\
                                                                   (self.body.right, self.body.centery-0.05*height)])
        pygame.draw.circle(self.image, (150,150,0), (int(self.body.right+width*0.175), int(self.body.top+height*0.1)), int(width*0.08))
        
        self.dirty=1
        self.visible=1

    def touched(self, pos):
        #looking at whole rect now, adjust this to body+arm
        return self.rect.collidepoint(pos)


    def update(self, reward):
        self.reward(reward)

    def reward(self, won):
        if won==1:
            pygame.draw.circle(self.image, (255,255,0), (int(self.body.centerx), int(self.body.bottom-2*parameters.reward_size*self.rect.width)),\
                                                        int(self.rect.width*parameters.reward_size))
        
        elif won==0:
            pygame.draw.circle(self.image, (0,0,0), (int(self.body.centerx), int(self.body.bottom-2*parameters.reward_size*self.rect.width)),\
                                                   int(self.rect.width*parameters.reward_size))
        self.dirty=1



class ProgressBar(pygame.sprite.LayeredDirty):

    def __init__(self, size, pos):
        pygame.sprite.LayeredDirty.__init__(self)
        width,height=size
        self.outline=Bar(size, pos, (40,40,40))
        self.trialnum=Bar((0,height), pos, (0,100,0))
        self.progress=Bar((0,height), pos, (0,255,0))
        self.add(self.outline, self.trialnum, self.progress)

    def update(self, played, won):
        trial_width=int(self.outline.rect.width*float(played)/parameters.n_trials)
        self.trialnum.update(trial_width)
        progress_width=int(self.outline.rect.width*float(won)/parameters.n_trials)
        self.progress.update(progress_width)


class Bar(pygame.sprite.DirtySprite):

    def __init__(self, size, pos, color):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty=1        
        self.image=pygame.Surface(size)
        self.rect=pygame.Rect(pos,size)
        self.color=color
        self.image.fill(self.color)
        
    def update(self, new_width):
        new_size=(new_width, self.rect.height)
        self.image=pygame.Surface(new_size)
        self.image.fill(self.color)
        self.dirty=1

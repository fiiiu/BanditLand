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
        self.trial_screen=TrialScreen(self.dark_background, self.bandits, self.progress_bar)
        self.metacognitive_screen=MetacognitiveScreen(self.light_background, self.bandits, 1, self.first_question)

    def create_visual_elements(self):
        window_rect=self.window.get_rect()
        #self.first_bandit, self.second_bandit
        self.dark_background=BackgroundSprite(window_rect.size, (20,20,20))
        self.light_background=BackgroundSprite(window_rect.size, (120,120,120))
        self.bandits=self.create_bandits()
        self.progress_bar=ProgressBar((window_rect.width*parameters.progress_width, window_rect.height*parameters.progress_height),\
                                        (window_rect.width*0.25, window_rect.height*0.125))

        self.first_question=MessageSprite((window_rect.width,60), (int(window_rect.width*0), int(window_rect.height*0.1)), u'¿Qué máquina paga más?')



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

    def start_block(self, a):
        pass

    def end_block(self):
        pass


    def set_progress(self, played, won):
        self.progress_bar.update(played, won)        

        # if played<parameters.n_trials:
        #     self.trial_screen=self.create_trial_progress_screen(played, won)
        # else:
        #     self.blockend_screen=self.create_blockend_screen(played,won)


    def show_metacognitive_screen(self, report_type):
        
        #pygame.display.flip()
        if report_type==0:
            return None
        elif report_type==1:
            #self.screen.blit(self.metacognitive_screens[report_type], (0,0))
            self.metacognitive_screen.draw(self.window)
            pygame.display.flip()
            waiting=True
            while waiting:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            pos = pygame.mouse.get_pos()
                            if self.bandits[0].touched(pos):
                                report=0
                                waiting=False
                            elif self.bandits[1].touched(pos):
                                report=1
                                waiting=False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            report=0
                            waiting=False
                        if event.key == pygame.K_RIGHT:
                            report=1
                            waiting=False
            
            # if report==0:
            #     #temporary_report=pygame.draw.rect(self.metacognitive_screens[report_type], (255,255,255), self.first_bandit)
            #     self.bandits[0].selected()
            # elif report==1:
            #     temporary_report=pygame.draw.rect(self.metacognitive_screens[report_type], (255,255,255), self.second_bandit)
            # self.screen.blit(self.metacognitive_screens[report_type], (0,0))
            # pygame.display.flip()
            # pygame.time.delay(200)
            # self.metacognitive_screens[report_type]=self.create_metacognitive_screen(report_type)
            # return report

            self.bandits[report].selected()
            self.metacognitive_screen.draw(self.window)
            pygame.display.flip()
            pygame.time.delay(200)
            self.bandits[report].clear()
            self.metacognitive_screen.draw(self.window)
            pygame.display.flip()
            #self.background.dirty=1
            return report


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
        self.bandits[choice].reward(reward)
        self.trial_screen.draw(self.window)
        pygame.display.flip()
        pygame.time.delay(300)
        self.bandits[choice].clear()
        self.trial_screen.draw(self.window)
        pygame.display.flip()
        


### SCREENS

class TrialScreen(pygame.sprite.LayeredDirty):
    def __init__(self, background, bandits, progress_bar):
        pygame.sprite.LayeredDirty.__init__(self)
        self.add(background, bandits, progress_bar)

class MetacognitiveScreen(pygame.sprite.LayeredDirty):
    def __init__(self, background, bandits, metacog_type, messages):
        pygame.sprite.LayeredDirty.__init__(self)
        self.add(background, bandits, messages)
        





### SPRITES

class BackgroundSprite(pygame.sprite.DirtySprite):
    def __init__(self, size, color):
        pygame.sprite.DirtySprite.__init__(self)
        self.image=pygame.Surface(size)
        self.rect=pygame.Rect((0,0), size)
        self.image.fill(color)
        self.dirty=1


class MessageSprite(pygame.sprite.DirtySprite):

    def __init__(self, size, pos, message):
        pygame.sprite.DirtySprite.__init__(self)
        self.image=pygame.Surface(size)
        self.rect=pygame.Rect(pos, size)

        font=pygame.font.Font(None, 36)
        self.text=font.render(message, 1, (200,200,200))
        textpos=self.text.get_rect(centerx=self.rect.centerx,centery=20)
        self.image.blit(self.text, textpos)
        self.dirty=1
        #?#metacognitive_screen.blit(metacog_text, metacog_textpos) 

        

class BanditSprite(pygame.sprite.DirtySprite):
    
    def __init__(self, size, pos, color):
        pygame.sprite.DirtySprite.__init__(self)
    
        self.image = pygame.Surface(size)
        self.rect=pygame.Rect(pos, size)
        #self.image = self.image.convert_alpha()
        width,height=size
      
        self.color=color
        self.body=pygame.draw.rect(self.image, self.color, (0,0,0.6*width, height))
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

    def reward(self, won):
        if won==1:
            pygame.draw.circle(self.image, (255,255,0), (int(self.body.centerx), int(self.body.bottom-2*parameters.reward_size*self.rect.width)),\
                                                        int(self.rect.width*parameters.reward_size))
        
        elif won==0:
            pygame.draw.circle(self.image, (0,0,0), (int(self.body.centerx), int(self.body.bottom-2*parameters.reward_size*self.rect.width)),\
                                                   int(self.rect.width*parameters.reward_size))
        self.dirty=1

    def selected(self):
        self.body=pygame.draw.rect(self.image, (255,255,255), (0,0,0.6*self.rect.width, self.rect.height))
        self.dirty=1

    def clear(self):
        self.body=pygame.draw.rect(self.image, self.color, (0,0,0.6*self.rect.width, self.rect.height))
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

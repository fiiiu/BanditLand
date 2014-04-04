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
        self.screen=pygame.display.set_mode(size)
        #self.create_static_screens()

        self.bs=BanditSprite(width,height)




class BanditSprite(pygame.sprite.Sprite):
    
    def __init__(self, screen_width, screen_height):
        pygame.sprite.Sprite.__init__(self)


        self.image = pygame.Surface([parameters.bandit_width, parameters.bandit_height])

        first_bandit_left=screen_width()/4-screen_width()*parameters.bandit_width/2
        first_bandit_top=screen_height()/4+screen_height()*parameters.bandit_height/2        
        
        first_bandit_rect=pygame.Rect(first_bandit_left, first_bandit_top, \
                                screen_width()*parameters.bandit_width, screen_height()*parameters.bandit_height)

        self.first_bandit=pygame.draw.rect(self.image, (255,0,0), first_bandit_rect)



       #  self.image = image
       #  self.rect = pygame.Rect((0, 0), image.get_size())
       #  self.defineHeadPos()

       # # Call the parent class (Sprite) constructor
       #  pygame.sprite.Sprite.__init__(self) 
         
       #  # Set the background color and set it to be transparent
       #  self.image = pygame.Surface([width, height])
       #  self.image.fill(white)
       #  self.image.set_colorkey(white)
         
       #  # Draw the ellipse
       #  pygame.draw.ellipse(self.image, color, [0, 0, width, height])


       #  first_bandit_left=self.screen.get_width()/4-self.screen.get_width()*parameters.bandit_width/2
       #  first_bandit_top=self.screen.get_height()/4+self.screen.get_height()*parameters.bandit_height/2        
        
       #  first_bandit_rect=pygame.Rect(first_bandit_left, first_bandit_top, \
       #                          self.screen.get_width()*parameters.bandit_width, self.screen.get_height()*parameters.bandit_height)
        
       #  first_arm=pygame.draw.polygon(trial_screen, (150,150,0), [(first_bandit_rect.right, first_bandit_rect.centery),\
       #                                                            (first_bandit_rect.right+30, first_bandit_rect.centery),\
       #                                                            (first_bandit_rect.right+30, first_bandit_rect.top+10),\
       #                                                            (first_bandit_rect.right+20, first_bandit_rect.top+10),\
       #                                                            (first_bandit_rect.right+20, first_bandit_rect.centery-10),\
       #                                                            (first_bandit_rect.right, first_bandit_rect.centery-10)])
       #  first_ball=pygame.draw.circle(trial_screen, (150,150,0), (first_bandit_rect.right+25, first_bandit_rect.top+10), 10)
                                               
        
       #  self.first_bandit=pygame.draw.rect(trial_screen, (255,0,0), first_bandit_rect)

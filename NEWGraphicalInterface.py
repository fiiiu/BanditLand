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
        #self.create_static_screens()

        window_rect=self.window.get_rect()
        first_bandit_left=int(window_rect.width/4-window_rect.width*parameters.bandit_width/2)
        first_bandit_top=int(window_rect.height/4+window_rect.height*parameters.bandit_height/2)     
        self.bs=BanditSprite(self.window.get_rect(), (first_bandit_left, first_bandit_top))

        self.group=pygame.sprite.LayeredDirty()
        self.group.add(self.bs)
        print "draw"
        self.group.draw(self.window)
        i=0
        while i < 5:
            pygame.display.flip()
            i+=1

        pygame.time.delay(1000) 





class BanditSprite(pygame.sprite.DirtySprite):
    
    def __init__(self, window_rect, pos):
        print pos
        pygame.sprite.DirtySprite.__init__(self)


        size=[int(parameters.bandit_width*window_rect.width), int(parameters.bandit_height*window_rect.height)]
        self.image = pygame.Surface(size)
   
        self.rect=pygame.Rect(pos, size)

        pygame.draw.rect(self.image, (255,0,0), self.rect)

        pygame.draw.circle(self.image, (150,150,0), pos, 10)

        self.dirty=1
        self.visible=1



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

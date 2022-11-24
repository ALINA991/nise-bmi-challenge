#!/usr/bin/env python
# coding: utf-8

# In[9]:


import numpy as np
#import pygame as pg
import random


# In[34]:


def the_grid(xb,yb,xp,yp):
    grid = np.ones((10,10))
    grid[xb][yb] = 66
    grid[xp][yp] = 44 
    print(grid)
    
def take_player2ball(xb,yb,xp,yp):
    if xp-xb>0 and yp-yb>0:
        print('1')
        yp = yp-1
        xp = xp-1
        the_grid(xb,yb,xp,yp)
        take_player2ball(xb,yb,xp,yp)
        
    elif xp-xb<0 and yp-yb<0:
        print('2')
        yp = yp+1
        xp = xp+1
        the_grid(xb,yb,xp,yp)
        take_player2ball(xb,yb,xp,yp)
        
    elif xp-xb==0 and yp-yb<0:
        print('3')
        if yp-yb==-1:
            return the_grid(xb,yb,xp,yp)
        else:
            yp = yp+1
            the_grid(xb,yb,xp,yp)
            take_player2ball(xb,yb,xp,yp)
            
    elif xp-xb==0 and yp-yb>0:
        print('4')
        if yp-yb==1:
            return the_grid(xb,yb,xp,yp)
        else:
            yp = yp-1 
            the_grid(xb,yb,xp,yp)
            take_player2ball(xb,yb,xp,yp)
            
    elif xp-xb>0 and yp-yb==0:
        print('5')
        if xp-xb==1:
            return the_grid(xb,yb,xp,yp)
        else:
            xp = xp-1 
            the_grid(xb,yb,xp,yp)
            take_player2ball(xb,yb,xp,yp)
    
    elif xp-xb<0 and yp-yb==0:
        print('6')
        if xp-xb==-1:
            return the_grid(xb,yb,xp,yp)
        else:
            xp = xp+1 
            the_grid(xb,yb,xp,yp)
            take_player2ball(xb,yb,xp,yp)
            
def 


# In[42]:



print(grid)

xb = 7#random.randint(0, 9)
yb = 8

xp = 7#random.randint(0, 9)
yp = 0

#print(xp)
#print(grid[xb][yb])
#grid[xb][yb] = 66
#grid[xp][yp] = 44

#print(grid)
#the_grid(xb,yb,xp,yp)

take_player2ball(xb,yb,xp,yp)


# In[ ]:





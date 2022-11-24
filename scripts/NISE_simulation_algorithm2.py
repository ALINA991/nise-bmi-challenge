#!/usr/bin/env python
# coding: utf-8

# In[9]:


import numpy as np
#import pygame as pg
import random


# In[69]:



def kick(xb,yb,xp,yp):
    if xb == xp:
        if yb > yp:
            print('la1')
            yb = yb+1 #?
        else:
            print('la2')
            yb = yb-1
    elif yb == yp:
        if xb > xp:
            print('la3')
            xb = xb+1 #?
        else:
            print('la4')
            xb = xb-1
    return xb,yb,xp,yp
        
def pull(xb,yb,xp,yp):
    if xb == xp:
        if yb > yp:
            yb = yb-2 #?
        else:
            yb = yb+2
    elif yb == yp:
        if xb > xp:
            xb = xb-2 #?
        else:
            xb = xb+2  
    return xb,yb,xp,yp
        
'''
def score(xb,yb,xp,yp):      
    if xb == xp:
        if yb > yp:
            print('la1')
            yb = yb+2 #?
        else:
            print('la2')
            yb = yb-2
    elif yb == yp:
        if xb > xp:
            print('la3')
            xb = xb+2 #?
        else:
            print('la4')
            xb = xb-2
    return xb,yb,xp,yp
'''




def together_2goal(xb,yb,xp,yp):
    if xp-xb == 0 and yp-yb == -1:
        print(1)
        if yb<8:
            if xp == 4 or xp == 5:
                xb,yb,xp,yp = kick(xb,yb,xp,yp)
                the_grid(xb,yb,xp,yp)
                together_2goal(xb,yb,xp,yp)
                take_player2ball(xb,yb,xp,yp)
                
            if xp < 4:
                xp = xp-1
                yp = yp+1
                xb,yb,xp,yp = kick(xb,yb,xp,yp)
                the_grid(xb,yb,xp,yp)
                together_2goal(xb,yb,xp,yp)
                take_player2ball(xb,yb,xp,yp)
                
            if xp > 4:
                xp = xp+1
                yp = yp+1
                xb,yb,xp,yp = kick(xb,yb,xp,yp)
                the_grid(xb,yb,xp,yp)
                together_2goal(xb,yb,xp,yp)
                take_player2ball(xb,yb,xp,yp)
        else:
            xb,yb,xp,yp = kick(xb,yb,xp,yp)
            return the_grid(xb,yb,xp,yp)
            
    
    if xp-xb == 0 and yp-yb == 1:
        print(2)
        xb,yb,xp,yp = pull(xb,yb,xp,yp)
        the_grid(xb,yb,xp,yp)
        together_2goal(xb,yb,xp,yp)
        take_player2ball(xb,yb,xp,yp)
    
    if xp-xb == 1 and yp-yb == 0:
        print(3)
        if xb == 4 or xb == 5:
            xp = xp-1
            yp = yp-1
            xb,yb,xp,yp = kick(xb,yb,xp,yp)
            the_grid(xb,yb,xp,yp)
            together_2goal(xb,yb,xp,yp)
            take_player2ball(xb,yb,xp,yp)
        if xp < 4:
            xb,yb,xp,yp = pull(xb,yb,xp,yp) # kick??
            the_grid(xb,yb,xp,yp)
            together_2goal(xb,yb,xp,yp)
            take_player2ball(xb,yb,xp,yp)
        if xp > 4:
            xb,yb,xp,yp = kick(xb,yb,xp,yp)
            the_grid(xb,yb,xp,yp)
            together_2goal(xb,yb,xp,yp)
            take_player2ball(xb,yb,xp,yp)
    
    if xp-xb == -1 and yp-yb == 0:
        print(4)
        if xb == 4 or xb == 5:
            xp = xp+1
            yp = yp-1
            xb,yb,xp,yp = kick(xb,yb,xp,yp)
            the_grid(xb,yb,xp,yp)
            together_2goal(xb,yb,xp,yp)
            take_player2ball(xb,yb,xp,yp)
        if xp < 4:
            xb,yb,xp,yp = kick(xb,yb,xp,yp)
            the_grid(xb,yb,xp,yp)
            together_2goal(xb,yb,xp,yp)
            take_player2ball(xb,yb,xp,yp)
        if xp > 4:
            xb,yb,xp,yp = pull(xb,yb,xp,yp) # kick??
            the_grid(xb,yb,xp,yp)  
            together_2goal(xb,yb,xp,yp)
            take_player2ball(xb,yb,xp,yp)
            
            
            

def the_grid(xb,yb,xp,yp):
    grid = np.ones((10,10))
    grid[xb][yb] = 66
    grid[xp][yp] = 44 
    print(grid)
    
def take_player2ball(xb,yb,xp,yp):
    if xp-xb>0 and yp-yb>0:
        print('1.1')
        yp = yp-1
        xp = xp-1
        the_grid(xb,yb,xp,yp)
        take_player2ball(xb,yb,xp,yp)
        
    elif xp-xb<0 and yp-yb<0:
        print('1.2')
        yp = yp+1
        xp = xp+1
        the_grid(xb,yb,xp,yp)
        take_player2ball(xb,yb,xp,yp)
        
    elif xp-xb==0 and yp-yb<0:
        print('1.3')
        if yp-yb==-1:
            the_grid(xb,yb,xp,yp)
            together_2goal(xb,yb,xp,yp)
            return 
        else:
            yp = yp+1
            the_grid(xb,yb,xp,yp)
            take_player2ball(xb,yb,xp,yp)
            
    elif xp-xb==0 and yp-yb>0:
        print('1.4')
        if yp-yb==1:
            the_grid(xb,yb,xp,yp)
            together_2goal(xb,yb,xp,yp)
            return 
        else:
            yp = yp-1 
            the_grid(xb,yb,xp,yp)
            take_player2ball(xb,yb,xp,yp)
            
    elif xp-xb>0 and yp-yb==0:
        print('1.5')
        if xp-xb==1:
            the_grid(xb,yb,xp,yp)
            together_2goal(xb,yb,xp,yp)
            return 
        else:
            xp = xp-1 
            the_grid(xb,yb,xp,yp)
            take_player2ball(xb,yb,xp,yp)
    
    elif xp-xb<0 and yp-yb==0:
        print('1.6')
        if xp-xb==-1:
            the_grid(xb,yb,xp,yp)
            together_2goal(xb,yb,xp,yp)
            return 
        else:
            xp = xp+1 
            the_grid(xb,yb,xp,yp)
            take_player2ball(xb,yb,xp,yp)
            
#def 


# In[70]:



#print(grid)

#xb = 7#random.randint(0, 9)
#yb = 8

#xp = 7#random.randint(0, 9)
#yp = 0

#print(xp)
#print(grid[xb][yb])
#grid[xb][yb] = 66
#grid[xp][yp] = 44

#print(grid)
#the_grid(xb,yb,xp,yp)

#take_player2ball(xb,yb,xp,yp)


# In[83]:



            
xb = 2
yb = 3
xp = 1
yp = 0
the_grid(xb,yb,xp,yp)
take_player2ball(xb,yb,xp,yp)
together_2goal(xb,yb,xp,yp)

# does kick work?
'''
the_grid(5,4,6,4) 
xb,yb,xp,yp = kick(5,4,6,4)   
print(xb,yb,xp,yp)
the_grid(xb,yb,xp,yp) 
'''
 
#the_grid(4,9,5,9)  


# In[ ]:





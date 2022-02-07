#roojump.py
#make transparent png file goto: https://onlinepngtools.com/create-transparent-png
#kangroo jumps off trampoline: https://www.youtube.com/watch?v=Z3qDprRMdI8
import pygame
import sys
import time
from random import randint as ri
pygame.init()
try:
    jumpSound=pygame.mixer.Sound("jump.wav")
    chewSound=pygame.mixer.Sound("roochew.wav")
    cheerSound=pygame.mixer.Sound("cheer.wav")
    sndCh=pygame.mixer.Channel(0)
    sndCh.set_volume(0.9)
    #pygame.mixer.music.load("ff7choco.mid")
    pygame.mixer.music.load("behappy.mid")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play()
except:
    print('sound file missing.')
screen=pygame.display.set_mode((800,600))
clock=pygame.time.Clock()
font = pygame.font.SysFont(None, 40)
BLACK=(0,0,0)
WHITE=(255,255,255)

#global vars
fileNotFound=False
bx1,bx2,by=0,750,400
x,y=100,400
vx,vy=0,0
a=1.2
ground_friction=0.8 #number between 0 and 1 works best
air_friction=0.8 #number between 0 and 1
lastX,lastY=0,0
rooStep,rooStepLim=0,12
rooState=0 #0 is no move
lastState=0
roo_power_bg=0.1
trampolines=[ ]
trampoline_x,trampoline_y=0,0
start=300
level=-400
maxHeight=0
for i in range(1,20):
    xshift=start + ri(-300,300)
    trampolines+=[(start+xshift, level * i)]

try: #load the files.
    rooImg=pygame.image.load('rooImg.png').convert_alpha()
    rooImg2=pygame.image.load('rooImg2.png').convert_alpha()
    rooImg3=pygame.image.load('rooImg3.png').convert_alpha()
    rooImgL=pygame.transform.flip(rooImg,True,False).convert_alpha()
    rooImg2L=pygame.transform.flip(rooImg2,True,False).convert_alpha()
    rooImg3L=pygame.transform.flip(rooImg3,True,False).convert_alpha()
    backImg=pygame.image.load('seamlessnz.jpg').convert() #get seamless from https://www.imgonline.com.ua/eng/make-seamless-texture.php
    trampolineImg=pygame.image.load('trampoline.png').convert_alpha()
    trampolineImg=pygame.transform.scale(trampolineImg,(100,50)).convert_alpha()
except:
    fileNotFound=True
bg_x_width=backImg.get_rect().width
bg_y_height=backImg.get_rect().height
bg_y_dist=pygame.display.get_window_size()[1]-bg_y_height
bg_x,bg_y=0,bg_y_dist
travel_x,travel_y=0,0
#end of global vars

#draw methods
def draw_background():
    global bg_x
    screen.fill((0,0,0))
    screen.blit(backImg,(bg_x,bg_y))
    screen.blit(backImg,(bg_x+bg_x_width,bg_y))
    screen.blit(backImg,(bg_x-bg_x_width,bg_y))
    if bg_x<-bg_x_width:
        bg_x=0
    if bg_x>bg_x_width:
        bg_x=0
    #print(f'bg_x:{bg_x}')
def draw_roo():
    global x,y,vx,vy,a,bx1,bx2,by,lastX,lastY,rooStep,rooStepLim,bg_x,bg_y,rooState,lastState,travel_x,travel_y,trampolines,trampoline_x,trampoline_y
    #print(x,y,vx,vy,a,bx1,bx2,by,lastX,lastY,rooStep,rooStepLim,bg_x,bg_y,rooState,lastState,travel_x,travel_y,trampolines,trampoline_x,trampoline_y)
    
    #about speed and position
    travel_y+=vy
    travel_x+=vx
    
    x+=vx
    y+=vy
    
    vy+=a

#state of roo, facing left or right
    if lastX>x:
        rooState=2
    elif lastX<x:
        rooState=1
    elif lastState==2 and lastX==x:
        rooState=4
    elif lastState==1 and lastX==x:
        rooState=3

    #check boundary
    if travel_x > bx1:
        bg_x-=vx
        trampoline_x-=vx
    if x < bx1:
        x=bx1
    if travel_x < bx1:
        travel_x = bx1
    if x > bx2//2:
        x=bx2//2
    if y < 0:
        y=0
    if y >= pygame.display.get_window_size()[1]-rooImg.get_rect().height:
        y=pygame.display.get_window_size()[1]-rooImg.get_rect().height
    
    #print(travel_y, bg_y, bg_y_dist)
    if bg_y > bg_y_dist:
        vx*=air_friction
        bg_y-=vy*roo_power_bg
        trampoline_y-=vy
        #print('in air')
    elif y >= by and travel_y >= 0:
        bg_y=bg_y_dist
        trampoline_y=trampolines[0][0]
        vy=0
        y=by
        vx*=ground_friction
        travel_y=0
        #print('on ground')
    elif y >= by and travel_y < 0:
        vx*=air_friction
        bg_y-=vy*roo_power_bg
        trampoline_y-=vy
        #print('still falling')
    else:
        vx*=air_friction
        bg_y-=vy*roo_power_bg
        trampoline_y-=vy
        #print('rebounded')
    if abs(vx) < 1:
        vx=0
        
    #rooState changes image
    if rooState==1:
        if y != by:
            screen.blit(rooImg,(x,y))
        else:
            rooStep+=1
            if rooStep>rooStepLim//2:
                screen.blit(rooImg,(x,y))
            else:
                screen.blit(rooImg2,(x,y))
            rooStep %= rooStepLim
    elif rooState==2:
        if y != by:
            screen.blit(rooImgL,(x,y))
        else:
            rooStep+=1
            if rooStep>rooStepLim//2:
                screen.blit(rooImgL,(x,y))
            else:
                screen.blit(rooImg2L,(x,y))
            rooStep %= rooStepLim
    elif rooState==3:
        screen.blit(rooImg2,(x,y))
    elif rooState==4:
        screen.blit(rooImg2L,(x,y))
        
    #reaction on trampoline
    for i in trampolines:
        if int(x) in range(int(trampoline_x+i[0])-50, int(trampoline_x+i[0])+100) and int(y) in range(int(trampoline_y+i[1])-50, int(trampoline_y+i[1])+50):
            vy=-30
            try: sndCh.play(jumpSound)
            except: pass
    
    #keep track of previous variable
    lastX,lastY,lastState=x,y,rooState

def draw_trampoline():
    for i in trampolines:
        screen.blit(trampolineImg,(trampoline_x+i[0],trampoline_y+i[1]))
    
#add text to screen
def draw_text(screen,x,y,text):
    img = font.render(text, True, WHITE)
    screen.blit(img, (x,y))

while True:
    #handle keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        if y >= by and vy==0:
            vy=-25
            try: sndCh.play(jumpSound)
            except: pass
    if keys[pygame.K_RIGHT]:
        vx+=2
    if keys[pygame.K_DOWN]:
        pass
    if keys[pygame.K_LEFT]:
        vx-=2
    if keys[pygame.K_q]:
        pygame.quit()
        sys.exit()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    draw_background()
    draw_roo()
    draw_trampoline()
    draw_text(screen,10,20,f'Travel:{int(travel_x)/100} m')
    if abs(int(travel_y)) > maxHeight:
        try: sndCh.play(cheerSound)
        except: pass

    maxHeight=max(abs(int(travel_y)),maxHeight)
    draw_text(screen,10,50,f'Height:{abs(int(travel_y))/100} m')
    draw_text(screen,10,80,f'MaxHeight:{maxHeight/100} m')
    pygame.display.flip()
    clock.tick(60)

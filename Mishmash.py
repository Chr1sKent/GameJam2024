import pygame
import random
import time
from pygame.locals import *

pygame.init()
movespeed = 7
scrn = pygame.display.set_mode((1280, 720)) 
planets = [0, 0, 0, 0, 0]
running = True

class Ship:
  def __init__(self, image, xPos, yPos ):
    self.image = image
    self.xPos = xPos
    self.yPos = yPos

class Planet:
  def __init__(self, image, size, pull, x, y):
    self.image = image
    self.size = size
    self.pull = pull
    self.x = x
    self.y = y
    self.orbit = (self.x-size[0]/2, self.y-size[1]/2 ,self.size[0]*1.5,self.size[1]*1.5)


ship_image = pygame.transform.scale(pygame.image.load("ship.png").convert_alpha(), (50, 50))
background_image = pygame.transform.scale(pygame.image.load("Background.png").convert_alpha(), (1280, 720))
planet1_image = pygame.transform.scale(pygame.image.load("planet1.png").convert_alpha(), (50, 50))
planet2_image = pygame.transform.scale(pygame.image.load("planet2.png").convert_alpha(), (50, 50))
planet3_image = pygame.transform.scale(pygame.image.load("planet3.png").convert_alpha(), (50, 50))
planet4_image = pygame.transform.scale(pygame.image.load("planet4.png").convert_alpha(), (50, 50))
planet5_image = pygame.transform.scale(pygame.image.load("planet5.png").convert_alpha(), (50, 50))
planet6_image = pygame.transform.scale(pygame.image.load("planet6.png").convert_alpha(), (50, 50))
planet7_image = pygame.transform.scale(pygame.image.load("planet7.png").convert_alpha(), (50, 50))
explosion_image = pygame.transform.scale(pygame.image.load("bam.png").convert_alpha(), (80, 80))
comet1_image = pygame.transform.scale(pygame.image.load("comet1.png").convert_alpha(), (40, 40))
comet2_image = pygame.transform.scale(pygame.image.load("comet2.png").convert_alpha(), (40, 40))
comet3_image = pygame.transform.scale(pygame.image.load("comet3.png").convert_alpha(), (40, 40))
comet4_image = pygame.transform.scale(pygame.image.load("comet4.png").convert_alpha(), (40, 40))
ship_image_right = pygame.transform.rotate(ship_image, 270)
ship_image_left = pygame.transform.rotate(ship_image, 90)
ship_image_up = pygame.transform.rotate(ship_image, 0)
ship_image_down = pygame.transform.rotate(ship_image, 180)
ship_image_ne = pygame.transform.rotate(ship_image, 315)
ship_image_se = pygame.transform.rotate(ship_image, 225)
ship_image_sw = pygame.transform.rotate(ship_image, 135)
ship_image_nw = pygame.transform.rotate(ship_image, 45)
ship = Ship(ship_image, 100, 100)
clock = pygame.time.Clock()

def border(ship):
  if ship.xPos > 1230:
    ship.xPos -= movespeed
  elif ship.xPos < 10:
    ship.xPos += movespeed
  elif ship.yPos > 650:
    ship.yPos -= movespeed
  elif ship.yPos < 10:
    ship.yPos += movespeed


def move(ship):
  keys = pygame.key.get_pressed()
  x = 0
  y = 0
  w = False
  a = False
  s = False
  d = False
  if keys[pygame.K_a]:
    x -= movespeed
    a = True
  if keys[pygame.K_d]:
    x += movespeed
    d = True
  if keys[pygame.K_w]:
    y -= movespeed
    w = True
  if keys[pygame.K_s]:
    y += movespeed
    s = True
  dist = pygame.Vector2(x,y)
  if dist.x != 0 and dist.y != 0:
    dist.scale_to_length(movespeed)
  player_vect = pygame.Vector2(ship.xPos,ship.yPos)
  player_vect = player_vect + dist
  ship.xPos,ship.yPos = player_vect.x,player_vect.y
  if w and d:
      ship.image = ship_image_ne
  elif s and d:
      ship.image = ship_image_se
  elif s and a:
      ship.image = ship_image_sw
  elif w and a:
      ship.image = ship_image_nw
  elif w:
      ship.image = ship_image_up
  elif s:
      ship.image = ship_image_down
  elif d:
      ship.image = ship_image_right
  elif a:
      ship.image = ship_image_left


def planetCreate(planets):
  planetImg = [planet1_image, planet2_image, planet3_image, planet4_image, planet5_image, planet6_image, planet7_image]
  lastY = 0
  for i in range(len(planets)):
    x = random.randint(1280,1480)
    y = random.randint(75,650)
    if planets[i] == 0:
      size = random.randint(25, 250)
      imageChoice = random.choice(planetImg)
      planets[i] = Planet(imageChoice, (size, size), size / 50, x, y)
      planets[i].image = pygame.transform.scale(imageChoice, (size, size))
      if -50 < lastY - y < 50:
        planets[i].y += random.choice([-100,100])
  return planets

def planetDelete(planets):
  planets[i] = 0
  return planets

count = 0
stage = 0
score = 0

class Comet():
    def __init__(self, width, height,cometTypes):
        self.comets = cometTypes
        self.width,self.height = width,height
        self.spawn()
        self.rect = (self.pos.x-width/2,self.pos.y-height/2,width,height)
        self.onScreen = False

    def Velocity(self):
        if self.wall == 1:
            x = random.randint(-10,10)
            y = random.randint(0,10)
        elif self.wall == 2:
            x = random.randint(-10,10)
            y = random.randint(-10,0)
        elif self.wall == 3:
            x = random.randint(0,10)
            y = random.randint(-10,10)
        else:
            x = random.randint(-10,10)
            y = random.randint(-10,0)
        return x,y


    def move(self):
        self.pos.x += self.velox
        self.pos.y += self.veloy
        self.rect = (self.pos.x-self.width/2,self.pos.y-self.height/2,self.width,self.height)
        self.screenCheck()

    def spawn(self):
        self.wall = random.randint(0,3)
        if self.wall == 1:
            x = random.randint(500,1280)
            y = 0
        elif self.wall == 2:
            x = random.randint(500,1280)
            y = 720
        elif self.wall == 3:
            x = 0
            y = random.randint(250,720)
        else:
            x = 1280
            y = random.randint(250,720)
        self.pos = pygame.Vector2(x,y)
        self.velox,self.veloy = self.Velocity()
        self.image = self.comets[random.randint(0,9)]


    def drawComet(self):
        scrn.blit(self.image, (self.rect[0], self.rect[1]))


    def screenCheck(self):
        if (self.pos.x <= 0 or self.pos.x >= 1280) or (self.pos.y <= 0 or self.pos.y >= 720):
            self.onScreen = False
    
    def deleteComet(self):
        self.spawn()
        self.drawComet()
        self.onScreen = True



class CometArray():
    def __init__(self):
        self.cArray = self.setArray()
    
    
    def setArray(self):
        cometTypes = [comet1_image,comet2_image,comet3_image,comet1_image,comet1_image,comet1_image,comet1_image,comet4_image,comet1_image,comet1_image] 
        comet1 = Comet(40,40,cometTypes)
        comet2 = Comet(40,40,cometTypes)
        comet3 = Comet(40,40,cometTypes)
        comet4 = Comet(40,40,cometTypes)
        comet5 = Comet(40,40,cometTypes)
        cArray = [comet1, comet2 , comet3 , comet4, comet5]
        return cArray
    

    def cometShipCollision(self, playerRect,ship):
        for comet in self.cArray:
            Rect = pygame.Rect(comet.rect)
            collide = pygame.Rect.colliderect(Rect, playerRect)
            if collide:
                ship.image = explosion_image
                return 1
        return 0

    def cometControl(self):
        for comet in self.cArray:
            if comet.onScreen == False:
                comet.deleteComet()
            comet.move()
            comet.drawComet()
    

Comets = CometArray()

def gravity(playerRect, orbitRect, orbitCentre ,pull):
    collide = pygame.Rect.colliderect(orbitRect, playerRect)
    if collide:
        orbitVec = pygame.Vector2(orbitCentre[0],orbitCentre[1])
        playerVec = pygame.Vector2(playerRect.x,playerRect.y)
        playerVec.move_towards_ip(orbitVec,pull)
        ship.xPos,ship.yPos = playerVec.x,playerVec.y

def scoring():
   score = pygame.time.get_ticks()//1000
   text = "Time Alive: " + str(score)
   font = pygame.font.SysFont("Arial", 25)
   txtsurf = font.render(text, True, "white")
   scrn.blit(txtsurf,(50,25))
   return score

def gameOver(score):
   text1 = "Time Survived: " + str(score)
   text2 = "GAME OVER"
   font1 = pygame.font.SysFont("Arial", 35)
   font2 = pygame.font.SysFont("Arial", 65)
   failsurf = font2.render(text2, True, "white")
   scoresurf = font1.render(text1, True, "white")
   scrn.blit(scoresurf,(540,400))
   scrn.blit(failsurf,(480,300))
    
while running: 
  if stage == 0:
    pygame.display.flip()
    scrn.fill((0, 0, 0))
    scrn.blit(background_image,(0, 0))
    scrn.blit(ship.image,(ship.xPos, ship.yPos))
    playerRect = pygame.Rect(ship.xPos, ship.yPos, 50, 50)
    if stage == 0:
      score = scoring()

    Comets.cometControl()
    planets = planetCreate(planets)
    stage = Comets.cometShipCollision(playerRect, ship)

    for i in range (5):
      scrn.blit(planets[i].image, (planets[i].x, planets[i].y))
      planetRect = pygame.Rect(planets[i].x + planets[i].size[0]*0.07, planets[i].y + planets[i].size[0]*0.07, planets[i].size[0]*0.9, planets[i].size[1]*0.9)
      planets[i].x -=5 / planets[i].pull
      orbitRect = pygame.Rect(planets[i].x-planets[i].size[0]/2, planets[i].y-planets[i].size[1]/2 ,planets[i].size[0]*2,planets[i].size[1]*2)
      orbitCentre = (planets[i].x + planets[i].size[0]/2,planets[i].y + planets[i].size[1]/2 )
      gravity(playerRect, orbitRect,orbitCentre,planets[i].pull)
      if planets[i].x < -260:
        planetDelete(planets)
      collide = pygame.Rect.colliderect(planetRect, playerRect)
      if collide:
        ship.image = explosion_image
        stage = 1
    move(ship)
    border(ship)
  if stage ==  1:
    ship.image = explosion_image
    ship.yPos += 7.5
    pygame.display.flip()
    scrn.fill((0, 0, 0))
    scrn.blit(background_image,(0, 0))
    scrn.blit(ship.image,(ship.xPos, ship.yPos))
    gameOver(score)
    restart = pygame.key.get_pressed()
    if restart[pygame.K_r]:
      stage = 0
      ship.xPos = 100
      ship.yPos = 100
      ship.image = ship_image

  clock.tick(30)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
import os, sys
import pygame
from pygame.locals import *

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_plain_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image
  
def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', wav
        raise SystemExit, message
    return sound

class Globals:
  def __init__(self):
    # Visible screen
    self.ulx = 0
    self.uly = 0

    self.reso_x = 1400
    self.reso_y = 1050

    self.lrx = self.reso_x
    self.lry = self.reso_y

    # Whole playground
    self.wholeLrx = 5000
    self.wholeLry = 5000

class Building(pygame.sprite.Sprite):
    def __init__(self):
      pygame.sprite.Sprite.__init__(self) #call Sprite initializer

      self.image, self.rect = load_image('pimp.bmp', -1)

      screen = pygame.display.get_surface()
      self.area = screen.get_rect()
      self.rect.topleft = -100,-100

      self.x = globals.reso_x
      self.y = globals.reso_y
      self.grounded = 1
      self.movement = 0

    def check(self):
      # Check if this object is within the visible screen
      if (self.x - globals.ulx > 0, self.x < globals.lrx):
        if (self.y - globals.lry > 0, self.y < globals.lry):
          self.rect.topleft = self.x - globals.ulx, self.y - globals.uly
          return self

class Shot(pygame.sprite.Sprite):
    def __init__(self, x, y, facing, center):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer

        self.image, self.rect = load_image('shot.bmp', -1)

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

        self.x = x
        self.y = y
        self.move = 0
        self.facing = facing
        self.rect.center = center
        self.speed = 70
        self.grounded = 0

    def update(self):
      mod = float(self.speed) / 100

      # Movement
      if self.facing < 91:
        self.x += self.facing * mod
        self.y += (self.facing - 90) * mod
      elif self.facing < 181:
        self.x += (90 - (self.facing - 90)) * mod
        self.y += (self.facing - 90) * mod
      elif self.facing < 271:
        self.x += (180 - self.facing) * mod
        self.y += (90 + 180 - self.facing) * mod
      elif self.facing < 360 or self.facing == 0:
        self.x += -(360 - self.facing) * mod
        self.y += -(90 + -(360 - self.facing)) * mod

      # Check if this object is out of the whole playground
      if self.x > globals.wholeLrx or self.x < 0 or self.y > globals.wholeLry or self.y < 0:
        allshots.remove(self)

      # Check if this object is within the visible screen
      if (self.x - globals.ulx > 0, self.x < globals.lrx):
        if (self.y - globals.lry > 0, self.y < globals.lry):
            self.rect.topleft = self.x - globals.ulx, self.y - globals.uly 

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer

        self.image, self.rect = load_image('a90.bmp', -1)
        self.img = {}
        self.grounded = 0

        self.files = ['a0.bmp', 'a1.bmp','a2.bmp','a3.bmp','a4.bmp','a5.bmp','a6.bmp','a7.bmp','a8.bmp','a9.bmp','a10.bmp','a11.bmp','a12.bmp','a13.bmp','a14.bmp','a15.bmp','a16.bmp','a17.bmp','a18.bmp','a19.bmp','a20.bmp','a21.bmp','a22.bmp','a23.bmp','a24.bmp','a25.bmp','a26.bmp','a27.bmp','a28.bmp','a29.bmp','a30.bmp','a31.bmp','a32.bmp','a33.bmp','a34.bmp','a35.bmp','a36.bmp','a37.bmp','a38.bmp','a39.bmp','a40.bmp','a41.bmp','a42.bmp','a43.bmp','a44.bmp','a45.bmp','a46.bmp','a47.bmp','a48.bmp','a49.bmp','a50.bmp','a51.bmp','a52.bmp','a53.bmp','a54.bmp','a55.bmp','a56.bmp','a57.bmp','a58.bmp','a59.bmp','a60.bmp','a61.bmp','a62.bmp','a63.bmp','a64.bmp','a65.bmp','a66.bmp','a67.bmp','a68.bmp','a69.bmp','a70.bmp','a71.bmp','a72.bmp','a73.bmp','a74.bmp','a75.bmp','a76.bmp','a77.bmp','a78.bmp','a79.bmp','a80.bmp','a81.bmp','a82.bmp','a83.bmp','a84.bmp','a85.bmp','a86.bmp','a87.bmp','a88.bmp','a89.bmp','a90.bmp','a91.bmp','a92.bmp','a93.bmp','a94.bmp','a95.bmp','a96.bmp','a97.bmp','a98.bmp','a99.bmp','a100.bmp','a101.bmp','a102.bmp','a103.bmp','a104.bmp','a105.bmp','a106.bmp','a107.bmp','a108.bmp','a109.bmp','a110.bmp','a111.bmp','a112.bmp','a113.bmp','a114.bmp','a115.bmp','a116.bmp','a117.bmp','a118.bmp','a119.bmp','a120.bmp','a121.bmp','a122.bmp','a123.bmp','a124.bmp','a125.bmp','a126.bmp','a127.bmp','a128.bmp','a129.bmp','a130.bmp','a131.bmp','a132.bmp','a133.bmp','a134.bmp','a135.bmp','a136.bmp','a137.bmp','a138.bmp','a139.bmp','a140.bmp','a141.bmp','a142.bmp','a143.bmp','a144.bmp','a145.bmp','a146.bmp','a147.bmp','a148.bmp','a149.bmp','a150.bmp','a151.bmp','a152.bmp','a153.bmp','a154.bmp','a155.bmp','a156.bmp','a157.bmp','a158.bmp','a159.bmp','a160.bmp','a161.bmp','a162.bmp','a163.bmp','a164.bmp','a165.bmp','a166.bmp','a167.bmp','a168.bmp','a169.bmp','a170.bmp','a171.bmp','a172.bmp','a173.bmp','a174.bmp','a175.bmp','a176.bmp','a177.bmp','a178.bmp','a179.bmp','a180.bmp','a181.bmp','a182.bmp','a183.bmp','a184.bmp','a185.bmp','a186.bmp','a187.bmp','a188.bmp','a189.bmp','a190.bmp','a191.bmp','a192.bmp','a193.bmp','a194.bmp','a195.bmp','a196.bmp','a197.bmp','a198.bmp','a199.bmp','a200.bmp','a201.bmp','a202.bmp','a203.bmp','a204.bmp','a205.bmp','a206.bmp','a207.bmp','a208.bmp','a209.bmp','a210.bmp','a211.bmp','a212.bmp','a213.bmp','a214.bmp','a215.bmp','a216.bmp','a217.bmp','a218.bmp','a219.bmp','a220.bmp','a221.bmp','a222.bmp','a223.bmp','a224.bmp','a225.bmp','a226.bmp','a227.bmp','a228.bmp','a229.bmp','a230.bmp','a231.bmp','a232.bmp','a233.bmp','a234.bmp','a235.bmp','a236.bmp','a237.bmp','a238.bmp','a239.bmp','a240.bmp','a241.bmp','a242.bmp','a243.bmp','a244.bmp','a245.bmp','a246.bmp','a247.bmp','a248.bmp','a249.bmp','a250.bmp','a251.bmp','a252.bmp','a253.bmp','a254.bmp','a255.bmp','a256.bmp','a257.bmp','a258.bmp','a259.bmp','a260.bmp','a261.bmp','a262.bmp','a263.bmp','a264.bmp','a265.bmp','a266.bmp','a267.bmp','a268.bmp','a269.bmp','a270.bmp','a271.bmp','a272.bmp','a273.bmp','a274.bmp','a275.bmp','a276.bmp','a277.bmp','a278.bmp','a279.bmp','a280.bmp','a281.bmp','a282.bmp','a283.bmp','a284.bmp','a285.bmp','a286.bmp','a287.bmp','a288.bmp','a289.bmp','a290.bmp','a291.bmp','a292.bmp','a293.bmp','a294.bmp','a295.bmp','a296.bmp','a297.bmp','a298.bmp','a299.bmp','a300.bmp','a301.bmp','a302.bmp','a303.bmp','a304.bmp','a305.bmp','a306.bmp','a307.bmp','a308.bmp','a309.bmp','a310.bmp','a311.bmp','a312.bmp','a313.bmp','a314.bmp','a315.bmp','a316.bmp','a317.bmp','a318.bmp','a319.bmp','a320.bmp','a321.bmp','a322.bmp','a323.bmp','a324.bmp','a325.bmp','a326.bmp','a327.bmp','a328.bmp','a329.bmp','a330.bmp','a331.bmp','a332.bmp','a333.bmp','a334.bmp','a335.bmp','a336.bmp','a337.bmp','a338.bmp','a339.bmp','a340.bmp','a341.bmp','a342.bmp','a343.bmp','a344.bmp','a345.bmp','a346.bmp','a347.bmp','a348.bmp','a349.bmp','a350.bmp','a351.bmp','a352.bmp','a353.bmp','a354.bmp','a355.bmp','a356.bmp','a357.bmp','a358.bmp','a359.bmp','a360.bmp']

        i = 0
        for file in self.files:
          self.img[i] = load_plain_image(file)
          i += 1

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.center = globals.reso_x / 2, globals.reso_y / 2
        self.movement = 0
        self.facing = 90

        # Turn rate means how much the ship is turning left(negative value means
        # it's turning right
        self.turn_rate = 0
        self.turn_rate_accel = 2
        self.turn_rate_max = 10
        self.turn_rate_min = -10

        self.x = globals.reso_x / 2
        self.y = globals.reso_y / 2

    def turn(self,direction):
      if direction == 'l':
        self.turn_rate += self.turn_rate_accel
        if self.turn_rate > self.turn_rate_max: 
          self.turn_rate = self.turn_rate_max

        self.facing -= self.turn_rate
      elif direction == 'r':
        self.turn_rate -= self.turn_rate_accel
        if self.turn_rate < self.turn_rate_min:
          self.turn_rate = self.turn_rate_min

        self.facing -= self.turn_rate

      if self.facing > 359:
        self.facing = 0

      if self.facing < 0:
        self.facing = 359

      self.image = self.img[self.facing]

    def shoot(self):
      # Create a new shot and assign it the properties of the ship
      shot = Shot(self.x, self.y, self.facing, self.rect.center)
      return shot

    def accel(self,movement):
      if self.movement < 45:
        self.movement += movement

    def brake(self,movement):
      self.movement -= movement
      if self.movement < -30:
        self.movement = -10

    def update(self):
      self.image = self.img[self.facing]
      mod = float(self.movement) / 100

      # Movement
      if self.facing < 91:
        self.x += self.facing * mod
        self.y += (self.facing - 90) * mod
        globals.ulx += self.facing * mod
        globals.uly += (self.facing - 90) * mod
      elif self.facing < 181:
        self.x += (90 - (self.facing - 90)) * mod
        self.y += (self.facing - 90) * mod
        globals.ulx += (90 - (self.facing - 90)) * mod
        globals.uly += (self.facing - 90) * mod
      elif self.facing < 271:
        self.x += (180 - self.facing) * mod
        self.y += (90 + 180 - self.facing) * mod
        globals.ulx += (180 - self.facing) * mod
        globals.uly += (90 + 180 - self.facing) * mod
      elif self.facing < 360 or self.facing == 0:
        self.x += -(360 - self.facing) * mod
        self.y += -(90 + -(360 - self.facing)) * mod
        globals.ulx += -(360 - self.facing) * mod
        globals.uly += -(90 + -(360 - self.facing)) * mod

      # Check if this object is out of the whole playground
      if self.x > globals.wholeLrx or self.x < 0:
        allsprites.remove(self)
        sys.exit(2)

      # Move turn-rate back towards default
      if self.turn_rate > 0:
        self.turn_rate -= 1
      elif self.turn_rate < 0:
        self.turn_rate += 1

def checkCollision(a, b):
  # Right now everything is a square

  if a.x < b.x:
    if a.y < b.y:
      if a.rect.bottomright[0] > b.rect.topleft[0] and a.rect.bottomright[1] > b.rect.topleft[1]:
        if a.grounded == 0:
          a.movement = 0
          a.x -= 10
          a.y -= 10
        elif b.grounded == 0:
          b.movement = 0
          allshots.remove(b)
          b.x -= 10
          b.y -= 10
    else:
      if a.rect.topright[0] > b.rect.bottomleft[0] and a.rect.topright[1] < b.rect.bottomleft[1]:
        if a.grounded == 0:
          a.movement = 0
          a.x -= 10
          a.y += 10
        elif b.grounded == 0:
          b.movement = 0
          allshots.remove(b)
          b.x -= 10
          b.y += 10
        else:
          a.movement = 0
          a.x -= 10
          a.y += 10
          b.movement = 0
          allshots.remove(b)
          b.x -= 10
          b.y += 10

  elif a.x > b.x:
    if a.y > b.y:
      if a.rect.topleft[0] < b.rect.bottomright[0] and a.rect.topleft[1] < b.rect.bottomright[1]:
        if a.grounded == 0:
          a.movement = 0
          a.x += 10
          a.y += 10
        elif b.grounded == 0:
          b.movement = 0
          allshots.remove(b)
          b.x += 10
          b.y += 10
        else:
          a.movement = 0
          a.x += 10
          a.y += 10
          b.movement = 0
          allshots.remove(b)
          b.x += 10
          b.y += 10
    else:
      if a.rect.bottomleft[0] < b.rect.topright[0] and a.rect.bottomleft[1] > b.rect.topright[1]:
        if a.grounded == 0:
          a.movement = 0
          a.x += 10
          a.y -= 10
        elif b.grounded == 0:
          b.movement = 0
          allshots.remove(b)
          b.x += 10
          b.y -= 10
        else:
          b.movement = 0
          allshots.remove(b)
          b.x += 10
          b.y -= 10
          a.movement = 0
          a.x += 10
          a.y -= 10

def bounceObject( obj, facing ):
  # Change object's facing determined by facing

  if obj.facing < 45:
      obj.facing -= 20
  elif obj.facing < 90:
      obj.facing += 20
  elif obj.facing < 135:
      obj.facing -= 20
  elif obj.facing < 180:
      obj.facing += 20
  elif obj.facing < 225:
      obj.facing -= 20
  elif obj.facing < 270:
      obj.facing += 20
  elif obj.facing < 315 or obj.facing == 0:
      obj.facing -= 20
  else:
      obj.facing += 20

  if obj.facing > 359:
    obj.facing -= 360
  elif obj.facing < 0:
    obj.facing += 360

def checkPlayerCollision(a, b):
  # Right now everything is a square

  impact = a.movement + b.movement

  if a.x < b.x:
    if a.y < b.y:
      if a.rect.bottomright[0] > b.rect.topleft[0] and a.rect.bottomright[1] > b.rect.topleft[1]:
        # a impacts from up left
        if a.grounded == 0:
          a.movement /= 2
          a.x -= impact
          a.y -= impact
          
          # Check if this is a direct hit
          if a.facing < 90:
            a.facing -= 10
          elif a.facing > 180:
            a.facing += 10
          else:
            bounceObject( a, 135)

          globals.ulx -= impact
          globals.uly -= impact
        elif b.grounded == 0:
          b.movement = 0
          b.x -= impact
          b.y -= impact
          globals.ulx -= impact
          globals.uly -= impact
        else:
          a.movement /= 2
          a.x -= impact
          a.y -= impact
          globals.ulx -= impact
          globals.uly -= impact
          b.movement = 0
          b.x -= impact
          b.y -= impact
          globals.ulx -= impact
          globals.uly -= impact
    else:
      if a.rect.topright[0] > b.rect.bottomleft[0] and a.rect.topright[1] < b.rect.bottomleft[1]:
        # a impacts from down left
        if a.grounded == 0:
          a.movement /= 2
          a.x -= impact
          a.y += impact
          
          bounceObject( a, 45 )

          globals.ulx -= impact
          globals.uly += impact
        elif b.grounded == 0:
          b.movement = 0
          b.x -= impact
          b.y += impact
          globals.ulx -= impact
          globals.uly += impact
        else:
          a.movement /= 2
          a.x -= impact
          a.y += impact
          globals.ulx -= impact
          globals.uly += impact
          b.movement = 0
          b.x -= impact
          b.y += impact
          globals.ulx -= impact
          globals.uly += impact

  elif a.x > b.x:
    if a.y > b.y:
      if a.rect.topleft[0] < b.rect.bottomright[0] and a.rect.topleft[1] < b.rect.bottomright[1]:
        # a impacts from bottom right
        if a.grounded == 0:
          a.movement /= 2
          a.x += impact
          a.y += impact

          bounceObject( a, 315 )

          globals.ulx += impact
          globals.uly += impact
        elif b.grounded == 0:
          b.movement = 0
          b.x += impact
          b.y += impact
          globals.ulx += impact
          globals.uly += impact
        else:
          a.movement /= 2
          a.x += impact
          a.y += impact
          globals.ulx += impact
          globals.uly += impact
          b.movement = 0
          b.x += impact
          b.y += impact
          globals.ulx += impact
          globals.uly += impact
    else:
      if a.rect.bottomleft[0] < b.rect.topright[0] and a.rect.bottomleft[1] > b.rect.topright[1]:
        # a impacts from up right
        if a.grounded == 0:
          a.movement /= 2
          a.x += impact
          a.y -= impact

          bounceObject( a, 225 )

          globals.ulx += impact
          globals.uly -= impact
        elif b.grounded == 0:
          b.movement = 0
          b.x += impact
          b.y -= impact
          globals.ulx += impact
          globals.uly -= impact
        else:
          b.movement = 0
          b.x += impact
          b.y -= impact
          globals.ulx += impact
          globals.uly -= impact
          a.movement = 0
          a.x += impact
          a.y -= impact
          globals.ulx += impact
          globals.uly -= impact

pygame.init()
globals = Globals()
screen = pygame.display.set_mode((globals.reso_x, globals.reso_y))
pygame.display.set_caption('Ape')
pygame.mouse.set_visible(0)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))

if pygame.font:
    font = pygame.font.Font(None, 36)
    text = font.render("Ape", 1, (10, 10, 10))
    textpos = text.get_rect(centerx=background.get_width()/2)
    background.blit(text, textpos)

screen.blit(background, (0, 0))
pygame.display.flip()

ship = Ship()
building = Building()

# TODO Tidy up this shot-initialization

allsprites = pygame.sprite.RenderPlain((ship))
allshots = pygame.sprite.RenderPlain()

clock = pygame.time.Clock()

# This has no meaning now, it seems
pygame.key.set_repeat(50)

# Game loop
while 1:
    clock.tick(30)

    pressed = pygame.key.get_pressed()
    if pressed[K_ESCAPE] == 1:
      sys.exit(2)
    if pressed[K_a] == 1:
      ship.turn('l')
    if pressed[K_d] == 1:
      ship.turn('r')
    if pressed[K_w] == 1:
      ship.accel(5)
    if pressed[K_s] == 1:
      ship.brake(5)
    if pressed[K_h] == 1:
      allshots.add(ship.shoot())

    for event in pygame.event.get():
      if event.type == QUIT:
          sys.exit(2)

    # Check if there are objects inside the visible screen
    a = building.check()
    if a:
      allsprites.add(a)


# TODO Intelligent checking for shots, sprites and all
    for object in allsprites:
      # Check player collisions
      checkPlayerCollision(ship, object)

      # Check shot collisions
      if object is not ship:
        for a_shot in allshots:
          checkCollision(object,a_shot)

    allsprites.update()
    allshots.update()

    screen.blit(background, (0, 0))
    allsprites.draw(screen)
    allshots.draw(screen)
    pygame.display.flip()

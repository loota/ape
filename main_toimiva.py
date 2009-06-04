import os, sys
import pygame
import math
import time
import random
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

class Body(pygame.sprite.Sprite):
  def __init__(self):
    self.x = 0
    self.y = 0
    self.velocity = 0
    self.facing = 0
    self.mass = 0

class Terrain(Body):
  def __init__(self, image, x, y, elevation):
    Body.__init__(self)
    pygame.sprite.Sprite.__init__(self) #call Sprite initializer
    self.image, self.rect = load_image(image, -1)
    screen = pygame.display.get_surface()
    self.area = screen.get_rect()
    self.x = x
    self.y = y
    self.grounded = 1
    self.hit_points = 10
    self.elevation = elevation

  def update(self):
    self.check()

  def check(self):
    # Check if this object is within the visible screen
    if (self.x - globals.ulx > 0, self.x < globals.lrx):
      if (self.y - globals.lry > 0, self.y < globals.lry):
        self.rect.topleft = self.x - globals.ulx, self.y - globals.uly
        return self

class CrossHairs(pygame.sprite.Sprite):
    def __init__(self,owner):
      pygame.sprite.Sprite.__init__(self) #call Sprite initializer
      self.image, self.rect = load_image('crosshairs.bmp', -1)
      screen = pygame.display.get_surface()
      self.area = screen.get_rect()
      self.rect.topleft = 800,500

      self.x = 500
      self.y = 500
      self.distance = 250
      self.owner = owner

    def update(self):
      mod = self.owner.velocity * 10
      if mod > (globals.reso_y / 2):
        mod = globals.reso_y / 2

      self.x = math.sin(math.radians(self.owner.facing)) * mod
      self.y = -math.cos(math.radians(self.owner.facing)) * mod

      self.rect.center = (globals.center[0] + self.x, globals.center[1] + self.y)

class Globals:
  def __init__(self):
    # Visible screen
    self.ulx = 0
    self.uly = 0

    self.reso_x = 1024
    self.reso_y = 768

    self.lrx = self.reso_x
    self.lry = self.reso_y
    self.center = (self.reso_x / 2, self.reso_y / 2)

    # Whole playground
    self.wholeLrx = 5000
    self.wholeLry = 5000

    self.bg_color = (255,255,255)
    self.compensation = 400

class Building(pygame.sprite.Sprite):
    def __init__(self, x, y, hit_points):
      pygame.sprite.Sprite.__init__(self) #call Sprite initializer

      self.image, self.rect = load_image('pimp.bmp', -1)

      screen = pygame.display.get_surface()
      self.area = screen.get_rect()
      self.rect.topleft = -100,-100

      self.x = x
      self.y = y
      self.grounded = 1
      self.velocity = 0
      self.hit_points = hit_points
      self.elevation = 1

    def check(self):
      # Check if this object is within the visible screen
      if (self.x - globals.ulx > 0, self.x < globals.lrx):
        if (self.y - globals.lry > 0, self.y < globals.lry):
          self.rect.topleft = self.x - globals.ulx, self.y - globals.uly
          return self

    def checkStatus(self):
      if self.hit_points < 0:
        pass

class GroundBattery(Building):
  def __init__(self, x, y, hit_points):
    Building.__init__(self, x, y, hit_points)
    self.dest_img = load_plain_image('explosion.bmp')

  def update(self):
    self.checkStatus()
    if self.hit_points > 0:
      
      distance_x = ship.x - self.x
      distance_y = ship.y - self.y

      # Tracking
      self.facing = math.degrees(math.atan(distance_x / distance_y))
      if distance_x < 0:
        # Other object is left of us
        if distance_y < 0:
          # Other object is left and above us
          distance_y = -distance_y
          distance_x = -distance_x
          self.facing = 360 - math.degrees(math.atan(distance_x / distance_y))

        elif distance_y > 0:
          #Other object is left and below of us
          distance_x = -distance_x
          self.facing = 180 + math.degrees(math.atan(distance_x / distance_y))

      else:
      # Other object is right of us
        if distance_y < 0:
          # Other object is right and above us
          distance_y = -distance_y
          self.facing = math.degrees(math.atan(distance_x / distance_y))

        elif distance_y > 0:
          #Other object is right and below of us
          self.facing = 180 - math.degrees(math.atan(distance_x / distance_y))

      if random.randrange(20) == 1:
        allshots.add(self.shoot())

  def shoot(self):
    shot = Shot(self.x, self.y, self.facing, self.rect.center, 40)
    return shot

  def checkStatus(self):
    if self.hit_points < 1:
      self.image = self.dest_img

class Shot(pygame.sprite.Sprite):
    def __init__(self, x, y, facing, center, velocity):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer

        self.image, self.rect = load_image('shot.bmp', -1)
        self.hit_image = load_plain_image('hit.bmp', -1)

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

        self.x = x
        self.y = y

        self.move = 0
        self.facing = facing
        self.rect.center = center
        self.velocity = velocity
        self.grounded = 0
        self.damage = 1
        self.disappear_timer = 0
        self.active = 1

        # Move the shot immediately so it won't hit the ship that launched it
        self.update()

    def explode(self):
      self.disappear_timer = 10
      self.image = self.hit_image
      self.active = 0
      self.velocity = 0

    def update(self):
      mod = float(self.velocity)

      if self.disappear_timer > 0:
        self.disappear_timer -= 1
        if self.disappear_timer % 2 == 0:
          self.x += random.randrange(-10, 10)
        else:
          self.y += random.randrange(-10, 10)

        if self.disappear_timer < 1:
          if self.active == 0:
            allshots.remove(self)

      # Movement
      if self.active > 0:
        self.x += math.sin(math.radians(self.facing)) * mod
        self.y += -math.cos(math.radians(self.facing)) * mod

      # Check if this object is out of the whole playground
      if self.x > globals.wholeLrx or self.x < 0 or self.y > globals.wholeLry or self.y < 0:
        allshots.remove(self)

      # Check if this object is within the visible screen
      if (self.x - globals.ulx > 0, self.x < globals.lrx):
        if (self.y - globals.lry > 0, self.y < globals.lry):
            self.rect.topleft = self.x - globals.ulx, self.y - globals.uly 

class Missile(Shot):
  def __init__(self, x, y, facing, center, velocity):
    Shot.__init__(self, x, y, facing, center, velocity)
    self.image = load_plain_image('missile.bmp', -1)
    self.damage = 10
    self.hit_image = load_plain_image('explosion1.bmp', -1)

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer

        self.image, self.rect = load_image('a90.bmp', -1)
        self.img = {}
        self.grounded = 0
        self.hit_points = 20
        self.dest_timer = 100

        self.files = ['a0.bmp', 'a1.bmp','a2.bmp','a3.bmp','a4.bmp','a5.bmp','a6.bmp','a7.bmp','a8.bmp','a9.bmp','a10.bmp','a11.bmp','a12.bmp','a13.bmp','a14.bmp','a15.bmp','a16.bmp','a17.bmp','a18.bmp','a19.bmp','a20.bmp','a21.bmp','a22.bmp','a23.bmp','a24.bmp','a25.bmp','a26.bmp','a27.bmp','a28.bmp','a29.bmp','a30.bmp','a31.bmp','a32.bmp','a33.bmp','a34.bmp','a35.bmp','a36.bmp','a37.bmp','a38.bmp','a39.bmp','a40.bmp','a41.bmp','a42.bmp','a43.bmp','a44.bmp','a45.bmp','a46.bmp','a47.bmp','a48.bmp','a49.bmp','a50.bmp','a51.bmp','a52.bmp','a53.bmp','a54.bmp','a55.bmp','a56.bmp','a57.bmp','a58.bmp','a59.bmp','a60.bmp','a61.bmp','a62.bmp','a63.bmp','a64.bmp','a65.bmp','a66.bmp','a67.bmp','a68.bmp','a69.bmp','a70.bmp','a71.bmp','a72.bmp','a73.bmp','a74.bmp','a75.bmp','a76.bmp','a77.bmp','a78.bmp','a79.bmp','a80.bmp','a81.bmp','a82.bmp','a83.bmp','a84.bmp','a85.bmp','a86.bmp','a87.bmp','a88.bmp','a89.bmp','a90.bmp','a91.bmp','a92.bmp','a93.bmp','a94.bmp','a95.bmp','a96.bmp','a97.bmp','a98.bmp','a99.bmp','a100.bmp','a101.bmp','a102.bmp','a103.bmp','a104.bmp','a105.bmp','a106.bmp','a107.bmp','a108.bmp','a109.bmp','a110.bmp','a111.bmp','a112.bmp','a113.bmp','a114.bmp','a115.bmp','a116.bmp','a117.bmp','a118.bmp','a119.bmp','a120.bmp','a121.bmp','a122.bmp','a123.bmp','a124.bmp','a125.bmp','a126.bmp','a127.bmp','a128.bmp','a129.bmp','a130.bmp','a131.bmp','a132.bmp','a133.bmp','a134.bmp','a135.bmp','a136.bmp','a137.bmp','a138.bmp','a139.bmp','a140.bmp','a141.bmp','a142.bmp','a143.bmp','a144.bmp','a145.bmp','a146.bmp','a147.bmp','a148.bmp','a149.bmp','a150.bmp','a151.bmp','a152.bmp','a153.bmp','a154.bmp','a155.bmp','a156.bmp','a157.bmp','a158.bmp','a159.bmp','a160.bmp','a161.bmp','a162.bmp','a163.bmp','a164.bmp','a165.bmp','a166.bmp','a167.bmp','a168.bmp','a169.bmp','a170.bmp','a171.bmp','a172.bmp','a173.bmp','a174.bmp','a175.bmp','a176.bmp','a177.bmp','a178.bmp','a179.bmp','a180.bmp','a181.bmp','a182.bmp','a183.bmp','a184.bmp','a185.bmp','a186.bmp','a187.bmp','a188.bmp','a189.bmp','a190.bmp','a191.bmp','a192.bmp','a193.bmp','a194.bmp','a195.bmp','a196.bmp','a197.bmp','a198.bmp','a199.bmp','a200.bmp','a201.bmp','a202.bmp','a203.bmp','a204.bmp','a205.bmp','a206.bmp','a207.bmp','a208.bmp','a209.bmp','a210.bmp','a211.bmp','a212.bmp','a213.bmp','a214.bmp','a215.bmp','a216.bmp','a217.bmp','a218.bmp','a219.bmp','a220.bmp','a221.bmp','a222.bmp','a223.bmp','a224.bmp','a225.bmp','a226.bmp','a227.bmp','a228.bmp','a229.bmp','a230.bmp','a231.bmp','a232.bmp','a233.bmp','a234.bmp','a235.bmp','a236.bmp','a237.bmp','a238.bmp','a239.bmp','a240.bmp','a241.bmp','a242.bmp','a243.bmp','a244.bmp','a245.bmp','a246.bmp','a247.bmp','a248.bmp','a249.bmp','a250.bmp','a251.bmp','a252.bmp','a253.bmp','a254.bmp','a255.bmp','a256.bmp','a257.bmp','a258.bmp','a259.bmp','a260.bmp','a261.bmp','a262.bmp','a263.bmp','a264.bmp','a265.bmp','a266.bmp','a267.bmp','a268.bmp','a269.bmp','a270.bmp','a271.bmp','a272.bmp','a273.bmp','a274.bmp','a275.bmp','a276.bmp','a277.bmp','a278.bmp','a279.bmp','a280.bmp','a281.bmp','a282.bmp','a283.bmp','a284.bmp','a285.bmp','a286.bmp','a287.bmp','a288.bmp','a289.bmp','a290.bmp','a291.bmp','a292.bmp','a293.bmp','a294.bmp','a295.bmp','a296.bmp','a297.bmp','a298.bmp','a299.bmp','a300.bmp','a301.bmp','a302.bmp','a303.bmp','a304.bmp','a305.bmp','a306.bmp','a307.bmp','a308.bmp','a309.bmp','a310.bmp','a311.bmp','a312.bmp','a313.bmp','a314.bmp','a315.bmp','a316.bmp','a317.bmp','a318.bmp','a319.bmp','a320.bmp','a321.bmp','a322.bmp','a323.bmp','a324.bmp','a325.bmp','a326.bmp','a327.bmp','a328.bmp','a329.bmp','a330.bmp','a331.bmp','a332.bmp','a333.bmp','a334.bmp','a335.bmp','a336.bmp','a337.bmp','a338.bmp','a339.bmp','a340.bmp','a341.bmp','a342.bmp','a343.bmp','a344.bmp','a345.bmp','a346.bmp','a347.bmp','a348.bmp','a349.bmp','a350.bmp','a351.bmp','a352.bmp','a353.bmp','a354.bmp','a355.bmp','a356.bmp','a357.bmp','a358.bmp','a359.bmp','a360.bmp']
        self.dest_img = load_plain_image("explosion.bmp")
        self.dest_img2 = load_plain_image("explosion1.bmp")

        i = 0
        for file in self.files:
          self.img[i] = load_plain_image(file)
          i += 1

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.center = globals.reso_x / 2, globals.reso_y / 2
        self.velocity = 0
        self.facing = 90

        # Turn rate means how much the ship is turning left(negative value means
        # it's turning right
        self.turn_rate = 0
        self.turn_rate_accel = 2
        self.turn_rate_max = 7
        self.turn_rate_min = -7
        self.max_speed = 150
        self.altitude = 3

        self.x = globals.reso_x / 2
        self.y = globals.reso_y / 2
        self.shot_delay = 1

    def update(self):
      self.move()

      # Check if this object is out of the whole playground
      if self.x > globals.wholeLrx:
        self.x = globals.wholeLrx
        self.velocity = 0

      if self.x < 0:
        self.x = 0
        self.velocity = 0
        #sys.exit(2)

      if self.y > globals.wholeLry:
        self.y = globals.wholeLry
        self.velocity = 0

      if self.y < 0:
        self.y = 0
        self.velocity = 0

      # Move turn-rate back towards default
      if self.turn_rate > 0:
        self.turn_rate -= 1
      elif self.turn_rate < 0:
        self.turn_rate += 1

      # TODO We shouldn't have to define this here
      if self.facing > 359 or self.facing < 1:
        self.facing = 0

      self.image = self.img[self.facing]

      if self.shot_delay > 0:
        self.shot_delay -= 1

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
      shot = Shot(self.x, self.y, self.facing, self.rect.center, 40)
      self.shot_delay += 5
      return shot

    def shootMissile(self):
      # Create a new shot and assign it the properties of the ship
      shot = Missile(self.x, self.y, self.facing, self.rect.center, 30)
      self.shot_delay += 25
      return shot

    def shootMachinegun(self):
      # Create a new shot and assign it the properties of the ship
      shot = Shot(self.x, self.y, self.facing, self.rect.center, 150)
      self.shot_delay += 2
      return shot

    def accel(self,velocity):
      if self.velocity < self.max_speed:
        self.velocity += velocity

    def brake(self,velocity):
      if self.velocity > -10:
        self.velocity -= velocity

    def move(self):
      mod = float(self.velocity) / 1
      old_x = self.x 
      old_y = self.y
      
      self.x += math.sin(math.radians(self.facing)) * mod
      self.y += -math.cos(math.radians(self.facing)) * mod
      globals.ulx += math.sin(math.radians(self.facing)) * mod
      globals.uly += -math.cos(math.radians(self.facing)) * mod

      # Shake the ship in fast speeds
      if random.randrange(2) == 1:
        self.facing += +self.velocity / 20 
        if self.facing > 360:
          self.facing = 0
      else:
        self.facing -= +self.velocity / 20 
        if self.facing < 0:
          self.facing = 0

      return( old_x - self.x, old_y - self.y )

    def checkStatus(self):
      if self.hit_points < 1:
        self.destruction()
        self.velocity += 2
        if self.dest_timer < 1:
          return -1

    def destruction(self):

      # Create shot which immediately explodes
      shot = Shot(self.x, self.y, self.facing, self.rect.center, 40)
      shot.explode()
      allshots.add(shot)

      if self.dest_timer % 2:
        self.image = self.dest_img2
        self.dest_timer -= 1
      else:
        self.image = self.dest_img
        self.dest_timer -= 1

def checkShotCollision(a, b):
  # Right now everything is a square

  # a to the left of b
  if a.x < b.x:
    # a above of b
    if a.y < b.y:
      if a.rect.bottomright[0] > b.rect.topleft[0] and a.rect.bottomright[1] > b.rect.topleft[1]:
        if b.active > 0:
          if a.grounded == 0:
            b.explode()
            if a.hit_points > 0:
              a.hit_points -= b.damage
          elif b.grounded == 0:
            b.explode()
            if a.hit_points > 0:
              a.hit_points -= b.damage
          else:
            b.explode()
            if a.hit_points > 0:
              a.hit_points -= b.damage
    else:
      if a.rect.topright[0] > b.rect.bottomleft[0] and a.rect.topright[1] < b.rect.bottomleft[1]:
        if b.active > 0:
          if a.grounded == 0:
            b.explode()
            if a.hit_points > 0:
              a.hit_points -= b.damage
          elif b.grounded == 0:
            b.explode()
            if a.hit_points > 0:
              a.hit_points -= b.damage
          else:
            b.explode()
            if a.hit_points > 0:
              a.hit_points -= b.damage

  elif a.x > b.x:
    if a.y > b.y:
      if a.rect.topleft[0] < b.rect.bottomright[0] and a.rect.topleft[1] < b.rect.bottomright[1]:
        if b.active > 0:
          if a.grounded == 0:
            b.explode()
            if a.hit_points > 0:
              a.hit_points -= b.damage
          elif b.grounded == 0:
            b.explode()
            if a.hit_points > 0:
              a.hit_points -= b.damage
          else:
            b.explode()
            if a.hit_points > 0:
              a.hit_points -= b.damage
    else:
      if a.rect.bottomleft[0] < b.rect.topright[0] and a.rect.bottomleft[1] > b.rect.topright[1]:
        if b.active > 0:
          if a.grounded == 0:
            b.explode()
            if a.hit_points > 0:
              a.hit_points -= b.damage
          elif b.grounded == 0:
            b.explode()
            if a.hit_points > 0:
              a.hit_points -= b.damage
          else:
            b.explode()
            if a.hit_points > 0:
              a.hit_points -= b.damage

def checkCollision(a, b):
  # Right now everything is a square

  if a.x < b.x:
    if a.y < b.y:
      if a.rect.bottomright[0] > b.rect.topleft[0] and a.rect.bottomright[1] > b.rect.topleft[1]:
        if a.grounded == 0:
          a.velocity = 0
          a.x -= 10
          a.y -= 10
        elif b.grounded == 0:
          b.velocity = 0
          b.x -= 10
          b.y -= 10
        else:
          a.velocity = 0
          a.x -= 10
          a.y -= 10
    else:
      if a.rect.topright[0] > b.rect.bottomleft[0] and a.rect.topright[1] < b.rect.bottomleft[1]:
        if a.grounded == 0:
          a.velocity = 0
          a.x -= 10
          a.y += 10
        elif b.grounded == 0:
          b.velocity = 0
          b.x -= 10
          b.y += 10
        else:
          a.velocity = 0
          a.x -= 10
          a.y += 10
          b.velocity = 0
          b.x -= 10
          b.y += 10

  elif a.x > b.x:
    if a.y > b.y:
      if a.rect.topleft[0] < b.rect.bottomright[0] and a.rect.topleft[1] < b.rect.bottomright[1]:
        if a.grounded == 0:
          a.velocity = 0
          a.x += 10
          a.y += 10
        elif b.grounded == 0:
          b.velocity = 0
          b.x += 10
          b.y += 10
        else:
          a.velocity = 0
          a.x += 10
          a.y += 10
          b.velocity = 0
          b.x += 10
          b.y += 10
    else:
      if a.rect.bottomleft[0] < b.rect.topright[0] and a.rect.bottomleft[1] > b.rect.topright[1]:
        if a.grounded == 0:
          a.velocity = 0
          a.x += 10
          a.y -= 10
        elif b.grounded == 0:
          b.velocity = 0
          b.x += 10
          b.y -= 10
        else:
          b.velocity = 0
          b.x += 10
          b.y -= 10
          a.velocity = 0
          a.x += 10
          a.y -= 10

def bounceObject( obj, facing ):
  # Change object's facing determined by facing

  turn_amount = obj.velocity * 3

  if obj.facing < 45:
      obj.facing -= turn_amount
  elif obj.facing < 90:
      obj.facing += turn_amount
  elif obj.facing < 135:
      obj.facing -= turn_amount
  elif obj.facing < 180:
      obj.facing += turn_amount
  elif obj.facing < 225:
      obj.facing -= turn_amount
  elif obj.facing < 270:
      obj.facing += turn_amount
  elif obj.facing < 315 or obj.facing == 0:
      obj.facing -= turn_amount
  else:
      obj.facing += turn_amount

  if obj.facing > 359:
    obj.facing -= 360
  elif obj.facing < 0:
    obj.facing += 360

def checkPlayerCollision(a, b):
  # Right now everything is a square

  impact = a.velocity + b.velocity

  if a.altitude <= b.elevation:
    if a.x < b.x:
      if a.y < b.y:
        if a.rect.bottomright[0] > b.rect.topleft[0] and a.rect.bottomright[1] > b.rect.topleft[1]:
          # a impacts from up left
          if a.grounded == 0:
            #a.velocity /= 2
            a.x -= impact
            a.y -= impact
            a.velocity = 0

            bounceObject(a, 135)

            """if a.facing < 135:
              a.facing -= 19
            elif a.facing < 180:
              a.facing += 19

            if a.facing > 359 or a.facing < 0:
              a.facing = 0"""

            globals.ulx -= impact
            globals.uly -= impact
          elif b.grounded == 0:
            b.x -= impact
            b.y -= impact
            b.velocity = 0
            globals.ulx -= impact
            globals.uly -= impact
          else:
            #a.velocity /= 2
            a.x -= impact
            a.y -= impact
            a.velocity = 0
            globals.ulx -= impact
            globals.uly -= impact
            b.x -= impact
            b.y -= impact
            b.velocity = 0
            globals.ulx -= impact
            globals.uly -= impact
      else:
        if a.rect.topright[0] > b.rect.bottomleft[0] and a.rect.topright[1] < b.rect.bottomleft[1]:
          # a impacts from down left
          if a.grounded == 0:
            #a.velocity /= 2
            a.x -= impact
            a.y += impact
            a.velocity = 0

            if a.y > b.y:
              direct_hit = 1
            else:
              direct_hit = 0
            
            bounceObject(a, 45)

            globals.ulx -= impact
            globals.uly += impact
          elif b.grounded == 0:
            b.x -= impact
            b.y += impact
            b.velocity = 0
            globals.ulx -= impact
            globals.uly += impact
          else:
            a.x -= impact
            a.y += impact
            a.velocity = 0
            globals.ulx -= impact
            globals.uly += impact
            b.x -= impact
            b.y += impact
            b.velocity = 0
            globals.ulx -= impact
            globals.uly += impact

    elif a.x > b.x:
      if a.y > b.y:
        if a.rect.topleft[0] < b.rect.bottomright[0] and a.rect.topleft[1] < b.rect.bottomright[1]:
          # a impacts from bottom right
          if a.grounded == 0:
            #a.velocity /= 2
            a.x += impact
            a.y += impact
            a.velocity = 0

            if a.y > b.y:
              direct_hit = 1
            else:
              direct_hit = 0
            
            bounceObject(a, 315)

            globals.ulx += impact
            globals.uly += impact
          elif b.grounded == 0:
            b.x += impact
            b.y += impact
            b.velocity = 0
            globals.ulx += impact
            globals.uly += impact
          else:
            #a.velocity /= 2
            a.x += impact
            a.y += impact
            a.velocity = 0
            globals.ulx += impact
            globals.uly += impact
            b.x += impact
            b.y += impact
            b.velocity = 0
            globals.ulx += impact
            globals.uly += impact
      else:
        if a.rect.bottomleft[0] < b.rect.topright[0] and a.rect.bottomleft[1] > b.rect.topright[1]:
          # a impacts from up right
          if a.grounded == 0:
            #a.velocity /= 2
            a.x += impact
            a.y -= impact
            a.velocity = 0

            if a.y > b.y:
              direct_hit = 1
            else:
              direct_hit = 0
            
            bounceObject(a, 225)

            globals.ulx += impact
            globals.uly -= impact
          elif b.grounded == 0:
            b.x += impact
            b.y -= impact
            b.velocity = 0
            globals.ulx += impact
            globals.uly -= impact
          else:
            b.x += impact
            b.y -= impact
            b.velocity = 0
            globals.ulx += impact
            globals.uly -= impact
            a.x += impact
            a.y -= impact
            a.velocity = 0
            globals.ulx += impact
            globals.uly -= impact

# TODO Move these into one function
def randomizeTerrain():
  random1 = random.randrange(100,4900)
  random2 = random.randrange(100,4900)
  if random1 % 2 > 0:
    retval = (Terrain('forest.bmp', random1, random2, 1))
  else:
    retval = (Terrain('mountain.bmp', random1, random2, 3))
  return retval

def randomizeEnemy():
  random1 = random.randrange(100,4900)
  random2 = random.randrange(100,4900)
  random3 = random.randrange(5,40)
  retval = (GroundBattery(random1, random2, random3))
  return retval

# Main portion begins

pygame.init()
globals = Globals()
screen = pygame.display.set_mode((globals.reso_x, globals.reso_y))
pygame.display.set_caption('Ape')
pygame.mouse.set_visible(0)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(globals.bg_color)

screen.blit(background, (0, 0))
pygame.display.flip()

ship = Ship()

# Create terrains
x = []
for i in range(100):
  x.append(randomizeTerrain())

terrain = tuple(x)

# Create enemies
x = []
for i in range(1):
  x.append(randomizeEnemy())

batteries = tuple(x)

crosshairs = CrossHairs(ship)
misc_sprites = pygame.sprite.RenderPlain(crosshairs)
terrain_sprites = pygame.sprite.RenderPlain(terrain)
allshots = pygame.sprite.RenderPlain()
moving_objects = pygame.sprite.RenderPlain()
shipsprites = pygame.sprite.RenderPlain(ship)

clock = pygame.time.Clock()

# Info text
if pygame.font:
    font = pygame.font.Font(None, 36)
    text = font.render("Ship hit points " + str(ship.hit_points), 1, (10, 10, 10))
    enemy_text = font.render("Enemy hit points " + str(ship.hit_points), 1, (10, 10, 10))

textpos = text.get_rect(left=50)
enemy_textpos = enemy_text.get_rect(left=400)

# This has no meaning now, it seems
pygame.key.set_repeat(50)

# Game loop
while 1:
    clock.tick(40)

    pressed = pygame.key.get_pressed()
    if pressed[K_ESCAPE] == 1:
      sys.exit(2)
    if pressed[K_a] == 1:
      ship.turn('l')
    if pressed[K_d] == 1:
      ship.turn('r')
    if pressed[K_w] == 1:
      ship.accel(1)
    if pressed[K_s] == 1:
      ship.brake(1)
    if pressed[K_h] == 1:
      if ship.shot_delay == 0:
        allshots.add(ship.shoot())
    if pressed[K_j] == 1:
      if ship.shot_delay == 0:
        allshots.add(ship.shootMissile())
    if pressed[K_l] == 1:
      if ship.shot_delay == 0:
        allshots.add(ship.shootMachinegun())

    if pressed[K_q] == 1:
      ship.hit_points = 1

    for event in pygame.event.get():
      if event.type == QUIT:
          sys.exit(2)

    # Check if there are objects inside the visible screen
    for battery in batteries:
      a = battery.check()
      if a:
        moving_objects.add(a)

    for object in moving_objects:
      # Check player collisions with other objects
      checkPlayerCollision(ship, object)

      # Check shot collisions against other objects
      for a_shot in allshots:
        checkShotCollision(object,a_shot)

    for object in terrain_sprites:
      # Check player collisions with terrain
      checkPlayerCollision(ship, object)

      for a_shot in allshots:
        checkShotCollision(object,a_shot)

# TODO
    # Check shot collisions for player
    for a_shot in allshots:
      checkShotCollision(ship,a_shot)

    if ship.checkStatus() == -1:
      break

    moving_objects.update()
    misc_sprites.update()
    shipsprites.update()
    terrain_sprites.update()
    allshots.update()

    screen.blit(background, (0, 0))
    moving_objects.draw(screen)
    shipsprites.draw(screen)
    misc_sprites.draw(screen)
    terrain_sprites.draw(screen)
    allshots.draw(screen)
    
    # Draw ship info
    background.fill(globals.bg_color, textpos)
    font = pygame.font.Font(None, 36)
    text = font.render("Ship hit points " + str(ship.hit_points), 1, (10, 10, 10))
    background.blit(text, textpos)

    # Draw enemy info
    background.fill(globals.bg_color, enemy_textpos)
    font = pygame.font.Font(None, 36)
    enemy_text = font.render("Enemy hit points " + str(battery.hit_points), 1, (10, 10, 10))
    background.blit(enemy_text, enemy_textpos)

    pygame.display.flip()

info_textpos = enemy_text.get_rect(top=400)
background.fill(globals.bg_color, info_textpos)
font = pygame.font.Font(None, 108)
info_text = font.render("You have been destroyed.", 1, (250, 0, 0))
background.blit(info_text, info_textpos)
pygame.display.flip()
screen.blit(background, (0, 0))

pygame.display.flip()
# End game
time.sleep(3)

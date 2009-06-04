import os, sys
import pygame
import math
import time
import random
import getopt
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
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', wav
        raise SystemExit, message
    return sound

# TODO make other classes derive from body and eleccomp
class Body(pygame.sprite.Sprite):
  def __init__(self, x = 0, y = 0, direction = 0, center = 0, velocity = 0):
    self.x = x
    self.y = y
    self.velocity = velocity
    self.direction = direction
    self.mass = 0
    self.grounded = 0

class Machine(Body):
  def __init__(self, x = 0, y = 0, direction = 0, center = 0, velocity = 0, byWire = 0, ruggedness = 0):
    Body.__init__(self, x, y, direction, center, velocity)
    self.byWire = 10
    self.ruggedness = 10

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

    self.reso_x           = 1400
    self.reso_y           = 1050
    self.shot_sound       = load_sound("colt45.wav")
    self.hit_sound        = load_sound("bang_1.wav")
    self.crash_sound      = load_sound("kickdoordown.wav")
    self.bomb_sound       = load_sound("missle.wav")
    self.explo_sound      = load_sound("explo.wav")
    self.long_explo_sound = load_sound("long_explo.wav")
    self.empty_sound      = load_sound("quick_shot.wav")
    self.all_weapons      = {"Rocket": Rocket, "Bomb": Bomb}
    self.all_sounds       = {"Rocket": self.shot_sound, "Bomb": self.bomb_sound, "Empty": self.empty_sound}
    self.rocket_velocity  = 80;

    try:                                
      opts,args = getopt.getopt(sys.argv[1:], "r:", ["resolution="]) 
    except getopt.GetoptError:           
      usage()                          
      sys.exit(2) 

    print getopt.getopt(sys.argv, "r:", ["resolution="])  

    for opt,arg in opts:
      if opt in ("-r", "--resolution"):
        self.reso_x, self.reso_y = arg.split('x')

    self.reso_x = int(self.reso_x)
    self.reso_y = int(self.reso_y)
    # Visible screen
    self.ulx = 0
    self.uly = 0
    self.lrx = self.reso_x
    self.lry = self.reso_y

    self.center = (self.reso_x / 2, self.reso_y / 2)

    # Whole playground
    self.wholeUlx = 0
    self.wholeUly = 0
    self.wholeLrx = 2000
    self.wholeLry = 2000

    self.bg_color = (255,255,255)
    self.compensation = 400

class Building(Machine):
    def __init__(self, x, y, hit_points):
      Machine.__init__(self, x, y, 0, 0, 0)
      pygame.sprite.Sprite.__init__(self) #call Sprite initializer

      self.image, self.rect = load_image('pimp.bmp', -1)

      screen = pygame.display.get_surface()
      self.area = screen.get_rect()
      self.rect.topleft = -100,-100

      self.grounded = 1
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
    self.facing = 90
    self.destroyed = False

  def update(self):
    if self.destroyed != True:
      self.checkStatus()
      
      distance_x = ship.x - self.x
      distance_y = ship.y - self.y

      # Tracking
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

      if random.randrange(40) == 1:
        allshots.add(self.shoot())

  def shoot(self):
    shot = Rocket(self.x, self.y, self.facing, self.rect.center, globals.rocket_velocity)
    globals.shot_sound.play()
    return shot

  def checkStatus(self):
    if self.hit_points < 1:
      globals.hit_sound.play()
      globals.long_explo_sound.play()
      self.image = self.dest_img
      self.destroyed = True

class Rocket(Machine):
    def __init__(self, x, y, facing, center, velocity):
        Machine.__init__(self, x, y, facing, center, velocity)
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer

        self.image, self.rect = load_image('shot.bmp', -1)
        self.hit_image = load_plain_image('hit.bmp', -1)

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

        self.x = x
        self.y = y

        self.facing = facing
        self.rect.center = center
        self.velocity = velocity
        self.damage = 1
        self.disappear_timer = 0
        self.active = 1
        self.update()

        # TODO Make the shot launch from the edge of the firerer instead of this:
        # Move the object once so it won't hit the object that shot it

    def explode(self):
      self.disappear_timer = 10
      self.image = self.hit_image
      self.active = 0
      self.velocity = 0
      globals.hit_sound.play()

    def move(self):
      if self.active > 0:
        mod = float(self.velocity)
        self.x += math.sin(math.radians(self.facing)) * mod
        self.y += -math.cos(math.radians(self.facing)) * mod

    def update(self):
      self.move()

      if self.disappear_timer > 0:
        self.disappear_timer -= 1
        if self.disappear_timer % 2 == 0:
          self.x += random.randrange(-10, 10)
        else:
          self.y += random.randrange(-10, 10)

        if self.disappear_timer < 1:
          if self.active == 0:
            allshots.remove(self)

      # Check if this object is out of the whole playground
      if self.x > globals.wholeLrx or self.x < 0 or self.y > globals.wholeLry or self.y < 0:
        allshots.remove(self)

      # Check if this object is within the visible screen
      if (self.x - globals.ulx > 0, self.x < globals.lrx):
        if (self.y - globals.lry > 0, self.y < globals.lry):
          self.rect.topleft = self.x - globals.ulx, self.y - globals.uly 

class Bomb(Rocket):
  def __init__(self, x, y, facing, center, velocity):
    Rocket.__init__(self, x, y, facing, center, velocity)
    self.image = load_plain_image('missile.bmp', -1)
    self.damage = 10
    self.hit_image = load_plain_image('explosion1.bmp', -1)

  def explode(self):
    Rocket.explode(self)
    globals.explo_sound.play()

class Engine(Machine):
  def __init__(self, thrust, acceleration, brakage):
    Machine.__init__(self, 0, 0, 0, 0, 0)
    self.image = load_plain_image('missile.bmp', -1)
    pygame.sprite.Sprite.__init__(self) #call Sprite initializer
    self.thrust = thrust
    self.acceleration = acceleration
    self.brakage = brakage

class Machinery(Machine):
  def __init__(self, type, loading_time):
    Machine.__init__(self, 0, 0, 0, 0, 0)
    self.image = load_plain_image('missile.bmp', -1)
    pygame.sprite.Sprite.__init__(self) #call Sprite initializer
    self.type         = type
    self.loading_time = loading_time

class Barrel(Machine):
  def __init__(self, length):
    Machine.__init__(self, 0, 0, 0, 0, 0)
    self.image = load_plain_image('missile.bmp', -1)
    pygame.sprite.Sprite.__init__(self) #call Sprite initializer
    self.length = length

class Clip(Machine):
  def __init__(self, space, amount):
    Machine.__init__(self, 0, 0, 0, 0, 0)
    self.image = load_plain_image('missile.bmp', -1)
    pygame.sprite.Sprite.__init__(self) #call Sprite initializer
    self.space  = space
    self.amount = amount

class Weapon(Machine):
  def __init__(self, machinery, barrel, clip):
    Machine.__init__(self, 0, 0, 0, 0, 0)
    self.image = load_plain_image('missile.bmp', -1)
    pygame.sprite.Sprite.__init__(self) #call Sprite initializer
    self.machinery = machinery
    self.barrel    = barrel
    self.clip      = clip
    self.shot_delay = 0

  def shoot(self, shooter):
    if self.clip.amount > 0:
      # Create a new shot and assign it the properties of the ship
      shot = globals.all_weapons[self.machinery.type](shooter.x, shooter.y, shooter.facing, shooter.rect.center, 40)
      #globals.shot_sound.play()
      globals.all_sounds[self.machinery.type].play()
      self.shot_delay += self.machinery.loading_time
      self.clip.amount -= 1
      return shot
    else:
      globals.all_sounds['Empty'].play()
      return False

  def update(self):
    if self.shot_delay > 0:
      self.shot_delay -= 1

class Ship(Machine):
    def __init__(self, engines, weapons):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        # We say here that start in the middle of the playfield, direction 90, center, velocity
        #Machine.__init__(self, globals.reso_x / 2, globals.reso_y / 2, 90, (globals.reso_x/2, globals.reso_y/2), 0)
        Machine.__init__(self, globals.reso_x / 2, globals.reso_y / 2, 90, (0,0), 0)

        self.image, self.rect = load_image('a90.bmp', -1)
        self.img = {}
        self.grounded = 0
        self.hit_points = 20
        self.dest_timer = 200
        self.engines = engines
        self.weapons = weapons

        # Define the files used by sprite(360 degrees)
        # TODO Make this a function to be used by all other sprites too
        self.files = []
        for i in range(360):
          s = 'a' + str(i) + '.bmp'
          self.files.append(s)

        self.dest_img = load_plain_image("explosion.bmp")
        self.dest_img2 = load_plain_image("explosion1.bmp")

        i = 0
        for file in self.files:
          self.img[i] = load_plain_image(file)
          i += 1

        self.max_speed    = 0
        self.acceleration = 0
        self.brakage      = 0
        for engine in self.engines:
          self.max_speed    += engine.thrust
          self.acceleration += engine.acceleration
          self.brakage      += engine.brakage

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.center = globals.reso_x / 2, globals.reso_y / 2
        self.facing = 90

        # Turn rate means how much the ship is turning left(negative value means
        # it's turning right
        self.turn_rate = 0
        self.turn_rate_accel = 2
        self.turn_rate_max = 7
        self.turn_rate_min = -7

        self.altitude = 3

    def update(self):
      self.move()
      for weapon in self.weapons:
        weapon.update()

      # Check if this object is out of the whole playground
      if self.x > globals.wholeLrx:
        self.x = globals.wholeLrx
        # Realign the visible screen
        globals.ulx = self.x - (globals.reso_x / 2)
        globals.lrx = self.x + (globals.reso_x / 2)
        self.velocity = 0

      if self.x < globals.wholeUlx:
        self.x = globals.wholeUlx
        # Realign the visible screen
        globals.ulx = self.x - (globals.reso_x / 2)
        globals.lrx = self.x + (globals.reso_x / 2)
        self.velocity = 0
        #sys.exit(2)

      if self.y > globals.wholeLry:
        self.y = globals.wholeLry
        # Realign the visible screen
        globals.uly = self.y - (globals.reso_y / 2)
        globals.lry = self.y + (globals.reso_y / 2)
        self.velocity = 0

      if self.y < globals.wholeUly:
        self.y = globals.wholeUly
        # Realign the visible screen
        globals.uly = self.y - (globals.reso_y / 2)
        globals.lry = self.y + (globals.reso_y / 2)
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
      # TODO These should be replaced with a function call that just makes
      # sure that we are in the right place
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
        if self.dest_timer < 1:
          return -1
        if self.velocity < self.max_speed:
          self.velocity += 1

    def destruction(self):
      # Create shot which immediately explodes
      shot = Rocket(self.x, self.y, self.facing, self.rect.center, 40)
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

def checkPotentialCollision(a, b):
  # Parameter 'a' is the one that must move always. 'b' can be still
  if a.velocity < 1:
    return

  mod = float(a.velocity)
  a_heading_x = a.x + math.sin(math.radians(a.facing)) * mod
  a_heading_y = a.y + -math.cos(math.radians(a.facing)) * mod

  a_next_x = a.x + a_heading_x
  a_next_y = a.y + a_heading_y

  if b.velocity > 0:
    b_heading_x = b.x + math.sin(math.radians(b.facing)) * mod
    b_heading_y = b.y + -math.cos(math.radians(b.facing)) * mod

    b_next_x = b_heading_x
    b_next_y = b_heading_y
  else:
    b_heading_x = 0
    b_heading_y = 0

    b_next_x = b.x
    b_next_y = b.y

  #if JANAT_LEIKKAAVAT
  #  print "HJI"
  #  # Bodies are on a crash course. Simulate the positions the bodies are in and check if they do collide
  #  a_simulated_x = a.x
  #  a_simulated_y = a.y

  #  b_simulated_x = b.x
  #  b_simulated_y = b.y
  #  # TODO Make a suitable terminating condition for the loop ("while not closing in on each other" for instance)
  #  for i in range(10):
  #    a_simulated_x += a_heading_x
  #    a_simulated_y += a_heading_y

  #    b_simulated_x += b_heading_x
  #    b_simulated_y += b_heading_y

  #    # TODO Clean this up.
  #    a_simulated = pygame.Rect(a_simulated_x - a.rect.width/2, a_simulated_y - a.rect.height/2, a_simulated_y + a.rect.height/2, a_simulated_y + a.rect.height/2)
  #    b_simulated = pygame.Rect(b_simulated_x - b.rect.width/2, b_simulated_y - b.rect.height/2, b_simulated_y + b.rect.height/2, b_simulated_y + b.rect.height/2)

  #    if a_simulated.contains(b_simulated):
  #      print "COLLISION"

def checkCollision(a, b):
  # Right now everything is a square

  if a.x < b.x:
    if a.y < b.y:
      if a.rect.bottomright[0] > b.rect.topleft[0] and a.rect.bottomright[1] > b.rect.topleft[1]:
        globals.crash_sound.play()
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
        globals.crash.play()
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
        globals.crash.play()
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
        globals.crash.play()
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

# TODO there should be only one collision-checker class/function and different handling of collisions
# should be done in the objects' classes
def checkPlayerCollision(a, b):
  # Right now everything is a square

  impact = a.velocity + b.velocity

  if a.altitude <= b.elevation:
    if a.x < b.x:
      if a.y < b.y:
        if a.rect.bottomright[0] > b.rect.topleft[0] and a.rect.bottomright[1] > b.rect.topleft[1]:
          # a impacts from up left
          globals.crash_sound.play()
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
          globals.crash_sound.play()
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
          globals.crash_sound.play()
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
          globals.crash_sound.play()
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
class GameInitiator:
  def randomizeTerrain(self):
    random1 = random.randrange(100,globals.wholeLrx)
    random2 = random.randrange(100,globals.wholeLry)
    if random1 % 2 > 0:
      retval = (Terrain('forest.bmp', random1, random2, 1))
    else:
      retval = (Terrain('mountain.bmp', random1, random2, 3))
    return retval

  def randomizeEnemy(self):
    random1 = random.randrange(100,globals.wholeLrx)
    random2 = random.randrange(100,globals.wholeLry)
    random3 = random.randrange(20, 25)
    retval = (GroundBattery(random1, random2, random3))
    return retval

  def createForest(self, x, y):
    retval = (Terrain('forest.bmp', x, y, 1))
    return retval

  def createMountain(self,x, y):
    retval = (Terrain('mountain.bmp', x, y, 3))
    return retval

  def createTerrainGroup(self, terrainFunction):
    random1 = random.randrange(100,globals.wholeLrx)
    random2 = random.randrange(100,globals.wholeLry)
    random3 = random.randrange(1,20)
    current_x = random1
    current_y = random2
    createdTerrains = []
    print current_x, current_y
    func = getattr(GameInitiator, terrainFunction)

    for i in range(random3):
      createdTerrains.append(func(self, current_x, current_y))
      current_x += 50
      if random.randrange(1,5) % 5 == 1:
        current_y += 50
        if random.randrange(1,2) == 2:
          current_x = random1
        else:
          current_x = random1 + random.randrange(50,100)

    return createdTerrains
#
# Main portion begins
#
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

# Create ship and it's components
# Rocket launcher
machinery       = Machinery("Rocket", 10)
barrel          = Barrel(5)
clip            = Clip(2, 200)
rocket_launcher = Weapon(machinery, barrel, clip)

# Bomber
machinery = Machinery("Bomb", 20)
barrel    = Barrel(2)
clip      = Clip(10, 4)
bomber    = Weapon(machinery, barrel, clip)

weapons   = [rocket_launcher, bomber]
engines   = [Engine(15, 1, 1), Engine(15, 1, 1)]
ship      = Ship(engines, weapons)

# Create terrains
"""x = []
for i in range(100):
  x.append(randomizeTerrain())"""

#terrain = tuple(x)

gameInit = GameInitiator()

x = []
for i in range(10):
  if random.randrange(1,3) == 1:
    next_terrain = 'createMountain'
  else:
    next_terrain = 'createForest'

  x.append(gameInit.createTerrainGroup(next_terrain))


terrain = tuple(x)

# Create enemies
x = []
for i in range(3):
  x.append(gameInit.randomizeEnemy())

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
    text = font.render("Ship hit points " + str(ship.hit_points) + " " + str(ship.weapons[0].machinery.type) + " ammo: " + str(ship.weapons[0].clip.amount) + " " + str(ship.weapons[1].machinery.type) + " ammo: " + str(ship.weapons[1].clip.amount), 1, (10, 10, 10))
    #enemy_text = font.render("Enemy hit points " + str(ship.hit_points), 1, (10, 10, 10))

textpos = text.get_rect(left=50)
#enemy_textpos = enemy_text.get_rect(left=400)

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
      ship.accel(ship.acceleration)
    if pressed[K_s] == 1:
      ship.brake(ship.brakage)
    if pressed[K_h] == 1:
      if ship.weapons[0].shot_delay == 0:
        shot = ship.weapons[0].shoot(ship)
        if shot:
          allshots.add(shot)
    if pressed[K_j] == 1:
      if ship.weapons[1].shot_delay == 0:
        shot = ship.weapons[1].shoot(ship)
        if shot:
          allshots.add(shot)
    if pressed[K_k] == 1:
      if ship.weapons[2].shot_delay == 0:
        shot = ship.weapons[2].shoot(ship)
        if shot:
          allshots.add(shot)

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

    # Check player collisions with other objects
    for object in moving_objects:
      checkPlayerCollision(ship, object)
      checkPotentialCollision(ship,object)

    # Check player collisions with terrain
    for object in terrain_sprites:
      checkPlayerCollision(ship, object)
      checkPotentialCollision(ship,object)

    # Check shot collisions
    for a_shot in allshots:
      # Check shot collisions for player
      checkShotCollision(ship,a_shot)
      checkPotentialCollision(ship,a_shot)

      # Check shot collisions against other objects
      for object in moving_objects:
        checkShotCollision(object,a_shot)
        checkPotentialCollision(object,a_shot)

      # Check shot collisions against terrain 
      for object in terrain_sprites:
        checkShotCollision(object,a_shot)
        checkPotentialCollision(a_shot,object)

# TODO

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

    text = font.render("Ship hit points " + str(ship.hit_points) + " " + str(ship.weapons[0].machinery.type) + " ammo: " + str(ship.weapons[0].clip.amount) + " " + str(ship.weapons[1].machinery.type) + " ammo: " + str(ship.weapons[1].clip.amount), 1, (10, 10, 10))

    background.blit(text, textpos)

    # Draw enemy info
    #background.fill(globals.bg_color, enemy_textpos)
    #font = pygame.font.Font(None, 36)
    #enemy_text = font.render("Enemy hit points " + str(battery.hit_points), 1, (10, 10, 10))
    #background.blit(enemy_text, enemy_textpos)

    pygame.display.flip()

#info_textpos = enemy_text.get_rect(top=400)
#background.fill(globals.bg_color, info_textpos)
font = pygame.font.Font(None, 108)
info_text = font.render("You have been destroyed.", 1, (250, 0, 0))
info_textpos = info_text.get_rect(top=400)
background.blit(info_text, info_textpos)
pygame.display.flip()
screen.blit(background, (0, 0))

pygame.display.flip()
# End game
time.sleep(3)

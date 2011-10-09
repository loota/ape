import math
import random
import media
import pygame
import global_state

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
    pygame.sprite.Sprite.__init__(self)
    self.image, self.rect = media.load_image(image, -1)
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
    if (self.x - global_state.globals.ulx > 0, self.x < global_state.globals.lrx):
      if (self.y - global_state.globals.lry > 0, self.y < global_state.globals.lry):
        self.rect.topleft = self.x - global_state.globals.ulx, self.y - global_state.globals.uly
        return self

class CrossHairs(pygame.sprite.Sprite):
    def __init__(self,owner):
      pygame.sprite.Sprite.__init__(self)
      self.image, self.rect = media.load_image('crosshairs.bmp', -1)
      screen = pygame.display.get_surface()
      self.area = screen.get_rect()
      self.rect.topleft = 800,500

      self.x = 500
      self.y = 500
      self.distance = 250
      self.owner = owner

    def update(self):
      mod = self.owner.velocity * 10
      if mod > (global_state.globals.reso_y / 2):
        mod = global_state.globals.reso_y / 2

      self.x = math.sin(math.radians(self.owner.facing)) * mod
      self.y = -math.cos(math.radians(self.owner.facing)) * mod

      self.rect.center = (global_state.globals.center[0] + self.x, global_state.globals.center[1] + self.y)

class Building(Machine):
    def __init__(self, x, y, hit_points):
      Machine.__init__(self, x, y, 0, 0, 0)
      pygame.sprite.Sprite.__init__(self)

      self.image, self.rect = media.load_image('ground-battery.bmp', -1)

      screen = pygame.display.get_surface()
      self.area = screen.get_rect()
      self.rect.topleft = -100,-100

      self.grounded = 1
      self.hit_points = hit_points
      self.elevation = 1

    def check(self):
      # Check if this object is within the visible screen
      if (self.x - global_state.globals.ulx > 0, self.x < global_state.globals.lrx):
        if (self.y - global_state.globals.lry > 0, self.y < global_state.globals.lry):
          self.rect.topleft = self.x - global_state.globals.ulx, self.y - global_state.globals.uly
          return self

    def checkStatus(self):
      if self.hit_points < 0:
        pass

class GroundBattery(Building):
  def __init__(self, x, y, hit_points):
    Building.__init__(self, x, y, hit_points)
    self.dest_img = media.load_plain_image('explosion.bmp')
    self.facing = 90
    self.destroyed = False
    self.target = False

  def update(self):
    if self.destroyed != True:
      self.checkStatus()
      
      distance_x = self.target.x - self.x
      distance_y = self.target.y - self.y

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
        global_state.globals.allshots.add(self.shoot())

  def shoot(self):
    shot = Rocket(self.x, self.y, self.facing, self.rect.center, global_state.globals.rocket_velocity)
    global_state.globals.shot_sound.play()
    return shot

  def checkStatus(self):
    if self.hit_points < 1:
      global_state.globals.hit_sound.play()
      global_state.globals.long_explo_sound.play()
      self.image = self.dest_img
      self.destroyed = True

class Rocket(Machine):
    def __init__(self, x, y, facing, center, velocity):
        Machine.__init__(self, x, y, facing, center, velocity)
        pygame.sprite.Sprite.__init__(self)

        self.image, self.rect = media.load_image('shot.bmp', -1)
        self.hit_image = media.load_plain_image('hit.bmp', -1)

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

    def explode(self):
      self.disappear_timer = 10
      self.image = self.hit_image
      self.active = 0
      self.velocity = 0
      global_state.globals.hit_sound.play()

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
            global_state.globals.allshots.remove(self)

      # Check if this object is out of the whole playground
      if self.x > global_state.globals.wholeLrx or self.x < 0 or self.y > global_state.globals.wholeLry or self.y < 0:
        global_state.globals.allshots.remove(self)

      # Check if this object is within the visible screen
      if (self.x - global_state.globals.ulx > 0, self.x < global_state.globals.lrx):
        if (self.y - global_state.globals.lry > 0, self.y < global_state.globals.lry):
          self.rect.topleft = self.x - global_state.globals.ulx, self.y - global_state.globals.uly 

class Bomb(Rocket):
  def __init__(self, x, y, facing, center, velocity):
    Rocket.__init__(self, x, y, facing, center, velocity)
    self.image = media.load_plain_image('missile.bmp', -1)
    self.damage = 10
    self.hit_image = media.load_plain_image('explosion1.bmp', -1)

  def explode(self):
    Rocket.explode(self)
    global_state.globals.explo_sound.play()

class Engine(Machine):
  def __init__(self, thrust, acceleration, brakage):
    Machine.__init__(self, 0, 0, 0, 0, 0)
    self.image = media.load_plain_image('missile.bmp', -1)
    pygame.sprite.Sprite.__init__(self)
    self.thrust = thrust
    self.acceleration = acceleration
    self.brakage = brakage

class Machinery(Machine):
  def __init__(self, type, loading_time):
    Machine.__init__(self, 0, 0, 0, 0, 0)
    self.image = media.load_plain_image('missile.bmp', -1)
    pygame.sprite.Sprite.__init__(self)
    self.type         = type
    self.loading_time = loading_time

class Barrel(Machine):
  def __init__(self, length):
    Machine.__init__(self, 0, 0, 0, 0, 0)
    self.image = media.load_plain_image('missile.bmp', -1)
    pygame.sprite.Sprite.__init__(self)
    self.length = length

class Clip(Machine):
  def __init__(self, space, amount):
    Machine.__init__(self, 0, 0, 0, 0, 0)
    self.image = media.load_plain_image('missile.bmp', -1)
    pygame.sprite.Sprite.__init__(self)
    self.space  = space
    self.amount = amount

class Weapon(Machine):
  def __init__(self, machinery, barrel, clip):
    Machine.__init__(self, 0, 0, 0, 0, 0)
    self.image = media.load_plain_image('missile.bmp', -1)
    pygame.sprite.Sprite.__init__(self)
    self.machinery = machinery
    self.barrel    = barrel
    self.clip      = clip
    self.shot_delay = 0

  def shoot(self, shooter):
    if self.clip.amount > 0:
      # Create a new shot and assign it the properties of the ship
      shot = global_state.globals.all_weapons[self.machinery.type](shooter.x, shooter.y, shooter.facing, shooter.rect.center, 40)
      global_state.globals.all_sounds[self.machinery.type].play()
      self.shot_delay += self.machinery.loading_time
      self.clip.amount -= 1
      return shot
    else:
      global_state.globals.all_sounds['Empty'].play()
      return False

  def update(self):
    if self.shot_delay > 0:
      self.shot_delay -= 1

class Ship(Machine):
    def __init__(self, engines, weapons):
        pygame.sprite.Sprite.__init__(self)
        # We say here that start in the middle of the playfield, direction 90, center, velocity
        Machine.__init__(self, global_state.globals.reso_x / 2, global_state.globals.reso_y / 2, 90, (0,0), 0)

        self.image, self.rect = media.load_image('a90.bmp', -1)
        self.img = {}
        self.grounded = 0
        self.hit_points = 20
        self.dest_timer = 200
        self.engines = engines
        self.weapons = weapons

        self.files = []
        for i in range(360):
          s = 'a' + str(i) + '.bmp'
          self.files.append(s)

        self.dest_img = media.load_plain_image("explosion.bmp")
        self.dest_img2 = media.load_plain_image("explosion1.bmp")

        i = 0
        for file in self.files:
          self.img[i] = media.load_plain_image(file)
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
        self.rect.center = global_state.globals.reso_x / 2, global_state.globals.reso_y / 2
        self.facing = 90

        # Turn rate means how much the ship is turning left and negative value means
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
      if self.x > global_state.globals.wholeLrx:
        self.x = global_state.globals.wholeLrx
        # Realign the visible screen
        global_state.globals.ulx = self.x - (global_state.globals.reso_x / 2)
        global_state.globals.lrx = self.x + (global_state.globals.reso_x / 2)
        self.velocity = 0

      if self.x < global_state.globals.wholeUlx:
        self.x = global_state.globals.wholeUlx
        # Realign the visible screen
        global_state.globals.ulx = self.x - (global_state.globals.reso_x / 2)
        global_state.globals.lrx = self.x + (global_state.globals.reso_x / 2)
        self.velocity = 0

      if self.y > global_state.globals.wholeLry:
        self.y = global_state.globals.wholeLry
        # Realign the visible screen
        global_state.globals.uly = self.y - (global_state.globals.reso_y / 2)
        global_state.globals.lry = self.y + (global_state.globals.reso_y / 2)
        self.velocity = 0

      if self.y < global_state.globals.wholeUly:
        self.y = global_state.globals.wholeUly
        # Realign the visible screen
        global_state.globals.uly = self.y - (global_state.globals.reso_y / 2)
        global_state.globals.lry = self.y + (global_state.globals.reso_y / 2)
        self.velocity = 0

      # Move turn-rate back towards default
      if self.turn_rate > 0:
        self.turn_rate -= 1
      elif self.turn_rate < 0:
        self.turn_rate += 1

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

    def accel(self, velocity):
      if self.velocity < self.max_speed:
        self.velocity += velocity / 2

    def brake(self, velocity):
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
      global_state.globals.ulx += math.sin(math.radians(self.facing)) * mod
      global_state.globals.uly += -math.cos(math.radians(self.facing)) * mod

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
      global_state.globals.allshots.add(shot)

      if self.dest_timer % 2:
        self.image = self.dest_img2
        self.dest_timer -= 1
      else:
        self.image = self.dest_img
        self.dest_timer -= 1

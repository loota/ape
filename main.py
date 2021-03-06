import time
import sys
import global_state
from pygame.locals import *
from bodies import *

def checkShotCollision(a, b):
  # Right now everything is a square

  # a to the left of b
  if a.x < b.x:
    # a above b
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

def checkCollision(a, b):
  # Right now everything is a square

  if a.x < b.x:
    if a.y < b.y:
      if a.rect.bottomright[0] > b.rect.topleft[0] and a.rect.bottomright[1] > b.rect.topleft[1]:
        global_state.globals.crash_sound.play()
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
        global_state.globals.crash.play()
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
        global_state.globals.crash.play()
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
        global_state.globals.crash.play()
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
          global_state.globals.crash_sound.play()
          if a.grounded == 0:
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

            global_state.globals.ulx -= impact
            global_state.globals.uly -= impact
          elif b.grounded == 0:
            b.x -= impact
            b.y -= impact
            b.velocity = 0
            global_state.globals.ulx -= impact
            global_state.globals.uly -= impact
          else:
            a.x -= impact
            a.y -= impact
            a.velocity = 0
            global_state.globals.ulx -= impact
            global_state.globals.uly -= impact
            b.x -= impact
            b.y -= impact
            b.velocity = 0
            global_state.globals.ulx -= impact
            global_state.globals.uly -= impact
      else:
        if a.rect.topright[0] > b.rect.bottomleft[0] and a.rect.topright[1] < b.rect.bottomleft[1]:
          global_state.globals.crash_sound.play()
          # a impacts from down left
          if a.grounded == 0:
            a.x -= impact
            a.y += impact
            a.velocity = 0

            if a.y > b.y:
              direct_hit = 1
            else:
              direct_hit = 0
            
            bounceObject(a, 45)

            global_state.globals.ulx -= impact
            global_state.globals.uly += impact
          elif b.grounded == 0:
            b.x -= impact
            b.y += impact
            b.velocity = 0
            global_state.globals.ulx -= impact
            global_state.globals.uly += impact
          else:
            a.x -= impact
            a.y += impact
            a.velocity = 0
            global_state.globals.ulx -= impact
            global_state.globals.uly += impact
            b.x -= impact
            b.y += impact
            b.velocity = 0
            global_state.globals.ulx -= impact
            global_state.globals.uly += impact

    elif a.x > b.x:
      if a.y > b.y:
        if a.rect.topleft[0] < b.rect.bottomright[0] and a.rect.topleft[1] < b.rect.bottomright[1]:
          global_state.globals.crash_sound.play()
          # a impacts from bottom right
          if a.grounded == 0:
            a.x += impact
            a.y += impact
            a.velocity = 0

            if a.y > b.y:
              direct_hit = 1
            else:
              direct_hit = 0
            
            bounceObject(a, 315)

            global_state.globals.ulx += impact
            global_state.globals.uly += impact
          elif b.grounded == 0:
            b.x += impact
            b.y += impact
            b.velocity = 0
            global_state.globals.ulx += impact
            global_state.globals.uly += impact
          else:
            a.x += impact
            a.y += impact
            a.velocity = 0
            global_state.globals.ulx += impact
            global_state.globals.uly += impact
            b.x += impact
            b.y += impact
            b.velocity = 0
            global_state.globals.ulx += impact
            global_state.globals.uly += impact
      else:
        if a.rect.bottomleft[0] < b.rect.topright[0] and a.rect.bottomleft[1] > b.rect.topright[1]:
          global_state.globals.crash_sound.play()
          # a impacts from up right
          if a.grounded == 0:
            a.x += impact
            a.y -= impact
            a.velocity = 0

            if a.y > b.y:
              direct_hit = 1
            else:
              direct_hit = 0
            
            bounceObject(a, 225)

            global_state.globals.ulx += impact
            global_state.globals.uly -= impact
          elif b.grounded == 0:
            b.x += impact
            b.y -= impact
            b.velocity = 0
            global_state.globals.ulx += impact
            global_state.globals.uly -= impact
          else:
            b.x += impact
            b.y -= impact
            b.velocity = 0
            global_state.globals.ulx += impact
            global_state.globals.uly -= impact
            a.x += impact
            a.y -= impact
            a.velocity = 0
            global_state.globals.ulx += impact
            global_state.globals.uly -= impact

class GameInitiator:
  def createTerrains(self):
    terrains = []
    for i in range(10):
      terrains.append(self.createTerrainGroup())
    return tuple(terrains)

  def createForest(self, x, y):
    forest = (Terrain('forest.bmp', x, y, 1))
    return forest

  def createMountain(self,x, y):
    mountain = (Terrain('mountain.bmp', x, y, 3))
    return mountain

  def createTerrainGroup(self):
    xPosition = random.randrange(100,global_state.globals.wholeLrx)
    yPosition = random.randrange(100,global_state.globals.wholeLry)
    numberOfTiles = random.randrange(1,20)
    createdTerrains = []
    current_x = xPosition
    current_y = yPosition
    randomNumber = random.randrange(1,3)
    for i in range(numberOfTiles):
      if randomNumber == 1:
        nextTerrain = self.createMountain(current_x, current_y)
      else:
        nextTerrain = self.createForest(current_x, current_y)

      createdTerrains.append(nextTerrain)
      current_x += 50
      if random.randrange(1,5) % 5 == 1:
        current_y += 50
        if random.randrange(1,2) == 2:
          current_x = xPosition
        else:
          current_x = yPosition + random.randrange(50,100)
    return createdTerrains

  def createShip(self):
    machinery       = Machinery("Rocket", 10)
    barrel          = Barrel(5)
    clip            = Clip(2, 200)
    rocket_launcher = Weapon(machinery, barrel, clip)

    machinery     = Machinery("Bomb", 20)
    barrel        = Barrel(2)
    clip          = Clip(10, 4)
    bomb_launcher = Weapon(machinery, barrel, clip)

    weapons   = [rocket_launcher, bomb_launcher]
    engines   = [Engine(15, 1, 1), Engine(15, 1, 1)]
    ship      = Ship(engines, weapons)
    return ship

  def createEnemies(self, ship):
    enemies = []
    for i in range(3):
      ground_battery = self.randomizeEnemy()
      ground_battery.target = ship
      enemies.append(ground_battery)
    return tuple(enemies)

  def randomizeEnemy(self):
    x_position = random.randrange(100,global_state.globals.wholeLrx)
    y_position = random.randrange(100,global_state.globals.wholeLry)
    hit_points = random.randrange(20, 25)
    ground_battery = (GroundBattery(x_position, y_position, hit_points))
    return ground_battery

class GraphicsRunner:
  def initDisplay(self):
    self.screen = pygame.display.set_mode((global_state.globals.reso_x, global_state.globals.reso_y))
    pygame.display.set_caption('Ape')
    pygame.mouse.set_visible(0)

    self.background = pygame.Surface(self.screen.get_size())
    self.background = self.background.convert()
    self.background.fill(global_state.globals.bg_color)

    self.screen.blit(self.background, (0, 0))
    pygame.display.flip()

  def drawObjects(self):
    self.screen.blit(self.background, (0, 0))
    moving_objects.draw(self.screen)
    shipsprites.draw(self.screen)
    misc_sprites.draw(self.screen)
    terrain_sprites.draw(self.screen)
    global_state.globals.allshots.draw(self.screen)
    
    self.background.fill(global_state.globals.bg_color, textpos)
    font = pygame.font.Font(None, 36)
    text = font.render("Ship hit points " + str(ship.hit_points) + " " + str(ship.weapons[0].machinery.type) + " ammo: " + str(ship.weapons[0].clip.amount) + " " + str(ship.weapons[1].machinery.type) + " ammo: " + str(ship.weapons[1].clip.amount), 1, (10, 10, 10))

    self.background.blit(text, textpos)
    pygame.display.flip()

class GameRunner:
    def endGame(self, text):
        font = pygame.font.Font(None, 108)
        info_text = font.render("Game over" + text , 1, (250, 0, 0))
        info_textpos = info_text.get_rect(top=30, left=30)
        graphicsRunner.background.blit(info_text, info_textpos)
        pygame.display.flip()
        graphicsRunner.screen.blit(graphicsRunner.background, (0, 0))

    def checkWinCondition(self):
        intact_battery_found = False
        for battery in batteries:
            if battery.destroyed == False:
                intact_battery_found = True

        if intact_battery_found == False:
            return True
        else:
            return False

    def handleKeyEvents(self):
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
              global_state.globals.allshots.add(shot)
        if pressed[K_j] == 1:
          if ship.weapons[1].shot_delay == 0:
            shot = ship.weapons[1].shoot(ship)
            if shot:
              global_state.globals.allshots.add(shot)

        if pressed[K_q] == 1:
          ship.hit_points = 1

        for event in pygame.event.get():
          if event.type == QUIT:
              sys.exit(2)

# Main portion begins
gameInit = GameInitiator()
graphicsRunner = GraphicsRunner()
graphicsRunner.initDisplay()

ship = gameInit.createShip()

terrain = gameInit.createTerrains()

batteries = gameInit.createEnemies(ship)

crosshairs = CrossHairs(ship)
misc_sprites = pygame.sprite.RenderPlain(crosshairs)
terrain_sprites = pygame.sprite.RenderPlain(terrain)
global_state.globals.allshots = pygame.sprite.RenderPlain()
moving_objects = pygame.sprite.RenderPlain()
shipsprites = pygame.sprite.RenderPlain(ship)

clock = pygame.time.Clock()

# Info text
if pygame.font:
    font = pygame.font.Font(None, 36)
    text = font.render("Ship hit points " + str(ship.hit_points) + " " + str(ship.weapons[0].machinery.type) + " ammo: " + str(ship.weapons[0].clip.amount) + " " + str(ship.weapons[1].machinery.type) + " ammo: " + str(ship.weapons[1].clip.amount), 1, (10, 10, 10))

textpos = text.get_rect(left=50)

# TODO This has no meaning now, it seems
pygame.key.set_repeat(50)

gameRunner = GameRunner()
# Game loop
while 1:
    clock.tick(30)

    gameRunner.handleKeyEvents()

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
    for a_shot in global_state.globals.allshots:
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

    if ship.checkStatus() == -1:
        endGame('. You lost')
        break

    if gameRunner.checkWinCondition():
        gameRunner.endGame('. You won!')
        break

    moving_objects.update()
    misc_sprites.update()
    shipsprites.update()
    terrain_sprites.update()
    global_state.globals.allshots.update()
    graphicsRunner.drawObjects()
    

pygame.display.flip()
# End game
time.sleep(3)

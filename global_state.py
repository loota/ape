from bodies import *
import sys
import media
import getopt
class Globals:
  def __init__(self):

    self.reso_x           = 1400
    self.reso_y           = 1050
    self.shot_sound       = media.load_sound("colt45.wav")
    self.hit_sound        = media.load_sound("bang_1.wav")
    self.crash_sound      = media.load_sound("kickdoordown.wav")
    self.bomb_sound       = media.load_sound("missle.wav")
    self.explo_sound      = media.load_sound("explo.wav")
    self.long_explo_sound = media.load_sound("long_explo.wav")
    self.empty_sound      = media.load_sound("quick_shot.wav")
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

globals = Globals()

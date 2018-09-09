import unittest
import media
import global_state
from bodies import *

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_terrain_visible(self):
        Terrain('mountain.bmp', 0, 0, 3)
        #self.assertEqual(self.seq, range(10))

if __name__ == '__main__':
    unittest.main()

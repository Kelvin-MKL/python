import unittest
from board import Board1



class MyTestCase(unittest.TestCase):
    def test_boundary(self): #screen size = 200 * 200
        self.assertTrue(Board1.boundary( 3,3))
        self.assertTrue(Board1.boundary( 100,100))
        self.assertFalse(Board1.boundary( 199,201))
        self.assertFalse(Board1.boundary( 201,3))



if __name__ == '__main__':
    unittest.main()

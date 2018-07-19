import random_name
import unittest

class MyTest(unittest.TestCase):
    def test_id_generator(self):
        self.assertEqual(len(random_name.id_generator()), 6)
if __name__ == "__main__":
    unittest.main()
import unittest
import app


class TestAppFunction(unittest.TestCase):

    def test_addition(self):
        self.assertEqual(app.addition(5, 4), 9)

    def test_divide(self):
        self.assertEqual(app.divide(12, 4), 3)
        self.assertEqual(app.divide(5, 5), 1)
        self.assertEqual(app.divide(12, 12), 1)
        self.assertEqual(app.divide(10, 2), 5)
        self.assertEqual(app.divide(-1, -1), 1)
        self.assertEqual(app.divide(12, -3), -4)
        self.assertEqual(app.divide(1, 0), 0)


if __name__ == "__main__":
    unittest.main()

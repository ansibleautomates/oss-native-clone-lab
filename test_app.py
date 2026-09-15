import unittest
from app import add

class AppTest(unittest.TestCase):
    def test_contributor_change(self):
        from app import SOURCE_MARKER
        self.assertTrue(SOURCE_MARKER.startswith("FORK_CODE"))

    def test_add(self):
        self.assertEqual(add(2, 3), 5)

if __name__ == "__main__":
    unittest.main()

import unittest

from multirange import MultiRange


class Test(unittest.TestCase):
    def test_add(self):
        r = MultiRange([(1, 2)])
        r.add(3, 5)
        self.assertEqual(r.ranges, [(1, 2), (3, 5)])
        r.add(2, 3)
        self.assertEqual(r.ranges, [(1, 5)])

        r = MultiRange([(1, 6)])
        r.add(3, 5)
        self.assertEqual(r.ranges, [(1, 6)])
        r.add(0, 1)
        self.assertEqual(r.ranges, [(0, 6)])
        r.add(6, 7)
        self.assertEqual(r.ranges, [(0, 7)])

        r = MultiRange([(1, 4)])
        r.add(3, 5)
        self.assertEqual(r.ranges, [(1, 5)])

    def test_delete(self):
        r = MultiRange([(1, 6)])
        r.delete(-3, -1)
        self.assertEqual(r.ranges, [(1, 6)])
        r.delete(-1, 10)
        self.assertEqual(r.ranges, [])

        r = MultiRange([(1, 6)])
        r.delete(4, 10)
        self.assertEqual(r.ranges, [(1, 4)])
        r.delete(2, 3)
        self.assertEqual(r.ranges, [(1, 2), (3, 4)])
        r.delete(1, 3)
        self.assertEqual(r.ranges, [(3, 4)])

    def test_get(self):
        r = MultiRange([(1, 3), (5, 7)])
        self.assertEqual(r.get(4, 5), [])

        r = MultiRange([(1, 3), (5, 6)])
        self.assertEqual(r.get(4, 6), [(5, 6)])
        self.assertEqual(r.get(2, 9), [(1, 3), (5, 6)])
        self.assertEqual(r.get(3, 4), [])
        self.assertEqual(r.get(4, 5), [])


if __name__ == "__main__":
    unittest.main()

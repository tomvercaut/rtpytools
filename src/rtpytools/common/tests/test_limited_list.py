import unittest

from common.limited_list import LimitedList


class TestLimitedList(unittest.TestCase):

    def test_append(self):
        ll = LimitedList(3)
        # Test the function under normal conditions
        ll.append(1)
        self.assertEqual(ll, [1])

        # Test with two items
        ll.append(2)
        self.assertEqual(ll, [1, 2])

        # Test with three items
        ll.append(3)
        self.assertEqual(ll, [1, 2, 3])

        # Test appending when over the limit
        ll.append(4)
        # The list should remain [1, 2, 3] since the limit is 3
        self.assertEqual(ll, [1, 2, 3])

    def test_extend_with_list(self):
        ll = LimitedList(3)
        ll.extend([1, 2, 3])
        self.assertEqual([1, 2, 3], ll)

    def test_extend_with_limited_list(self):
        ll = LimitedList(3)
        tl = LimitedList(3)
        tl.extend([4, 5, 6])
        ll.extend(tl)
        self.assertEqual([4, 5, 6], ll)

    def test_extend_with_list_and_limit(self):
        ll = LimitedList(3)
        ll.limit = 2
        ll.extend([7, 8, 9])
        self.assertEqual([7, 8], ll)

    def test_extend_with_limited_list_and_limit(self):
        ll = LimitedList(3)
        ll.limit = 2
        tl = LimitedList(3)
        tl.extend([10, 11, 12])
        ll.extend(tl)
        self.assertEqual([10, 11], ll)

    def test_extend_with_iterable(self):
        ll = LimitedList(3)
        ll.extend(iter([13, 14, 15]))
        self.assertEqual([13, 14, 15], ll)

    def test_is_limited_within_limit(self):
        ll = LimitedList(3)
        self.assertFalse(ll.is_limited())
        ll.append(1)
        self.assertFalse(ll.is_limited())
        ll.append(1)
        self.assertFalse(ll.is_limited())

    def test_is_limited_reached_limit(self):
        ll = LimitedList(3)
        for i in range(3):
            ll.append(i + 1)
        self.assertTrue(ll.is_limited())


if __name__ == '__main__':
    unittest.main()

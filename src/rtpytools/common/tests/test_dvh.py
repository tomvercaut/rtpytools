import json
import unittest

from common.dvh import Dvh, parse_json_str


class TestDvh(unittest.TestCase):

    def test_add(self):
        d = Dvh()
        self.assertEqual(0, len(d.data))
        d.add(10.0, 5.0)
        self.assertEqual(1, len(d.data))
        self.assertFalse(d.is_sorted)

    def test_is_sorted(self):
        d = Dvh()
        self.assertFalse(d.is_sorted)
        d.add(10.0, 5.0)
        self.assertFalse(d.is_sorted)
        d.sort()
        self.assertTrue(d.is_sorted)

    def test_sort(self):
        d = Dvh()
        d.add(20.0, 10.0)
        d.add(10.0, 5.0)
        d.sort()
        self.assertAlmostEqual(d.data.iloc[0]['Volume'], 10.0)
        self.assertAlmostEqual(d.data.iloc[0]['Dose'], 5.0)
        self.assertAlmostEqual(d.data.iloc[1]['Volume'], 20.0)
        self.assertAlmostEqual(d.data.iloc[1]['Dose'], 10.0)

    def test_get(self):
        d = Dvh()
        d.add(10.0, 5.0)
        d.add(20.0, 2.0)
        self.assertEqual(d.get(0), [10.0, 5.0])
        self.assertEqual(d.get(1), [20.0, 2.0])

    def test_get_volume(self):
        d = Dvh()
        d.add(10.0, 5.0)
        d.add(20.0, 2.0)
        self.assertEqual(d.get_volume(0), 10.0)
        self.assertEqual(d.get_volume(1), 20.0)

    def test_get_dose(self):
        d = Dvh()
        d.add(10.0, 5.0)
        d.add(20.0, 2.0)
        self.assertEqual(d.get_dose(0), 5.0)
        self.assertEqual(d.get_dose(1), 2.0)

    def test_dx(self):
        d = Dvh()
        d.volume = 100.0
        d.add(10.0, 5.0)
        d.add(20.0, 10.0)
        d.sort()
        self.assertEqual(d.dx(10.0), 5.0)
        self.assertEqual(d.dx(10.0, is_volume_absolute=True), 5.0)
        d.add(30, 20)
        d.add(40, 30)
        self.assertEqual(d.dx(35), 25)
        self.assertEqual(d.dx(32), 22)
        self.assertEqual(d.dx(38), 28)
        self.assertEqual(d.dx(30), 20)
        self.assertEqual(d.dx(40), 30)
        self.assertEqual(d.dx(0), None)
        self.assertEqual(d.dx(50), None)

    def test_vx(self):
        d = Dvh()
        d.volume = 100.0
        d.add(100.0, 50.0)
        d.add(90.0, 60.0)
        d.sort()
        self.assertEqual(d.vx(50.0), 100.0)
        self.assertEqual(d.vx(60.0), 90.0)
        d.add(80, 70)
        self.assertEqual(d.vx(70.0), 80.0)
        self.assertEqual(d.vx(52.0), 98.0)
        self.assertEqual(d.vx(58.0), 92.0)
        self.assertEqual(d.vx(55.0), 95.0)
        self.assertEqual(d.vx(0.0), None)
        self.assertEqual(d.vx(30.0), None)

    def test_parse_json_str_basic(self):
        json_str = """
{
  "name": "GTV",
  "volume": 50.0,
  "data": [
    {
      "volume": 100.0,
      "dose": 50.0
    },
    {
      "volume": 80.0,
      "dose": 55.0
    },
    {
      "volume": 50.0,
      "dose": 60.0
    },
    {
      "volume": 20.0,
      "dose": 65.0
    },
    {
      "volume": 2.0,
      "dose": 70.0
    }
  ]
}
        """
        data = json.loads(json_str)
        dvhs = parse_json_str(data)
        self.assertTrue(isinstance(dvhs, list))
        self.assertEqual(1, len(dvhs))
        dvh = dvhs[0]
        self.assertTrue(isinstance(dvh, Dvh))
        self.assertEqual("GTV", dvh.name)
        self.assertEqual(50.0, dvh.volume)
        self.assertEqual(5, dvh.size())
        self.assertEqual([100.0, 50.0], dvh.get(0))
        self.assertEqual([80.0, 55.0], dvh.get(1))
        self.assertEqual([50.0, 60.0], dvh.get(2))
        self.assertEqual([20.0, 65.0], dvh.get(3))
        self.assertEqual([2.0, 70.0], dvh.get(4))


if __name__ == '__main__':
    unittest.main()

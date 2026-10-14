import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from ILoveTriangle import r1, parse_float, is_triangle, triangle_type, compute_vertices


class TestTriangleModule(unittest.TestCase):

    def test_r1_rounds_positive_value_to_one_decimal(self):
        self.assertEqual(r1(3.14), 3.1)
        self.assertEqual(r1(3.16), 3.2)

    def test_parse_float_returns_none_for_none(self):
        self.assertIsNone(parse_float(None))

    def test_parse_float_returns_none_for_empty_string(self):
        self.assertIsNone(parse_float("   "))

    def test_parse_float_returns_none_for_non_numeric_text(self):
        self.assertIsNone(parse_float("abc"))

    def test_parse_float_parses_integer_string(self):
        self.assertEqual(parse_float(" 42 "), 42.0)

    def test_parse_float_parses_float_string(self):
        self.assertEqual(parse_float("3.14"), 3.14)

    def test_is_triangle_returns_true_for_valid_sides(self):
        self.assertTrue(is_triangle(3, 4, 5))

    def test_is_triangle_returns_false_for_zero_side(self):
        self.assertFalse(is_triangle(0, 4, 5))

    def test_is_triangle_returns_false_for_negative_side(self):
        self.assertFalse(is_triangle(-3, 4, 5))

    def test_is_triangle_returns_false_for_degenerate_triangle(self):
        self.assertFalse(is_triangle(1, 2, 3))

    def test_is_triangle_returns_false_when_inequality_fails(self):
        self.assertFalse(is_triangle(2, 3, 6))

    def test_triangle_type_returns_equilateral(self):
        self.assertEqual(triangle_type(5, 5, 5), "равносторонний")

    def test_triangle_type_returns_isosceles(self):
        self.assertEqual(triangle_type(5, 5, 6), "равнобедренный")

    def test_triangle_type_returns_scalene(self):
        self.assertEqual(triangle_type(3, 4, 5), "разносторонний")

    def test_compute_vertices_returns_three_points(self):
        self.assertEqual(len(compute_vertices(3, 4, 5)), 3)

    def test_compute_vertices_returns_integer_coordinates(self):
        points = compute_vertices(3, 4, 5)
        for x, y in points:
            self.assertIsInstance(x, int)
            self.assertIsInstance(y, int)

    def test_compute_vertices_stays_within_canvas(self):
        size = 100
        padding = 5
        points = compute_vertices(3, 4, 5, size=size, padding=padding)
        for x, y in points:
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x, size)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(y, size)

    def test_compute_vertices_handles_very_small_triangle(self):
        points = compute_vertices(0.1, 0.1, 0.1)
        self.assertEqual(len(points), 3)


if __name__ == "__main__":
    unittest.main()
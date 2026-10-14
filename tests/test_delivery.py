import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from Delivery import calculate_delivery_cost


class TestDeliveryCost(unittest.TestCase):

    def test_invalid_weight_too_small_returns_error(self):
        self.assertEqual(calculate_delivery_cost(0.05, 100, "обычный"), (-1, "0000-00-00"))

    def test_invalid_weight_too_large_returns_error(self):
        self.assertEqual(calculate_delivery_cost(50.1, 100, "обычный"), (-1, "0000-00-00"))

    def test_invalid_distance_too_small_returns_error(self):
        self.assertEqual(calculate_delivery_cost(1, 0, "обычный"), (-1, "0000-00-00"))

    def test_invalid_distance_too_large_returns_error(self):
        self.assertEqual(calculate_delivery_cost(1, 5001, "обычный"), (-1, "0000-00-00"))

    def test_invalid_package_type_returns_error(self):
        self.assertEqual(calculate_delivery_cost(1, 100, "жидкий"), (-1, "0000-00-00"))

    def test_min_valid_weight_and_distance(self):
        self.assertEqual(calculate_delivery_cost(0.1, 1, "обычный"), (205, "2026-09-04"))

    def test_weight_above_five_gets_twenty_percent_surcharge(self):
        self.assertEqual(calculate_delivery_cost(5.1, 100, "обычный"), (840, "2026-09-04"))

    def test_weight_twenty_gets_fifty_percent_surcharge(self):
        self.assertEqual(calculate_delivery_cost(20, 100, "обычный"), (1050, "2026-09-04"))

    def test_fragile_package_adds_three_hundred(self):
        self.assertEqual(calculate_delivery_cost(2, 100, "хрупкий"), (1000, "2026-09-04"))

    def test_dangerous_package_adds_one_thousand(self):
        self.assertEqual(calculate_delivery_cost(2, 100, "опасный"), (1700, "2026-09-04"))

    def test_regular_short_distance_delivery_date(self):
        self.assertEqual(calculate_delivery_cost(1, 400, "обычный"), (2200, "2026-09-04"))

    def test_regular_thousand_km_delivery_date(self):
        self.assertEqual(calculate_delivery_cost(1, 1000, "обычный"), (5200, "2026-09-05"))

    def test_express_cost_is_higher_than_regular(self):
        regular = calculate_delivery_cost(2, 100, "обычный", False)[0]
        express = calculate_delivery_cost(2, 100, "обычный", True)[0]
        self.assertGreater(express, regular)

    def test_express_short_distance_not_delivered_before_next_day(self):
        _, date_str = calculate_delivery_cost(2, 400, "обычный", True)
        self.assertGreaterEqual(date_str, "2026-09-04")

    def test_express_reduces_days_for_long_distance(self):
        regular_date = calculate_delivery_cost(1, 2000, "обычный", False)[1]
        express_date = calculate_delivery_cost(1, 2000, "обычный", True)[1]
        self.assertLess(express_date, regular_date)


if __name__ == "__main__":
    unittest.main()
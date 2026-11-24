import unittest
from AddingAndCreating import (
    add_item_to_order,
    add_menu_item,
    create_menu,
    create_order,
)


class TestRestaurantFunctions(unittest.TestCase):
    def setUp(self):
        """Create a fresh menu and order before each test method."""
        self.menu = create_menu()
        self.order = create_order("ORD-101")

    def test_create_default_menu(self):
        self.assertEqual(
            self.menu,
            {
                "burger": 120.0,
                "fries": 45.0,
                "cola": 25.0,
            },
        )

    def test_create_custom_menu_normalizes_names(self):
        custom_menu = create_menu({"  Pizza ": 150, "Salad": 70.5})
        self.assertEqual(custom_menu, {"pizza": 150.0, "salad": 70.5})

    def test_add_menu_item_adds_and_updates(self):
        add_menu_item(self.menu, "  Juice ", 35)
        self.assertEqual(self.menu["juice"], 35.0)

        # Updating an existing item's price
        add_menu_item(self.menu, "burger", 130.0)
        self.assertEqual(self.menu["burger"], 130.0)

    def test_add_menu_item_invalid_name_or_price(self):
        with self.assertRaises(ValueError):
            add_menu_item(self.menu, "   ", 50.0)

        with self.assertRaises(ValueError):
            add_menu_item(self.menu, "Tea", 0)

        with self.assertRaises(ValueError):
            add_menu_item(self.menu, "Tea", -10)

    def test_create_order_valid_and_invalid(self):
        order = create_order("  ORD-202  ")
        self.assertEqual(order["id"], "ORD-202")
        self.assertEqual(order["items"], [])
        self.assertEqual(order["status"], "PENDING")

        with self.assertRaises(ValueError):
            create_order("   ")

    def test_add_item_to_order_new_and_duplicate_items(self):
        add_item_to_order(self.order, self.menu, "Burger", 1)
        add_item_to_order(self.order, self.menu, "burger", 2)

        self.assertEqual(len(self.order["items"]), 1)
        self.assertEqual(
            self.order["items"][0],
            {"name": "burger", "price": 120.0, "qty": 3},
        )

    def test_add_item_to_order_missing_item_raises_key_error(self):
        with self.assertRaises(KeyError):
            add_item_to_order(self.order, self.menu, "pasta", 1)

    def test_add_item_to_order_invalid_qty_raises_value_error(self):
        with self.assertRaises(ValueError):
            add_item_to_order(self.order, self.menu, "fries", 0)

        with self.assertRaises(ValueError):
            add_item_to_order(self.order, self.menu, "fries", -2)

    def test_add_item_to_order_closed_order_raises_value_error(self):
        self.order["status"] = "DELIVERED"
        with self.assertRaises(ValueError):
            add_item_to_order(self.order, self.menu, "cola", 1)

        self.order["status"] = "CANCELLED"
        with self.assertRaises(ValueError):
            add_item_to_order(self.order, self.menu, "cola", 1)


if __name__ == "__main__":
    unittest.main()
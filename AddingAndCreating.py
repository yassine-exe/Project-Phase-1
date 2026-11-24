from typing import Dict


def create_menu(initial_items: Dict[str, float] | None = None) -> Dict[str, float]:
    """Create a menu dictionary mapping item name -> price."""
    if initial_items is None:
        return {
            "burger": 120.0,
            "fries": 45.0,
            "cola": 25.0,
        }

    menu: Dict[str, float] = {}
    for name, price in initial_items.items():
        add_menu_item(menu, name, price)
    return menu


def add_menu_item(menu: Dict[str, float], item_name: str, price: float) -> Dict[str, float]:
    """Add or update an item in the menu."""
    clean_name = item_name.strip().lower()
    if not clean_name:
        raise ValueError("Item name cannot be empty.")
    if price <= 0:
        raise ValueError("Price must be greater than zero.")

    menu[clean_name] = float(price)
    return menu


def create_order(order_id: str) -> dict:
    """Create a new empty order."""
    if not order_id or not order_id.strip():
        raise ValueError("Order ID cannot be empty.")

    return {
        "id": order_id.strip(),
        "items": [],  # list of {"name": str, "price": float, "qty": int}
        "status": "PENDING",
    }


def add_item_to_order(order: dict, menu: Dict[str, float], item_name: str, qty: int = 1) -> dict:
    """Add a menu item with quantity to an order."""
    if order["status"] in ("DELIVERED", "CANCELLED"):
        raise ValueError(f"Cannot modify an order with status {order['status']}.")
    if qty <= 0:
        raise ValueError("Quantity must be greater than zero.")

    clean_name = item_name.strip().lower()
    if clean_name not in menu:
        raise KeyError(f"Item '{item_name}' is not on the menu.")

    for entry in order["items"]:
        if entry["name"] == clean_name:
            entry["qty"] += qty
            return order

    order["items"].append({
        "name": clean_name,
        "price": menu[clean_name],
        "qty": qty,
    })
    return order
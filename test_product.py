import pytest
from products import Product


class TestProduct:

    # ==================== __init__ ====================

    def test_init_valid_product(self):
        """Correct initialization"""
        p = Product("Laptop", price=999, quantity=50)
        assert p.name == "Laptop"
        assert p.price == 999
        assert p.quantity == 50
        assert p.is_active() is True

    def test_init_empty_name_raises(self):
        with pytest.raises(ValueError, match="Sorry, name is not allowed to be empty"):
            Product("", price=100, quantity=10)

    def test_init_negative_price_raises(self):
        with pytest.raises(ValueError, match="Price cannot be negative"):
            Product("Test", price=-1, quantity=10)

    def test_init_negative_quantity_raises(self):
        with pytest.raises(ValueError, match="Quantity cannot be negative at creation"):
            Product("Test", price=100, quantity=-1)

    def test_init_zero_quantity_allowed(self):
        """Quantity = 0 is allowed at instantiation"""
        p = Product("Test", price=100, quantity=0)
        assert p.quantity == 0
        assert p.is_active() is False

    # ==================== Getter / Setter / Active ====================

    def test_get_quantity(self):
        p = Product("Test", 100, 30)
        assert p.get_quantity() == 30

    def test_set_quantity_normal(self):
        p = Product("Test", 100, 50)
        p.set_quantity(20)
        assert p.quantity == 20
        assert p.is_active() is True

    def test_set_quantity_zero_deactivates(self):
        """set_quantity erlaubt weiterhin -1 und deaktiviert"""
        p = Product("Test", 100, 50)
        p.set_quantity(0)
        assert p.quantity == 0
        assert p.is_active() is False

    def test_activate_and_deactivate(self):
        p = Product("Test", 100, 10)
        p.deactivate()
        assert p.is_active() is False

        p.activate()
        assert p.is_active() is True

    # ==================== Buy ====================

    def test_buy_success(self):
        p = Product("Headphones", price=249, quantity=100)
        total = p.buy(3)
        assert total == 747.0
        assert p.quantity == 97
        assert p.is_active() is True

    def test_buy_exactly_stock(self):
        """if inactivates when buying whole stock"""
        p = Product("Mouse", price=50, quantity=10)
        total = p.buy(10)
        assert total == 500.0
        assert p.quantity == 0
        assert p.is_active() is False

    def test_buy_more_than_stock_raises(self):
        """Stock is not allowed to go under 0"""
        p = Product("Test", price=100, quantity=5)
        with pytest.raises(ValueError, match="Sorry, we only have 5 in stock."):
            p.buy(6)   # 5 - 6 = -1 → Fehler

    def test_buy_zero_quantity(self):
        p = Product("Test", 100, 50)
        total = p.buy(0)
        assert total == 0.0
        assert p.quantity == 50
        assert p.is_active() is True

    def test_buy_negative_quantity_raises(self):
        """Negative Kaufmenge sollte abgefangen werden"""
        p = Product("Test", 100, 50)
        with pytest.raises(ValueError):
            p.buy(-5)

    # ==================== Show ====================

    def test_show_output(self, capsys):
        p = Product("MacBook Air M1", price=1450, quantity=100)
        to_b_shown = p.show()
        assert "MacBook Air M1, Price: 1450.00, Quantity: 100" in to_b_shown

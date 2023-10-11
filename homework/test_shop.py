import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book",100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


@pytest.fixture
def empty_cart():
    return Cart()


class TestProducts:

    def test_product_check_quantity(self, product):
        assert product.check_quantity(500) == True
        assert product.check_quantity(1500) == False

        assert product.check_quantity(product.quantity - 1) == True
        assert product.check_quantity(product.quantity + 1) == False

    def test_product_buy(self, product):
        product.buy(1000)
        assert product.quantity == 0

    def test_product_buy_more_than_available(self, product):
        with pytest.raises(ValueError):
            product.buy(1001)


class TestCart:

    def test_add_product_to_cart(self, cart, product):
        cart.add_product(product,1)
        assert len(cart.products) == 1
        assert cart.products[product] == 1

    def test_add_and_remove_product_from_cart(self, cart, product):
        cart.add_product(product,100)
        cart.remove_product(product,50)
        assert product in cart.products
        assert cart.products[product] == 50

    def test_clear_cart(self, cart, product):
        cart.add_product(product)
        cart.clear()
        assert not cart.products

    def test_get_price_with_products(self, cart, product):
        cart.add_product(product, 6)
        assert cart.get_total_price() == 600

    def test_empty_cart(self, empty_cart):
        try:
            empty_cart.buy()
        except ValueError as e:
            assert str(e) == "Корзина пуста"

    def test_cart_buy(self, cart, product):
        cart.add_product(product, 1000)
        cart.buy()
        assert product.quantity == 0

    def test_cart_buy_more_than_available(self, cart, product):
        cart.add_product(product, 1500)
        with pytest.raises(ValueError):
            cart.buy()
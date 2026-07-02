# from products import Product
import products as products_module

class Store():
    """contains one variable - a list of products that exist in the store and facilitates multi product purchase"""

    def __init__(self, products: list):
        if not isinstance(products, list):
            raise ValueError('Sorry, this is not a list form')
        self.products = products

    def add_product(self, product):
        """
        Adds product to the Store(list of self.products)
        :param product: product
        """
        self.products.append(product)

    def remove_product(self, product):
        """
        Removes a product from store.
        :param product: product
        """
        self.products.remove(product)

    def get_total_quantity(self) -> int:
        """
        Returns how many items are in the store in total
        :return: items in store total
        """
        number_of_products = 0
        for product in self.products:
            number_of_products += product.get_quantity()
        return number_of_products

    def get_all_products(self) -> list[products_module.Product]:
        """
        Returns all products in the store that are active
        :return: list of ACTIVE products
        """
        active_products = []
        for product in self.products:
            if product.is_active():
                active_products.append(product)
        return active_products


    def order(self, shopping_list: list[tuple[products_module.Product, int]]) -> float:
        """
        Gets a list of tuples, where each tuple has 2 items:
        Product (Product class) and quantity (int).
        Buys the products and returns the total price of the order.
        :param shopping_list:
        :return: total price of the order
        """
        shopping_list_total_price = 0
        for product_ordered, quantity in shopping_list:
                shopping_list_total_price += product_ordered.buy(quantity)
        return shopping_list_total_price

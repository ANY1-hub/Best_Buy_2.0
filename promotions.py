from abc import ABC, abstractmethod
import products as products_module

class Promotion(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def apply_promotion(self, product: products_module.Product, quantity) -> float:
        """
        receives a product instance and a quantity for it. Applies the discount rate and returns the discounted price.
        :param product: Product instance
        :param quantity: quantity of the product instance
        :return: discounted price as float (product price * quantity => applied discount)
        """
        pass


class SecondHalfPrice(Promotion):

    def __init__(self, name ):
        super().__init__(name)

    def apply_promotion(self, product: products_module.Product, quantity) -> float:
        """
        receives a product instance and a quantity for it. Applies the discount rate and returns the discounted price.
        :param product: Product instance
        :param quantity: quantity of the product instance
        :return: discounted price as float (product price * quantity => applied discount)
        """
        count_reduced_items = quantity // 2
        count_full_paid_items = quantity - count_reduced_items
        reduced_amount = product.price * count_reduced_items
        full_priced_amount = product.price * count_full_paid_items
        sum_to_pay = reduced_amount + full_priced_amount
        return sum_to_pay

class ThirdOneFree(Promotion):
    """discount where after buying 2 of that item, the third one is free"""
    def __init__(self, name):
        super().__init__(name)

    def apply_promotion(self, product: products_module.Product, quantity) -> float:
        """
        receives a product instance and a quantity for it. Applies the discount rate and returns the discounted price.
        :param product: Product instance
        :param quantity: quantity of the product instance
        :return: discounted price as float (product price * quantity => applied discount)
        """
        count_free_items = quantity // 3
        count_full_paid_items = quantity - count_free_items
        return product.price * count_full_paid_items


class PercentDiscount(Promotion):
    """ applies percentual discount to the price of the product """
    def __init__(self, name, percent: float|int ):
        super().__init__(name)
        self.percent = percent

    def apply_promotion(self, product: products_module.Product, quantity) -> float:
        """
        receives a product instance and a quantity for it. Applies the discount rate and returns the discounted price.
        :param product: Product instance
        :param quantity: quantity of the product instance
        :return: discounted price as float (product price * discount value 8 quantity)
        """
        return product.price *  (1 - self.percent / 100) * quantity



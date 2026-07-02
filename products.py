from config import colors


class Product:
    """ Represents a specific type of product available in the store
        (For example, MacBook Air M2). It encapsulates information about
        the product, including its name and price. It includes an
        attribute to keep track of the total quantity of items of
        that product currently available in the store."""
    def __init__(self, name, price, quantity, active=True):
        if name == '':
            raise ValueError("Sorry, name is not allowed to be empty")
        self.name = name

        if price < 0:
            raise ValueError("Price cannot be negative")
        self.price = price

        if quantity < 0:
            raise ValueError("Quantity cannot be negative at creation")
        elif quantity == 0:
            self.active = False
        else:
            self.active = active
        self.quantity = quantity
        self.promotion = None

    # ------------- getters --------------

    def get_quantity(self) -> int:
        """
        Getter function for quantity.
        :return: quantity (int)
        """
        return self.quantity

    def get_promotion(self):
        """
        Getter function for promotions
        :return: promotions
        """
        return self.promotion

    def is_active(self) -> bool:
        """
        Getter function for active.
        :return:
        """
        return self.active


    # ------------- setters --------------

    def set_quantity(self, quantity):
        """
        Setter function for quantity. If quantity reaches 0, deactivates the product.
        :param quantity:
        :return: True if the product is active, otherwise False.
        """
        if quantity <= 0:
            self.deactivate()
        elif quantity > 0:
            self.activate()
        self.quantity = quantity

    def set_promotion(self, promotion):
        """
	    sets the promotion of the product
	    """
        self.promotion = promotion

    def activate(self):
        """
        Activates the product.
        """
        self.active = True

    def deactivate(self):
        """
        Deactivates the product
        :return:
        """
        self.active = False

    def show(self):
        """
        Returns a printable string that represents the product, for example:
        "MacBook Air M1, Price: 1450, Quantity: 100"
        :return: string representation of a product
        """
        if self.promotion:
            return (f'{colors.YELLOW}{self.name}:{colors.RESET}\n\tPrice: {colors.CYAN}{self.price:.2f}{colors.RESET}, '
                f'Quantity: {colors.CYAN}{self.quantity}{colors.RESET}\n\tPromotion: {colors.GREEN}{self.promotion.name}{colors.RESET}\n')
        return (f'{colors.YELLOW}{self.name}:{colors.RESET}\n\tPrice: {colors.CYAN}{self.price:.2f}{colors.RESET}, '
            f'Quantity: {colors.CYAN}{self.quantity}{colors.RESET}\n')

    def buy(self, quantity) -> float:
        """
        Buys a given quantity of the product.
        Updates the quantity of the product.
        In case of a problem, raises an Exception.
        :param quantity:
        :return: total price (float) of the purchase
        """
        if quantity < 0:
            raise ValueError('Sorry, you cannot buy negative quantities.')
        if self.quantity - quantity < 0:
            raise ValueError(f'Sorry, we only have {self.quantity} in stock.')
        self.set_quantity(self.quantity - quantity)
        if self.promotion:
            return float(self.promotion.apply_promotion(self, quantity))
        return float(quantity * self.price)


class NonStockedProduct(Product):
    """ Represents a specific non stockable type of product available in the store

        (For example, Windows11 License). It encapsulates information about
        the product, including its name and price. It DOES NOT have a quantity for stock.
    """
    def __init__(self, name, price):
        super().__init__(name, price,0)
        self.active = True


    def set_quantity(self, quantity):
        if quantity != 0:
           raise (ValueError('This Product has no Stock. Please do not try to modify it'))

    def show(self):
        """
        Returns a printable string that represents the product, for example:
        "Windows License, Price: 1450"
        :return: string representation of a product
        """
        if self.promotion:
            return f'{colors.YELLOW}{self.name}:{colors.RESET}\n\tPrice: {colors.CYAN}{self.price:.2f}{colors.RESET}\n\tPromotion: {colors.GREEN}{self.promotion.name}{colors.RESET}\n'
        return f'{colors.YELLOW}{self.name}:{colors.RESET}\n\tPrice: {colors.CYAN}{self.price:.2f}{colors.RESET}\n'

    def buy(self, quantity) -> float:
        """
        Buys a given quantity of the product.
        In case of a problem, raises an Exception.
        :param quantity: qnty to buy, but no Stock change as no stock for this product
        :return: total price (float) of the purchase
        """
        if quantity < 0:
            raise ValueError('Sorry, you cannot buy negative quantities.')
        if self.promotion:
            return float(self.promotion.apply_promotion(self, quantity))
        return float(quantity * self.price)


class LimitedProduct(Product):
    """
    Buys a limited quantity of the product.
    In case of a problem, raises an Exception.
    :param quantity: qnty to buy, but no Stock change as no stock for this product
    :maximum: maximum quantity in an order
    :return: total price (float) of the purchase
    """
    def __init__(self, name, price, quantity, maximum):
        super().__init__(name, price, quantity)
        if maximum < 1:
            raise ValueError('Please enter a maximum order quantity')
        self.maximum = maximum

    def get_maximum(self) -> int:
        """
        Getter function for quantity.
        :return: quantity (int)
        """
        return self.maximum


    def set_maximum(self, maximum):
        """set maximum number of product purchasable in an order"""
        self.maximum = maximum

    def show(self):
        """
        Returns a printable string that represents the product, for example:
        "Windows License, Price: 1450"
        :return: string representation of a product
        """
        if self.promotion:
            return (f'{colors.YELLOW}{self.name}:{colors.RESET}\n\tPrice: {colors.CYAN}{self.price:.2f}{colors.RESET}, '
                   f'Maximum per Order: {colors.CYAN}{self.maximum}{colors.RESET}\n\tPromotion: {colors.GREEN}{self.promotion.name}{colors.RESET}')
        return (f'{colors.YELLOW}{self.name}:{colors.RESET}\n\tPrice: {colors.CYAN}{self.price:.2f}{colors.RESET}, '
                   f'Maximum per Order: {colors.CYAN}{self.maximum}{colors.RESET}')

    def buy(self, quantity) -> float:
        """
        Buys a quantity of the product limited by a maximum.
        In case of a problem, raises an Exception.
        :param quantity: qnty to buy, but no Stock change as no stock for this product
        :return: total price (float) of the purchase
        """
        if quantity < 0:
            raise ValueError('Sorry, you cannot buy negative quantities.')
        if self.quantity - quantity < 0:
            raise ValueError(f'Sorry, we only have {self.quantity} in stock.')
        if quantity > self.maximum:
            raise ValueError(f'Sorry, you can order at most {self.maximum} of this product')
        self.set_quantity(self.quantity - quantity)
        if self.promotion:
            return float(self.promotion.apply_promotion(self, quantity))
        return float(self.price * quantity)
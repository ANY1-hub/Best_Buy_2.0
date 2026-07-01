class Product():
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
        self.quantity = quantity

        self.active = active

    def get_quantity(self) -> int:
        """
        Getter function for quantity.
        :return: quantity (int)
        """
        return self.quantity

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

    def is_active(self) -> bool:
        """
        Getter function for active.
        :return:
        """
        return self.active


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
        return (f'{self.name}, Price: {self.price:.2f}, Quantity: {self.quantity}')


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
        return float(quantity * self.price)

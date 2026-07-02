from config import colors
import products as products_module
import promotions as promotions_module
import store as store_module

# setup initial stock of inventory ===========================================================
product_list = [ products_module.Product("MacBook Air M2", price=1450, quantity=100),
                 products_module.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                 products_module.Product("Google Pixel 7", price=500, quantity=250),
                 products_module.NonStockedProduct("Windows License", price=125),
                 products_module.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
                 ]

# Create promotion catalog
second_half_price = promotions_module.SecondHalfPrice("Second Half price!")
third_one_free = promotions_module.ThirdOneFree("Third One Free!")
thirty_percent = promotions_module.PercentDiscount("30% off!", percent=30)

# Add promotions to products
product_list[0].set_promotion(second_half_price)
product_list[1].set_promotion(third_one_free)
product_list[3].set_promotion(thirty_percent)

best_buy = (store_module.Store(product_list))
# ============================================================================================


def start(store_instance):
    """
    handles the main menu
    :return: None
    """

    exit_item = len(menu_items) - 1
    while True:
        print("\n")
        for i, item in enumerate(menu_items):
            print(f"{colors.CYAN}{i + 1}.{colors.RESET}\t {item[0]}")
        try:
            menu_choice = int(
                input(
                    f"\nPlease choose: {colors.YELLOW}({colors.CYAN}1-{len(menu_items)}"
                    f"{colors.YELLOW}){colors.RESET}: ")) - 1
        except ValueError:
            print(f"\n{colors.YELLOW}Ooops, This was not a {colors.BRIGHT}number "
                  f"{colors.NORMAL}{colors.RESET}")
            continue
        if (len(menu_items) - 1 < menu_choice or menu_choice < 0) and isinstance(menu_choice, int):
            print(
                f"\n{colors.RED}Please enter one of the {colors.BRIGHT}menu item{colors.NORMAL}s "
                f"{colors.BRIGHT}number{colors.RESET}\n")
            continue

        if menu_choice == exit_item:
            break
        menu_items[menu_choice][1](store_instance)


def list_all_products_in_store(store_instance):
    """lists all products in the store"""
    all_products = store_instance.get_all_products()
    for item in all_products:
        print(item.show())


def show_total_items_in_store(store_instance):
    """shows total number of items in store"""
    total_number = store_instance.get_total_quantity()
    print(f'total number of products : {total_number}')

def get_order_input(store_instance):
    """ gets user input for the order (state machine)
        collects all info in a list (cart) and when finished, sends it to processing
    """
    cart = [] # list[tuple[Product, int]]
    all_products = store_instance.get_all_products()
    while True:
        print("\n")
        if all_products:
            for i, item in enumerate(all_products):
                print(f'{colors.CYAN}{i + 1}.{colors.RESET}\t {item.name}')
            try:
                item_choice = int(
                    input(
                        f"\nPlease enter the product id: {colors.YELLOW}({colors.CYAN}1-{len(all_products)}"
                        f"{colors.YELLOW}){colors.RESET}: ")) - 1

                if item_choice >= len(all_products)  or item_choice < 0:
                    print(
                        f"\n{colors.RED}Please enter one of the {colors.BRIGHT} item{colors.NORMAL}s "
                        f"{colors.BRIGHT}number{colors.RESET}\n")
                    continue

                order_quantity = int(input('How many would you like to buy?: '))
                on_stock = all_products[item_choice].get_quantity()

                # check if product is LimitedProduct for maximum order quantity
                if isinstance(all_products[item_choice], products_module.LimitedProduct):
                    maximum = all_products[item_choice].get_maximum()
                    quantity_in_cart = 0
                    for cart_product in cart:
                        if cart_product[0] == all_products[item_choice]:
                            quantity_in_cart += cart_product[1]
                    if order_quantity + quantity_in_cart > maximum:
                        if input(f'\nYou can only order {maximum} of this product. '
                                 f'Would you like that quantity? (y/*): ') in ('y', 'yes'):
                            order_quantity = maximum - quantity_in_cart
                        else:
                            continue

                # check if order quantity is on stock
                if order_quantity > on_stock and not isinstance(all_products[item_choice], products_module.NonStockedProduct):
                    print(f'\nSorry we have only {on_stock} pieces on stock.\n')
                    if input('Would you like to buy them? (y/*): ') in ('y','yes'):
                        cart.append((all_products[item_choice],on_stock))
                    continue
                cart.append((all_products[item_choice], order_quantity))

            except ValueError:
                print(f"\n{colors.YELLOW}Ooops, This was not a valid {colors.BRIGHT}number "
                      f"{colors.NORMAL}{colors.RESET}")
                continue

            if input('\nContinue Shopping? (y/*): ') not in ('y','yes'):
                break
    if cart:
        process_order(store_instance, cart)


def process_order(store_instance, shopping_cart:list[tuple[products_module.Product, int]]):
    """processes the order"""
    for shopping_cart_item, qnty in shopping_cart:
        if shopping_cart_item.promotion:
            print(f'{shopping_cart_item.name}:\n\tquantity: {qnty}\n\tdiscount: {shopping_cart_item.promotion.name}\n\t'
                  f'Product price total: {qnty * shopping_cart_item.price:.2f}EUR\n\t')
                  # f'Discounted product price total: {}')
        else:
            print(f'{shopping_cart_item.name}: quantity: {qnty}, '
                  f'price: {qnty * shopping_cart_item.price:.2f}EUR')
    print(f'Order value total: {store_instance.order(shopping_cart):.2f}EUR')


menu_items = [("List all products in store", list_all_products_in_store),
              ("Show total quantity in store", show_total_items_in_store),
              ("Make an order", get_order_input),
              ("Quit", None)]


def main():
    """Main entry point of the application."""
    print(
        f"\n\n{colors.GREEN_B}**********{colors.RESET_B} {colors.YELLOW}Best buy{colors.RESET} "
        f"{colors.GREEN_B}**********{colors.RESET_B}")
    start(best_buy)


if __name__ == '__main__':
    main()


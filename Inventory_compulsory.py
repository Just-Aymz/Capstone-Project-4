import os
from tabulate import tabulate


class Shoe:
    """
    Represents a shoe object within an inventory system. With the
    country where the shoe is going, the unique code to identify the
    product, the product name, the cost of the product per unit, as
    well as the total number of units
    """
    def __init__(self, country, code, product, cost, quantity) -> None:
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        """
        Returns the cost of the Shoe object
        """
        self.cost

    def get_quantity(self):
        """
        Returns the quantity remaining of the Shoe object
        """
        self.quantity

    def shoe_dict(self):
        """
        Returns a dictionary of the attributes of the Shoe object
        """
        dct = {
            'country': self.country,
            'code': self.code,
            'product': self.product,
            'cost': self.cost,
            'quantity': self.quantity
        }

        return dct

    def __str__(self) -> str:
        """
        Returns the details of the Shoe object as a dictionary
        """
        f"Country: {self.country}"
        f"Code: {self.code}"
        f"Product: {self.product}"
        f"Cost: {self.cost}"
        f"Quantity: {self.quantity}"


def directory_path(filename):
    """
    A function that finds the filepath on a system depending on where
    this file is on the system, and takes in the filename as an input,
    to create the filepath to the file.

    Args:
        filename(str): The name of the desired .txt file as a string

    Returns:
        filepath(str): The filepath to the program and file
    """
    dirpath = os.path.dirname((__file__))
    filepath = os.path.join(dirpath, filename)

    return filepath


def menu():
    """
    A function that is responsible for returning a menu in the desired
    format and requests an input from the user from the menu.

    Return:
        user_request(str): Input from the user from the menu options
    """
    print("\nWelcome to HyperionDev's Inventory App!")
    print("*"*65)
    print("a - To add a new shoe product on the database")
    print("v - To view all the products that are on the database")
    print("r - To restock on products with the lowest quantity")
    print("vi - To view the total value of each item")
    print("dsc - To view the shoe on sale right now!")
    print("s - To search for a particular shoe using its SKUcode")
    print("q - To to quit application", end="")
    user_request = input(": ").strip().lower()

    return user_request


def file_read(filename):
    """
    A function responsible for reading in a .txt file and storing
    its contents as a variable

    Args:
        filename(str): A .txt file that is in the same directory as
        the programe

    Return:
        content(list): A list of all the lines within the .txt file
        with each new line represented as an element in the list.

    """
    file = directory_path(filename)
    with open(file, "r", encoding="utf-8") as file:
        content = file.readlines()

    return content


def object_creation(filename, products_list):
    """
    A function that is responsible for reading in a .txt file for read
    only function, and creates Shoe objects by passing the information
    in the file on each line into the Shoe class to build a Shoe object
    and append that Shoe object into an empty list

    Args:
        filename(str): A .txt file in the same directory as the program
        products_list(list): An empty list to append each new Shoe
        object

    Returns:
        products_list(list): An non-empty list containing Shoe objects
        created from the contents of the read in .txt file
    """
    content = file_read(filename)
    for line in content[1:]:
        information_list = list(line.split(","))
        information_list = [element.strip() for element in information_list]
        shoe_object = Shoe(*information_list).shoe_dict()
        products_list.append(shoe_object)

    return products_list


def write_file(filename, method, data):
    """
    A function that is responsible for appending new data onto an
    existing .txt file in the same direcctory as the program. If the
    file does not exist, it creates one, and if it does it appends the
    input data to the existing data found in the file

    Args:
        filename(str): A .txt file in the same directory as the program
    """
    file = directory_path(filename)
    with open(file, method, encoding="utf-8") as file:
        content_to_append = data
        file.write(content_to_append)


def user_input_requests():
    """
    A function that prompts the user for information about the details
    of a new shoe to be added to the database.

    Returns:
        new_shoe(dict): A dictionary with the following keys: country,
        code, product, cost and quantity and user input for values
    """
    while True:
        try:
            print()
            # Title case the input from the user
            country = input(
                "Which country will the inventory be going?: ").title()
            code = input("What is the SKU 5-digit code for the products?: ")
            # Title case the input from the user
            product = input("Product name?: ").title()
            # Ensure that cost and quantity are integers
            cost = int(input("Unit cost?: R"))
            quantity = int(input("Total number of units?: "))

            if (code.isdigit()) & (5 <= len(code) < 6):
                new_shoe = {
                    "country": country,
                    "code": f"SKU{code}",
                    "product": product,
                    "cost": cost,
                    "quantity": quantity
                }
                break
            else:
                print("\nPlease confirm SKU code consists of 5 digits only\n")
        except ValueError:
            # If cost or quantity are not integers, execute this code
            print("Please ensure that unit cost and quanitity", end=" ")
            print("are integer values")

    return new_shoe


def capture_shoe():
    """
    A function that is responsible for taking user information to
    create a new Shoe object and appends that new shoe into the
    list provided at function call.

    Args:
        products_list(list): An empty list to append each new Shoe
        object

    Returns:
        shoe_append(str): A string formated to append the new shoe
        into a .txt file
    """
    user_input = user_input_requests()
    shoe_object = Shoe(**user_input)

    shoe_append = (
        f"{shoe_object.country}, {shoe_object.code}, {shoe_object.product}, "
        f"{shoe_object.cost}, {shoe_object.quantity}"
        )

    return shoe_append


def view_all(products_list):
    """
    A function responsible for creating a list of dictionaries into a
    a table view with the keys as the column names.

    Args:
        product_list(list): A list of dictionaries

    Return:
        table(str): Formatted string into a table format.
    """
    table = tabulate(products_list, headers="keys", showindex="always")
    print(table)
    print()


def search(product_list):
    found_shoe = False
    while not found_shoe:
        print("\nPlease provide the SKU code of the shoe you are", end=" ")
        # Ensure the code provided is in uppercase.
        SKUcode = input("searching for: ").upper().strip()
        for dct in product_list:
            # Use list comprehension to get the keys of the dictionary
            # as a list
            keys_list = [list(dct.keys())[i] for i in range(len(dct.keys()))]
            if dct.get("code") == SKUcode:
                print(
                    f'{keys_list[0]}: \t{dct.get("country")}\n'
                    f'{keys_list[1]}: \t\t{dct.get("code").strip()}\n'
                    f'{keys_list[2]}: \t{dct.get("product")}\n'
                    f'{keys_list[3]}: \t\tR{dct.get("cost")}.00\n'
                    f'{keys_list[4]}: \t{dct.get("quantity").strip()}\n'
                )
                found_shoe = True
                break
        else:
            print("SKU code not in database. Please try again")
            print("s - To search again")
            print("m - To go back to menu", end=" ")
            # Remove any blank space from user input and store input
            # as lower case
            choice = input(": ").lower().strip()
            if choice == "m":
                break
            else:
                continue
        break


def value_per_item(product_list):
    """
    A function that is responsible for calculating the product between
    the quantity of each shoe, and its unit cost.

    Args:
        product_list(list): a list of all the shoe objects in the
        database

    Return:
        value(int): returns the product of each shoes quantity and unit
        cost, neatly formatted to include the name of the shoe object.
    """
    for shoe in product_list:
        print(f'\n{shoe.get("product").strip()}:')
        print("Total value per item:", end=" ")
        # Ensure the quantity of the shoe and the cost of the shoe are
        # an integer and with no trailing whitespace
        value = (int(shoe.get("quantity").strip())
                 * int(shoe.get("cost").strip()))
        print(f"R{value}.00\n")


def shoe_for_sale(product_list):
    """
    A function that is responsible for creating a list of all the
    quantities of the shoes available into an integer and storing
    the maximum value within that list. The shoe in the database
    that matches the max quatity, will then returned with a neatly
    formatted message

    Args:
        product_list(list): a list of all the shoes in the database

    Returns:
        A neatly formatted string
    """
    # Use list comprehension to get the quantity as an integer
    quantity_list = [int(shoe['quantity'].strip()) for shoe in product_list]
    # Apply max function to return max value from a list
    maximum_quantity = max(quantity_list)
    for shoe in product_list:
        if int(shoe["quantity"].strip()) == maximum_quantity:
            print(f"\n{shoe['product'].strip()} are for sale!")
            break


def low_quantity(product, restock, product_list):
    """
    A function that is responsible for changing the stock quantity of a
    a shoe, that has been provided because of its low stock

    Args:
        product(str): A product that needs to be restocked
        restock(int): An int value of how many units we are looking to
        restock with
        product_list(list): a list of all the products in the database
    """
    for dct in product_list:
        # If the 'item' is the value of one of
        # one of the dct items, return the dct
        # in a list
        if dct["product"] == product:
            # Update the quantity key of the dct
            # with the same value as "item" for
            # product key, by converting values to
            # integers, and aggregating
            dct["quantity"] = int(dct.get("quantity")) + int(restock)
            dct["quantity"] = str(dct["quantity"]) + "\n"
            print(f"{product} order has", end=" ")
            print("been placed successfuly!\n")


def re_stock(product_list):
    """
    A functon that is responsible for making a list of all the
    "quantity" keys' values from each dictionary in the list of
    dictionaries provided. The minimum value of that list is then used
    to find the items with the same minimum value for quantity, and
    adds these product names into a list.
    For each product name in that list, an option to restock that
    product is requested to user.

    Args:
        product_list(list): List of all the Shoe objects

    """
    # Use list comprehension to convert the quantity values in each
    # dictionary in the list into an integer and remove any whitespace
    quantity_list = [int(dct['quantity'].strip()) for dct in product_list]
    minimum_quantity = min(quantity_list)
    items_to_restock = []
    for dct in product_list:
        # Store the name of the products with their quantity value
        # being the minimum value in the "quantity_list"
        if int(dct["quantity"].strip()) == minimum_quantity:
            items_to_restock.append(dct["product"])

    print("\nThe total number of shoes needing to be restocked:", end=" ")
    print(f"{len(items_to_restock)}")
    for item in items_to_restock:
        # loop through each element in the list of items whose quantity
        # value is the minimum value amongst all the dictionaries in
        # the shoe_list
        print(f"Current inventory total for {item} is {minimum_quantity}")

    for item in items_to_restock:
        while True:
            print("\nWould you like to restock on")
            # Strip any whitespace and ensure user input is in
            # lowercase
            restock_request = input(f"{item}?(y/n): ").strip().lower()
            if restock_request == "y":
                while True:
                    print(f"Current inventory is {minimum_quantity}.", end=" ")
                    print("Please provide restock order quantity", end=" ")
                    restock_value = input("as an integer: ")
                    # Ensure that the restock input is a digit
                    if not restock_value.isdigit():
                        print("Please ensure restock order", end=" ")
                        print("quantity is a digit")
                    else:
                        low_quantity(item, restock_value, product_list)
                        content = file_read("inventory.txt")
                        # Slice the header of the .txt file
                        header_list = content[:1]
                        # Cast list to string value
                        header_string = "".join(header_list)
                        # Overwrite the .txt file
                        write_file("inventory.txt", "w+", header_string)
                        for dct in product_list:
                            # To avoid adding a new blank line after
                            # restocking an item, remove the newline
                            # character when appending product
                            if dct.get("product") == item:
                                product = ", ".join(list(dct.values()))
                                write_file("inventory.txt", "a+", f"{product}")
                            # For every other product, add newline
                            # character
                            else:
                                product = ", ".join(list(dct.values()))
                                write_file(
                                    "inventory.txt", "a+", f"{product}\n"
                                )
                        break
            elif restock_request == "n":
                print("Be careful not to run out of stock!")
            else:
                print("Ooops, thats not right, lets try again.\n")
            break


shoes_list = []

object_creation("inventory.txt", shoes_list)
choice = "x"
while True:
    choice = menu()
    if choice == "a":
        while True:
            new_shoe_str = capture_shoe()
            print("\nYou have provided the following shoe details:", end=" ")
            print(f"{new_shoe_str}")
            request_input = input("\nIs this correct?(y/n): ").strip().lower()
            if request_input == "y":
                new_shoe_list = new_shoe_str.split(", ")
                new_shoe_dct = Shoe(*new_shoe_list).shoe_dict()
                shoes_list.append(new_shoe_dct)
                break
            else:
                print("q - to quit")
                print("b - to re-input information", end="")
                quit = input(": ").strip().lower()
                if quit == "q":
                    break
                if quit == "b":
                    continue
    elif choice == "v":
        print()
        view_all(shoes_list)
    elif choice == "r":
        re_stock(shoes_list)
    elif choice == "s":
        search(shoes_list)
    elif choice == "vi":
        value_per_item(shoes_list)
    elif choice == "dsc":
        shoe_for_sale(shoes_list)
    elif choice == "q":
        print("\nGoodbye!")
        break
    else:
        print("\nPlease provide a valid option from the menu!")

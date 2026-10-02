"""
=============================================================================
TITLE: Online Shopping Cart Simulation
COLLEGE MINOR PROJECT - PYTHON PROGRAMMING
=============================================================================
This program simulates a complete menu-driven console online shopping cart
demonstrating the following required 11 core Python concepts:
  1. Dictionary        -> Product catalog with name and prices
  2. Tuple             -> Cart order items stored as (item_name, quantity)
  3. Set               -> Unique product categories
  4. Frozen Set        -> Immutable coupon codes (SAVE10, SAVE20, WELCOME)
  5. Function Aliasing -> Reassigning checkout function to another variable
  6. Lambda + Map      -> Applying discounts and computing subtotals
  7. Filter            -> Filtering products above user-specified price
  8. Reduce            -> Calculating total bill with functools.reduce
  9. Recursive Function-> Displaying cart items recursively
  10. Decorator        -> Logging cart operations (add, remove)
  11. Decorator Chaining -> Validating cart emptiness + logging on checkout
=============================================================================
"""

from functools import reduce
import time

# =============================================================================
# CONCEPT 1: DICTIONARY
# Storing product names (keys) and prices in INR (values)
# =============================================================================
products = {
    "Laptop": 50000,
    "Smartphone": 20000,
    "Headphones": 2500,
    "Mouse": 500,
    "Keyboard": 1200,
    "Smart Watch": 3500,
    "Backpack": 1500,
    "USB Cable": 200,
    "Power Bank": 1800,
    "Monitor": 12000
}

# Product to category mapping
product_category_map = {
    "Laptop": "Electronics",
    "Smartphone": "Electronics",
    "Headphones": "Accessories",
    "Mouse": "Peripherals",
    "Keyboard": "Peripherals",
    "Smart Watch": "Wearables",
    "Backpack": "Accessories",
    "USB Cable": "Accessories",
    "Power Bank": "Accessories",
    "Monitor": "Electronics"
}

# =============================================================================
# CONCEPT 3: SET
# Storing unique product categories using set() to eliminate duplicates
# =============================================================================
product_categories = set(product_category_map.values())

# =============================================================================
# CONCEPT 4: FROZEN SET
# Immutable set to store valid coupon codes so they cannot be altered at runtime
# =============================================================================
VALID_COUPONS = frozenset({"SAVE10", "SAVE20", "WELCOME"})

# Coupon discount percentages
COUPON_DISCOUNTS = {
    "SAVE10": 10,     # 10% off
    "SAVE20": 20,     # 20% off
    "WELCOME": 15     # 15% off
}

# =============================================================================
# CONCEPT 2: TUPLE
# Cart is maintained as a list of tuples: [(product_name, quantity), ...]
# Each item is stored as an immutable pair (item_name, quantity)
# =============================================================================
cart = []
applied_coupon = None
discount_percent = 0


# =============================================================================
# CONCEPT 10: DECORATOR
# A decorator function to log cart operations (add, remove, etc.)
# =============================================================================
def log_cart_action(func):
    """Logs the entry and successful completion of a cart operation."""
    def wrapper(*args, **kwargs):
        action_name = func.__name__.replace("_", " ").title()
        print(f"\n[SYSTEM LOG] Starting operation: '{action_name}'...")
        result = func(*args, **kwargs)
        print(f"[SYSTEM LOG] Operation '{action_name}' finished.")
        return result
    return wrapper


def verify_cart_not_empty(func):
    """Validator decorator: Checks if the cart contains any items before proceeding."""
    def wrapper(cart_items, *args, **kwargs):
        if not cart_items:
            print("\n" + "=" * 50)
            print("[VALIDATION ERROR] Cannot proceed! Cart is completely EMPTY.")
            print("Please add at least one product before performing this action.")
            print("=" * 50)
            return False
        return func(cart_items, *args, **kwargs)
    return wrapper


# -----------------------------------------------------------------------------
# HELPER DISPLAY FUNCTIONS
# -----------------------------------------------------------------------------
def display_header():
    print("\n" + "=" * 50)
    print("           ONLINE SHOPPING CART SIMULATION          ")
    print("=" * 50)


def display_categories():
    print(f"\nAvailable Categories ({len(product_categories)}):", end=" ")
    # CONCEPT 3: Set iteration
    print(", ".join(sorted(product_categories)))


def view_products():
    """Displays all available products from the dictionary."""
    display_header()
    display_categories()
    print("\n----------------- PRODUCT CATALOG -----------------")
    print(f"{'S.No.':<6}{'Product Name':<20}{'Category':<15}{'Price (Rs.)':<10}")
    print("-" * 51)
    
    # CONCEPT 1: Accessing Dictionary keys and values
    for index, (item, price) in enumerate(products.items(), start=1):
        cat = product_category_map.get(item, "General")
        print(f"{index:<6}{item:<20}{cat:<15}Rs. {price:<10}")
    print("-" * 51)


# =============================================================================
# CONCEPT 9: RECURSIVE FUNCTION
# Recursively displays all items in the cart without a regular for-loop
# =============================================================================
def display_cart_recursive(cart_items, index=0):
    """
    CONCEPT 9: Recursive function to print cart items one-by-one.
    Base case: When index reaches the length of cart_items, stop.
    Recursive step: Print current item, then call function for index + 1.
    """
    if index >= len(cart_items):
        return  # Base condition
    
    # CONCEPT 2: Tuple unpacking
    item_name, qty = cart_items[index]
    unit_price = products[item_name]
    subtotal = unit_price * qty
    print(f"{index + 1:<6}{item_name:<20}{qty:<10}Rs. {unit_price:<12}Rs. {subtotal:<10}")
    
    # Recursive Call
    display_cart_recursive(cart_items, index + 1)


def view_cart(cart_items):
    """Displays current items present in the cart."""
    display_header()
    print("\n------------------- YOUR CART ---------------------")
    if not cart_items:
        print("Your cart is currently empty.")
        print("-" * 51)
        return

    print(f"{'S.No.':<6}{'Product Name':<20}{'Quantity':<10}{'Unit Price':<12}{'Subtotal':<10}")
    print("-" * 60)
    
    # Calling recursive function to display cart contents
    display_cart_recursive(cart_items, 0)
    print("-" * 60)
    
    # Calculate and show current subtotal using reduce
    subtotal = calculate_cart_total(cart_items)
    print(f"Current Cart Subtotal: Rs. {subtotal:.2f}")
    if applied_coupon:
        print(f"Applied Coupon       : {applied_coupon} ({discount_percent}% OFF)")
    print("-" * 60)


# =============================================================================
# CONCEPT 10: DECORATED CART OPERATIONS
# =============================================================================
@log_cart_action
def add_to_cart(cart_items, product_name, quantity):
    """
    Adds a product to the cart.
    CONCEPT 2: Stores items as tuples (product_name, quantity).
    """
    for i, (item, qty) in enumerate(cart_items):
        if item.lower() == product_name.lower():
            new_qty = qty + quantity
            cart_items[i] = (item, new_qty)  # Updating with new Tuple
            print(f"[SUCCESS] Updated '{item}' quantity in cart to {new_qty}.")
            return True
    
    for item in products:
        if item.lower() == product_name.lower():
            cart_items.append((item, quantity))  # CONCEPT 2: Appending (item, qty) Tuple
            print(f"[SUCCESS] Added {quantity}x '{item}' to your cart.")
            return True

    print(f"[ERROR] Product '{product_name}' not found in catalog!")
    return False


@log_cart_action
def remove_from_cart(cart_items, product_name):
    """Removes a product completely from the cart."""
    for i, (item, qty) in enumerate(cart_items):
        if item.lower() == product_name.lower():
            removed_tuple = cart_items.pop(i)  # CONCEPT 2: Tuple removed
            print(f"[SUCCESS] Removed '{removed_tuple[0]}' from your cart.")
            return True
    print(f"[ERROR] '{product_name}' is not in your cart!")
    return False


def change_quantity(cart_items, product_name, new_quantity):
    """Updates the quantity of a product in the cart."""
    if new_quantity <= 0:
        print("[INFO] Quantity is 0 or less. Removing product from cart...")
        return remove_from_cart(cart_items, product_name)

    for i, (item, qty) in enumerate(cart_items):
        if item.lower() == product_name.lower():
            cart_items[i] = (item, new_quantity)  # CONCEPT 2: Stored as Tuple
            print(f"[SUCCESS] Quantity for '{item}' updated to {new_quantity}.")
            return True
            
    print(f"[ERROR] Product '{product_name}' was not found in your cart.")
    return False


# =============================================================================
# CONCEPT 7: FILTER
# Uses filter() and a lambda function to find products whose price > threshold
# =============================================================================
def search_products_above_price(min_price):
    """
    CONCEPT 7: FILTER
    Uses filter() with a lambda expression to extract products above min_price.
    """
    print(f"\nFiltering products with price strictly greater than Rs. {min_price:.2f}...")
    filtered_items = list(filter(lambda item_pair: item_pair[1] > min_price, products.items()))
    
    print("\n---------------- FILTERED PRODUCTS ----------------")
    if not filtered_items:
        print(f"No products found with price > Rs. {min_price}")
    else:
        print(f"{'Product Name':<25}{'Price (Rs.)':<10}")
        print("-" * 35)
        for name, price in filtered_items:
            print(f"{name:<25}Rs. {price:<10}")
    print("-" * 35)


# =============================================================================
# CONCEPT 4: FROZEN SET USAGE
# Checking membership against an immutable frozenset
# =============================================================================
def apply_coupon_code(coupon_input):
    """
    CONCEPT 4: FROZEN SET
    Validates coupon code against immutable VALID_COUPONS frozenset.
    """
    code = coupon_input.strip().upper()
    if code in VALID_COUPONS:
        discount = COUPON_DISCOUNTS.get(code, 0)
        print(f"\n[COUPON APPLIED] Success! Coupon '{code}' activated.")
        print(f"You unlocked a flat {discount}% DISCOUNT on your order!")
        return code, discount
    else:
        print(f"\n[INVALID COUPON] '{code}' is not valid.")
        print(f"Valid fixed coupons are: {', '.join(sorted(VALID_COUPONS))}")
        return None, 0


# =============================================================================
# CONCEPT 8: REDUCE
# Uses functools.reduce to compute cumulative sum of all cart item totals
# =============================================================================
def calculate_cart_total(cart_items):
    """
    CONCEPT 8: REDUCE
    Calculates the total price of items in the cart using functools.reduce().
    """
    if not cart_items:
        return 0.0
    
    total = reduce(
        lambda acc, item_tuple: acc + (products[item_tuple[0]] * item_tuple[1]),
        cart_items,
        0.0
    )
    return total


# =============================================================================
# CONCEPT 6: LAMBDA + MAP
# Uses map() and lambda to calculate item subtotals and discounted prices
# =============================================================================
def calculate_bill_breakdown(cart_items, discount_pct=0):
    """
    CONCEPT 6: LAMBDA + MAP
    1. Uses map() with lambda to compute item-wise subtotals.
    2. Uses map() with lambda to calculate discounted price of each product.
    """
    display_header()
    print("\n------------------ BILL CALCULATION ------------------")
    if not cart_items:
        print("Your cart is empty. Total Bill: Rs. 0.00")
        return 0.0, 0.0, 0.0

    # 1. Map each tuple to its subtotal: (item, qty) -> price * qty
    subtotals = list(map(lambda item: products[item[0]] * item[1], cart_items))
    
    # 2. Map each tuple to its discounted unit price
    discount_factor = (100 - discount_pct) / 100.0
    discounted_unit_prices = list(
        map(lambda item: (item[0], round(products[item[0]] * discount_factor, 2)), cart_items)
    )

    print(f"{'Product':<18}{'Qty':<6}{'Original Unit':<15}{'Discounted Unit':<18}{'Subtotal'}")
    print("-" * 72)
    for (item, qty), (_, disc_price), sub in zip(cart_items, discounted_unit_prices, subtotals):
        orig_price = products[item]
        print(f"{item:<18}{qty:<6}Rs. {orig_price:<11}Rs. {disc_price:<14}Rs. {sub:.2f}")
    print("-" * 72)

    # CONCEPT 8: Total bill using reduce
    gross_total = reduce(lambda a, b: a + b, subtotals, 0.0)
    discount_amount = gross_total * (discount_pct / 100.0)
    net_payable = gross_total - discount_amount

    print(f"Gross Cart Subtotal    : Rs. {gross_total:.2f}")
    if discount_pct > 0:
        print(f"Discount Applied ({discount_pct}%) : -Rs. {discount_amount:.2f}")
    print(f"Final Net Payable Bill : Rs. {net_payable:.2f}")
    print("-" * 72)
    
    return gross_total, discount_amount, net_payable


# =============================================================================
# CONCEPT 11: DECORATOR CHAINING
# Multiple decorators applied to the checkout function:
#   1st: @verify_cart_not_empty (outer gatekeeper)
#   2nd: @log_cart_action (logs execution)
# Execution order: verify_cart_not_empty -> log_cart_action -> checkout
# =============================================================================
@verify_cart_not_empty
@log_cart_action
def checkout(cart_items, discount_pct=0, coupon_name=None):
    """
    Processes final checkout and prints order confirmation.
    Protected by 2 chained decorators.
    """
    gross, discount, net = calculate_bill_breakdown(cart_items, discount_pct)
    
    print("\n================== ORDER CONFIRMATION ==================")
    print("STATUS         : SUCCESS (Order Placed)")
    print(f"ORDER TIMESTAMP: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"ITEMS COUNT    : {sum(qty for _, qty in cart_items)} items")
    if coupon_name:
        print(f"COUPON USED    : {coupon_name} (Flat {discount_pct}% Discount)")
    print(f"TOTAL PAID     : Rs. {net:.2f}")
    print("========================================================")
    print("Thank you for shopping with us! Your order will be delivered soon.")
    print("========================================================\n")
    
    # Clear the cart after successful order
    cart_items.clear()
    return True


# =============================================================================
# CONCEPT 5: FUNCTION ALIASING
# Assigning the checkout function object to another variable name.
# In Python, functions are first-class objects!
# =============================================================================
process_payment_and_checkout = checkout  # CONCEPT 5: Function alias created!


# =============================================================================
# MAIN INTERACTIVE MENU LOOP
# =============================================================================
def main():
    global applied_coupon, discount_percent
    
    while True:
        display_header()
        print("1.  View Products Catalog")
        print("2.  Add Product to Cart")
        print("3.  Remove Product from Cart")
        print("4.  View Cart")
        print("5.  Change Product Quantity")
        print("6.  Search Products Above Price")
        print("7.  Apply Discount Coupon")
        print("8.  Calculate Total Bill")
        print("9.  Checkout (Places Order)")
        print("10. Exit Application")
        print("=" * 50)
        
        choice = input("Enter your choice (1-10): ").strip()
        
        if choice == "1":
            view_products()
            input("\nPress Enter to return to menu...")

        elif choice == "2":
            view_products()
            prod_name = input("\nEnter product name to add: ").strip()
            
            matched = None
            for p in products:
                if p.lower() == prod_name.lower():
                    matched = p
                    break
            
            if not matched:
                print(f"[ERROR] '{prod_name}' does not exist in our catalog!")
            else:
                try:
                    qty = int(input(f"Enter quantity for '{matched}': "))
                    if qty <= 0:
                        print("[ERROR] Quantity must be greater than zero!")
                    else:
                        add_to_cart(cart, matched, qty)
                except ValueError:
                    print("[ERROR] Invalid input! Quantity must be an integer.")
            input("\nPress Enter to return to menu...")

        elif choice == "3":
            if not cart:
                print("\n[INFO] Your cart is already empty.")
            else:
                view_cart(cart)
                prod_name = input("\nEnter product name to remove: ").strip()
                remove_from_cart(cart, prod_name)
            input("\nPress Enter to return to menu...")

        elif choice == "4":
            view_cart(cart)
            input("\nPress Enter to return to menu...")

        elif choice == "5":
            if not cart:
                print("\n[INFO] Your cart is empty.")
            else:
                view_cart(cart)
                prod_name = input("\nEnter product name to update: ").strip()
                try:
                    new_qty = int(input(f"Enter new quantity for '{prod_name}' (0 to remove): "))
                    change_quantity(cart, prod_name, new_qty)
                except ValueError:
                    print("[ERROR] Invalid quantity! Please enter an integer.")
            input("\nPress Enter to return to menu...")

        elif choice == "6":
            try:
                threshold = float(input("\nEnter minimum price threshold (Rs.): "))
                search_products_above_price(threshold)
            except ValueError:
                print("[ERROR] Please enter a valid numeric price.")
            input("\nPress Enter to return to menu...")

        elif choice == "7":
            print("\nAvailable promotional coupons: SAVE10 (10%), SAVE20 (20%), WELCOME (15%)")
            code_input = input("Enter coupon code: ")
            code, disc = apply_coupon_code(code_input)
            if code:
                applied_coupon = code
                discount_percent = disc
            input("\nPress Enter to return to menu...")

        elif choice == "8":
            calculate_bill_breakdown(cart, discount_percent)
            input("\nPress Enter to return to menu...")

        elif choice == "9":
            print("\n" + "=" * 50)
            print("[DEMO] Demonstrating CONCEPT 5: FUNCTION ALIASING")
            print("Invoking 'process_payment_and_checkout()' which is an alias of 'checkout()'")
            print("=" * 50)
            
            success = process_payment_and_checkout(cart, discount_percent, applied_coupon)
            if success:
                applied_coupon = None
                discount_percent = 0
            input("\nPress Enter to return to menu...")

        elif choice == "10":
            print("\nThank you for using Online Shopping Cart Simulator!")
            print("Exiting project. Have a great day!\n")
            break

        else:
            print("[ERROR] Invalid selection! Please enter a number between 1 and 10.")
            input("\nPress Enter to try again...")


if __name__ == "__main__":
    main()

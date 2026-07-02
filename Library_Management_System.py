import csv
import os
from datetime import datetime

# ==========================
# Global Constants 
# ==========================
MANAGER_PIN = 2503

BOOKS_FILE = "books.csv"
USERS_FILE = "users.csv"
HISTORY_FILE = "history.csv"

# Unicode Border Characters
TL, TR, BL, BR, H, V, TR_SPLIT, TL_SPLIT = "╔", "╗", "╚", "╝", "═", "║", "╠", "╣"


# ==========================
# Database Initializer 
# ==========================
def initialize_database():
    """Creates files with appropriate field headers if they don't exist yet."""
    if not os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Book_ID", "Title", "Author", "Quantity"])
            
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["User_ID", "Name"])
            
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "User_ID", "Action", "Book_ID"])


# ==========================
# UI Border Helper Functions
# ==========================
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_box(text, width=54):
    print(TL + H * (width - 2) + TR)
    print(V + text.center(width - 2) + V)
    print(BL + H * (width - 2) + BR)

def draw_menu(title, options, width=54):
    print(TL + H * (width - 2) + TR)
    print(V + title.center(width - 2) + V)
    print(TR_SPLIT + H * (width - 2) + TL_SPLIT)
    for option in options:
        print(V + f"  {option}".ljust(width - 2) + V)
    print(BL + H * (width - 2) + BR)


# ==========================
# Manager Functions
# ==========================

def manager_login():
    pin=int(input("Enter the PIN to login = "))

    if pin == MANAGER_PIN:
        manager_menu()
    else:
        print("Invalid PIN..!!")


def manager_menu():
    print("This is manager menu (trail)")

def add_user():
    pass

def remove_user():
    pass

def view_users():
    pass

def add_book():
    pass

def remove_book():
    pass

def view_books():
    pass

def search_book():
    pass

def view_transaction_history():
    pass


# ==========================
# User Functions
# ==========================

def user_login():
    pass

def user_menu():
    pass

def view_available_books():
    pass

def issue_book():
    pass

def return_book():
    pass

def view_my_history():
    pass

def border():
    print("---------------------------------------------")

# ==========================
# Main Function
# ==========================

def main():
    
    while True:

        border()
        print("1.Library Manager")
        print("2.User")
        print("3.Exit")
        border()

        choice=int(input("Enter you choice: "))
        border()

        if choice == 1:
            manager_login()

        elif choice == 2:
            border()
            user_login()

        elif choice == 3:
            print("Thank you for using the Library management system.")
            border()
            break
        
        else:
            border()
            print("Invalid Choice..!!")

# ==========================
# Program Entry Point
# ==========================

if __name__ == "__main__":
    main()
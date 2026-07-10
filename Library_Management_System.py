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
    clear_screen()
    draw_box("MANAGER AUTHENTICATION")
    try:
        pin = int(input("Enter the PIN to login: "))
        if pin == MANAGER_PIN:
            manager_menu()
        else:
             print("\n❌ Invalid PIN..!!")
             input("\nPress Enter to return...")

    except ValueError:
        print("\n⚠️ Numbers only! Invalid input.")
        input("\nPress Enter to return...")

def manager_menu():
    while True:
        clear_screen()
        options = [
            "1. Add User", "2. Remove User", "3. View All Users",
            "4. Add Book", "5. Remove Book", "6. View All Books",
            "7. Search Book", "8. View Transaction History", "9. Logout"
        ]
        draw_menu("MANAGER CONTROL DASHBOARD", options)
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1: add_user()
            elif choice == 2: remove_user()
            elif choice == 3: view_users()
            elif choice == 4: add_book()
            elif choice == 5: remove_book()
            elif choice == 6: view_books()
            elif choice == 7: search_book()
            elif choice == 8: view_transaction_history()
            elif choice == 9: break
            else:
                print("❌ Invalid Choice..!!")
                input("Press Enter to retry...")
        except ValueError:
            print("⚠️ Numbers only! Invalid input.")
            input("Press Enter to retry...")

def add_user():
    clear_screen()
    draw_box("ADD NEW USER")
    uid = input("Enter unique User ID: ").strip().upper()
    
    # To Check if user already exists
    with open(USERS_FILE, mode='r', encoding='utf-8') as f:
        if any(row[0] == uid for row in csv.reader(f)):
            draw_box("⚠️ USER ID ALREADY EXISTS..!!")
            input("\nPress Enter to return...")
            return
        
    name = input("Enter User Name: ").strip()
    if uid and name:
        with open(USERS_FILE, mode='a', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow([uid, name])
        print("✅ User registered successfully!")
    else:
        draw_box("⚠️ User Name cannot be empty..!!")
    input("\nPress Enter to return...")

def remove_user():
    clear_screen()
    draw_box("REMOVE USER REGISTRATION")
    uid = input("Enter User ID to delete: ").strip()
    updated_rows = []
    found = False
    
    with open(USERS_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        updated_rows.append(headers)
        for row in reader:
            if row[0] == uid:
                found = True
            else:
                updated_rows.append(row)
                
    if found:
        with open(USERS_FILE, mode='w', newline='', encoding='utf-8') as f:
            csv.writer(f).writerows(updated_rows)
        print("✅ User removed successfully!")
    else:
        print("❌ User ID not found.")
    input("\nPress Enter to return...")

def view_users():
    clear_screen()
    draw_box("REGISTERED SYSTEM USERS")
    with open(USERS_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader) 
        print(f"{'User ID':<15} | {'User Name':<30}")
        print("-" * 48)
        count = 0
        for row in reader:
            print(f"{row[0]:<15} | {row[1]:<30}")
            count += 1
    if count == 0:
        print("No users registered yet.")
    input("\nPress Enter to return...")

def add_book():
    clear_screen()
    draw_box("ADD BOOK TO INVENTORY")
    bid = input("Enter Book ID (ISBN/Serial): ").strip().upper()
    
    rows = []
    found = False
    with open(BOOKS_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows.append(headers)
        for row in reader:
            if row[0] == bid:
                found = True
                try:
                    qty = int(input(f"Book exists. Current stock: {row[4]}. Add how many? "))
                    row[4] = str(int(row[4]) + qty)
                except ValueError:
                    print("⚠️ Invalid number. Aborting stock addition.")
                    input("\nPress Enter to return...")
                    return
            rows.append(row)
            
    if found:
        with open(BOOKS_FILE, mode='w', newline='', encoding='utf-8') as f:
            csv.writer(f).writerows(rows)
        print("✅ Stock updated successfully!")
    else:
        title = input("Enter Book Title: ").strip()
        author = input("Enter Author Name: ").strip()
        year = int(input("Enter Publication Year: "))
        try:
            qty = int(input("Enter Quantity: "))
            if bid and title and author and year and qty >= 0:
                with open(BOOKS_FILE, mode='a', newline='', encoding='utf-8') as f:
                    csv.writer(f).writerow([bid, title, author, year, qty])
                print("✅ New book indexed successfully!")
            else:
                print("⚠️ Invalid fields.")
        except ValueError:
            print("⚠️ Invalid quantity number.")
    input("\nPress Enter to return...")

def remove_book():
    clear_screen()
    draw_box("REMOVE BOOK INDEX")
    bid = input("Enter Book ID to delete completely: ").strip().upper()
    updated_rows = []
    found = False
    
    with open(BOOKS_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        updated_rows.append(headers)
        for row in reader:
            if row[0] == bid:
                found = True
            else:
                updated_rows.append(row)
                
    if found:
        with open(BOOKS_FILE, mode='w', newline='', encoding='utf-8') as f:
            csv.writer(f).writerows(updated_rows)
        print("✅ Book removed Successfully! ")
    else:
        print("❌ Book ID not found.")
    input("\nPress Enter to return...")

def view_books():
    clear_screen()
    draw_box("LIBRARY CATALOG")
    with open(BOOKS_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        print(f"{'Book id':<12} | {'Title':<25} | {'Author':<20} | {'Year':<6} | {'Qty':<5}")
        print("-" * 88)
        count = 0
        for row in reader:
            print(f"{row[0]:<12} | {row[1]:<25}|{row[2]:<20}|{row[3]:<6}|{row[4]:<5}")
            count += 1
        draw_box(f"TOTAL BOOKS : {count}")

    if count == 0:
        print("NO BOOKS AVALIABLE")
    input("\nPress Enter to return...")

def search_book():
    clear_screen()
    draw_box("SEARCH BOOK")

    query = input("Enter Book ID, Title or Author: ").strip().lower()

    with open(BOOKS_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)

        print(f"{'Book ID':<12} | {'Title':<25} | {'Author':<20} | {'Year':<6} | {'Qty':<5}")
        print("-" * 88)

        found = False
        count = 0

        for row in reader:
            if (query in row[0].lower() or query in row[1].lower()  or query in row[2].lower()):
                print(f"{'Book ID':<12} | {'Title':<25} | {'Author':<20} | {'Year':<6} | {'Qty':<5}")
                found = True
                count += 1

        if not found:
            draw_box("BOOK NOT FOUND")
        else:
            print("-" * 88)
            print(f"Search Results : {count}")

    input("\nPress Enter to return...")

    
def view_transaction_history():
    clear_screen()
    draw_box("TRANSACTION HISTORY")

    with open(HISTORY_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)

        print(f"{'Trans ID':<10} | {'User ID':<10} | {'Book ID':<12} | {'Issue Date':<12} | {'Return Date':<12} | {'Status':<10}")
        print("-" * 85)

        count = 0

        for row in reader:
            print(
                f"{row[0]:<10} | "
                f"{row[1]:<10} | "
                f"{row[2]:<12} | "
                f"{row[3]:<12} | "
                f"{row[4]:<12} | "
                f"{row[5]:<10}"
            )
            count += 1

    if count == 0:
        draw_box("NO TRANSACTION HISTORY FOUND")
    else:
        print("-" * 85)
        print(f"Total Transactions : {count}")

    input("\nPress Enter to return...")


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


# ==========================
# Main Function
# ==========================

def main():
    
    while True:

        
        print("1.Library Manager")
        print("2.User")
        print("3.Exit")

        choice=int(input("Enter you choice: "))
        

        if choice == 1:
            manager_login()

        elif choice == 2:
            user_login()

        elif choice == 3:
            print("Thank you for using the Library management system.")
            break
        
        else:
            print("Invalid Choice..!!")

# ==========================
# Program Entry Point
# ==========================

if __name__ == "__main__":
    main()
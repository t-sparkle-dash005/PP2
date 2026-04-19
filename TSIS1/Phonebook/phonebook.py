import psycopg2
import csv
from config import load_config


def phonebook():
    commands = (
        """
        CREATE TABLE IF NOT EXISTS contacts (
            id         SERIAL PRIMARY KEY,
            username   VARCHAR(50)  UNIQUE NOT NULL,
            first_name VARCHAR(255) NOT NULL,
            phone      VARCHAR(20)  NOT NULL
        );
        """,
    )
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                for command in commands:
                    cur.execute(command)
            conn.commit()
        print('Table "contacts" created successfully')
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def import_from_csv(filepath: str):

    sql = """
        INSERT INTO contacts (username, first_name, phone)
        VALUES (%s, %s, %s)
        ON CONFLICT (username) DO NOTHING;
    """
    inserted = 0
    skipped  = 0

    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open(filepath, newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        cur.execute(sql, (
                            row['username'],
                            row['first_name'],
                            row['phone']
                        ))
                        if cur.rowcount == 1:
                            inserted += 1
                        else:
                            skipped += 1
            conn.commit()
        print(f"Import done: row {inserted} inserted, {skipped} skipped")
    except FileNotFoundError:
        print(f"File '{filepath}' not found")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def insert_contact(username: str, first_name: str, phone: str):
    sql = """
        INSERT INTO contacts (username, first_name, phone)
        VALUES (%s, %s, %s)
        RETURNING id;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (username, first_name, phone))
                new_id = cur.fetchone()[0]
            conn.commit()
        print(f"Contact saved: id={new_id}, username='{username}'")
    except psycopg2.errors.UniqueViolation:
        print(f"Username '{username}' already exists")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def prompt_and_insert():
    print("\n------>> Add New Contact <<------")
    username   = input("Username   : ").strip()
    first_name = input("First name : ").strip()
    phone      = input("Phone      : ").strip()

    if not username:
        print("Username can't be empty")
        return
    if not first_name:
        print("First name can't be empty")
        return
    if not phone:
        print("Phone can't be empty")
        return

    insert_contact(username, first_name, phone)


def update_first_name(username: str, new_name: str):
    sql = "UPDATE contacts SET first_name = %s WHERE username = %s;"
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (new_name, username))
                rows = cur.rowcount
            conn.commit()

        if rows == 0:
            print(f"No contact found with username '{username}'")
        else:
            print(f"First name updated to '{new_name}' for '{username}'")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def update_phone(username: str, new_phone: str):
    sql = "UPDATE contacts SET phone = %s WHERE username = %s;"
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (new_phone, username))
                rows = cur.rowcount
            conn.commit()

        if rows == 0:
            print(f"No contact found with username '{username}'")
        else:
            print(f"Phone updated to '{new_phone}' for '{username}'")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def prompt_and_update():
    print("\n------>> Update Contact <<------")
    username = input("Enter username to update: ").strip()

    print("Update options:")
    print("  1 - First name")
    print("  2 - Phone number")
    choice = input("Choice: ").strip()

    if choice == "1":
        new_name = input("New first name: ").strip()
        if not new_name:
            print("First name can't empty")
            return
        update_first_name(username, new_name)

    elif choice == "2":
        new_phone = input("New phone: ").strip()
        if not new_phone:
            print("Phone must not be empty.")
            return
        update_phone(username, new_phone)

    else:
        print("Invalid")



def print_results(rows: list):

    if not rows:
        print("  (no results found)")
        return
    print(f"\n  {'ID':<5} {'Username':<15} {'First Name':<25} {'Phone':<15}")
    print("  " + "-" * 62)
    for row in rows:
        print(f"  {row[0]:<5} {row[1]:<15} {row[2]:<25} {row[3]:<15}")
    print(f"\n  {len(rows)} record_s found")


def search_by_name(name: str):
    sql = """
        SELECT id, username, first_name, phone
        FROM contacts
        WHERE first_name ILIKE %s
        ORDER BY first_name;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (f"%{name}%",))
                rows = cur.fetchall()
        print(f"\n------>> Results for name containing '{name}' <<------")
        print_results(rows)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def search_by_username(username: str):
    sql = """
        SELECT id, username, first_name, phone
        FROM contacts
        WHERE username = %s;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (username,))
                rows = cur.fetchall()
        print(f"\n------>> Results for username '{username}' <<------")
        print_results(rows)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def search_by_phone_prefix(prefix: str):
    sql = """
        SELECT id, username, first_name, phone
        FROM contacts
        WHERE phone LIKE %s
        ORDER BY phone;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (f"{prefix}%",))
                rows = cur.fetchall()
        print(f"\n------>> Results with phone prefix '{prefix}' <<------")
        print_results(rows)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def get_all_contacts():
    sql = """
        SELECT id, username, first_name, phone
        FROM contacts
        ORDER BY id;
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchall()
        print("\n------>> All Contacts <<------")
        print_results(rows)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def prompt_and_search():
    print("\n------>> Search Contacts <<------")
    print("  1 - Search by name")
    print("  2 - Search by username")
    print("  3 - Search by phone prefix")
    print("  4 - Show all contacts")
    choice = input("Choice: ").strip()

    if choice == "1":
        name = input("Enter name: ").strip()
        search_by_name(name)
    elif choice == "2":
        username = input("Enter username: ").strip()
        search_by_username(username)
    elif choice == "3":
        prefix = input("Enter phone prefix (e.g. +7701): ").strip()
        search_by_phone_prefix(prefix)
    elif choice == "4":
        get_all_contacts()
    else:
        print("Invalid")


def delete_by_username(username: str):
    sql = "DELETE FROM contacts WHERE username = %s;"
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (username,))
                rows = cur.rowcount
            conn.commit()

        if rows == 0:
            print(f"No contact found with this username: '{username}'")
        else:
            print(f"Contact '{username}' deleted")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def delete_by_phone(phone: str):
    sql = "DELETE FROM contacts WHERE phone = %s;"
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (phone,))
                rows = cur.rowcount
            conn.commit()

        if rows == 0:
            print(f"No contact found with phone '{phone}'")
        else:
            print(f"Contact with phone '{phone}' deleted ({rows} row_s removed)")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


def prompt_and_delete():
    print("\n------>> Delete Contact <<------")
    print("  1 - Delete by username")
    print("  2 - Delete by phone number")
    choice = input("Choice: ").strip()

    if choice == "1":
        username = input("Delete username: ").strip()
        confirm  = input(f"Are you sure? (y/n): ").strip()
        if confirm.lower() == "y":
            delete_by_username(username)
        else:
            print("Cancelled")

    elif choice == "2":
        phone   = input("Phone to delete: ").strip()
        confirm = input(f"Delete contact with phone '{phone}'? (y/n): ").strip()
        if confirm.lower() == "y":
            delete_by_phone(phone)
        else:
            print("Cancelled")

    else:
        print("Invalid")


def main():

    while True:
        print("\n Phonebook menu with PostgreSQL DB")
        print("_" * 40)
        print("  1 |  Import contacts from CSV")
        print("-" * 40)
        print("  2 |  Add a contact manually")
        print("-" * 40)
        print("  3 |  Update contacts' info")
        print("-" * 40)
        print("  4 |  Search, filter contacts")
        print("-" * 40)
        print("  5 |  Delete a contact")
        print("-" * 40)
        print("  0 |  Exit")
        print("=" * 40)

        choice = input("  Choice: ").strip()

        if choice == "1":
            import_from_csv("contacts.csv")
        elif choice == "2":
            prompt_and_insert()
        elif choice == "3":
            prompt_and_update()
        elif choice == "4":
            prompt_and_search()
        elif choice == "5":
            prompt_and_delete()
        elif choice == "0":
            print("Exiting app...")
            break
        else:
            print("Invalid, try again")


if __name__ == '__main__':
    main()
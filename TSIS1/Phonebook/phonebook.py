"""
New features over Practice 8:
  • Extended schema  (email, birthday, groups, phones table)
  • Filter contacts by group
  • Search by email (handled by the updated search_contacts() SQL function)
  • Sort results  (name / birthday / date added)
  • Paginated navigation  (next / prev / quit loop)
  • Export to JSON
  • Import from JSON  (skip or overwrite on duplicate)
  • CSV import extended to handle email, birthday, group, phone type
  • add_phone  (new stored procedure)
  • move_to_group  (new stored procedure)
"""

import csv
import json
import psycopg2
from datetime import date, datetime
from config import load_config


# ── helpers ──────────────────────────────────────────────────────────────────

def _conn():
    """Return a fresh psycopg2 connection."""
    return psycopg2.connect(**load_config())


def _print_contacts(rows: list, headers=None):
    if not rows:
        print("  (no results)")
        return
    if headers is None:
        headers = ["ID", "Username", "First Name", "Email", "Birthday", "Group"]
    widths = [max(len(str(headers[i])), max((len(str(r[i] or "")) for r in rows), default=0))
              for i in range(len(headers))]
    sep = "  " + "-" * (sum(widths) + 3 * len(widths))
    fmt = "  " + "  ".join(f"{{:<{w}}}" for w in widths)
    print()
    print(fmt.format(*headers))
    print(sep)
    for r in rows:
        print(fmt.format(*[str(v or "") for v in r]))
    print(f"\n  {len(rows)} record(s).")


def _print_phones(contact_id: int):
    """Print all phone numbers for a contact."""
    try:
        with _conn() as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT phone, type FROM phones WHERE contact_id = %s ORDER BY type;",
                (contact_id,)
            )
            rows = cur.fetchall()
        if rows:
            for phone, ptype in rows:
                print(f"      📞 {phone}  [{ptype}]")
        else:
            print("      (no phones)")
    except Exception as e:
        print(f"  Error fetching phones: {e}")


# ── setup ─────────────────────────────────────────────────────────────────────

def setup_database():
    """Run schema.sql then procedures.sql then functions.sql to initialise / migrate the DB."""
    for filename in ("schema.sql", "procedures.sql", "functions.sql"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                sql = f.read()
            with _conn() as conn, conn.cursor() as cur:
                cur.execute(sql)
            print(f"  ✓  Loaded {filename}")
        except FileNotFoundError:
            print(f"  ✗  '{filename}' not found – run from the TSIS1/ directory.")
        except Exception as e:
            print(f"  ✗  Error loading {filename}: {e}")


# ── 1. upsert (single contact) ────────────────────────────────────────────────

def upsert_contact(username: str, first_name: str, email: str = None,
                   birthday: date = None, group_id: int = None):
    try:
        with _conn() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO contacts (username, first_name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (username) DO UPDATE SET
                    first_name = EXCLUDED.first_name,
                    email      = COALESCE(EXCLUDED.email,    contacts.email),
                    birthday   = COALESCE(EXCLUDED.birthday, contacts.birthday),
                    group_id   = COALESCE(EXCLUDED.group_id, contacts.group_id)
            """,
                (username, first_name, email, birthday, group_id)
            )
        print(f"  ✓  Contact '{username}' saved.")
    except Exception as e:
        print(f"  Error: {e}")


def _get_groups() -> dict:
    """Return {name: id} mapping of all groups."""
    with _conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT name, id FROM groups ORDER BY name;")
        return {name: gid for name, gid in cur.fetchall()}


def prompt_and_upsert():
    print("\n──── Add / Update Contact ────")
    username   = input("  Username   : ").strip()
    first_name = input("  First name : ").strip()
    email      = input("  Email      : ").strip() or None
    bday_raw   = input("  Birthday   (YYYY-MM-DD, blank to skip): ").strip()
    birthday   = None
    if bday_raw:
        try:
            birthday = datetime.strptime(bday_raw, "%Y-%m-%d").date()
        except ValueError:
            print("  Invalid date – birthday skipped.")

    groups = _get_groups()
    print(f"  Groups: {', '.join(groups)}")
    gname    = input("  Group (blank to skip): ").strip()
    group_id = groups.get(gname)

    if not username or not first_name:
        print("  Username and first name are required.")
        return

    upsert_contact(username, first_name, email, birthday, group_id)

    # Ask if user wants to add a phone right away
    add_now = input("  Add a phone number now? (y/n): ").strip().lower()
    if add_now == "y":
        phone = input("  Phone : ").strip()
        ptype = input("  Type  (home/work/mobile) [mobile]: ").strip() or "mobile"
        _add_phone(username, phone, ptype)


# ── 2. add_phone ──────────────────────────────────────────────────────────────

def _add_phone(username: str, phone: str, ptype: str = "mobile"):
    try:
        with _conn() as conn, conn.cursor() as cur:
            cur.execute("CALL add_phone(%s::varchar, %s::varchar, %s::varchar);", (username, phone, ptype))
        print(f"  ✓  Phone added.")
    except Exception as e:
        print(f"  Error: {e}")


def prompt_and_add_phone():
    print("\n──── Add Phone Number ────")
    username = input("  Username : ").strip()
    phone    = input("  Phone    : ").strip()
    ptype    = input("  Type (home/work/mobile) [mobile]: ").strip() or "mobile"
    _add_phone(username, phone, ptype)


# ── 3. move_to_group ──────────────────────────────────────────────────────────

def _move_to_group(username: str, group_name: str):
    try:
        with _conn() as conn, conn.cursor() as cur:
            cur.execute("CALL move_to_group(%s::varchar, %s::varchar);", (username, group_name))
        print(f"  ✓  '{username}' moved to group '{group_name}'.")
    except Exception as e:
        print(f"  Error: {e}")


def prompt_and_move_group():
    print("\n──── Move Contact to Group ────")
    username   = input("  Username   : ").strip()
    group_name = input("  Group name : ").strip()
    _move_to_group(username, group_name)


# ── 4. bulk insert ────────────────────────────────────────────────────────────

def bulk_insert_contacts(entries: list[tuple]):
    """entries: [(username, first_name, phone, phone_type), ...]"""
    if not entries:
        print("  No entries supplied.")
        return

    usernames   = [e[0] for e in entries]
    first_names = [e[1] for e in entries]
    phones      = [e[2] for e in entries]
    types       = [e[3] if len(e) > 3 else "mobile" for e in entries]

    try:
        with _conn() as conn, conn.cursor() as cur:
            # Use a function wrapper so we can SELECT the INOUT result.
            # Passing the seed array as empty text[] and reading back the
            # modified value via a temp table avoids the psycopg2 CALL/INOUT
            # limitation where fetchone() returns None after CALL.
            cur.execute("""
                DO $$
                DECLARE
                    v_invalid TEXT[];
                BEGIN
                    CALL bulk_insert_contacts(
                        %s::varchar[],
                        %s::varchar[],
                        %s::varchar[],
                        %s::varchar[],
                        v_invalid
                    );
                    -- stash result in a temp table so Python can read it
                    CREATE TEMP TABLE IF NOT EXISTS _bulk_result (invalid TEXT[]);
                    DELETE FROM _bulk_result;
                    INSERT INTO _bulk_result VALUES (v_invalid);
                END;
                $$;
                SELECT invalid FROM _bulk_result;
            """, (usernames, first_names, phones, types))
            result = cur.fetchone()
        invalid = result[0] if result and result[0] else []
        if invalid:
            print(f"\n  ⚠️  {len(invalid)} invalid phone(s) skipped:")
            for entry in invalid:
                print(f"     ✗  {entry}")
        else:
            print("  ✓  All entries processed.")
    except Exception as e:
        print(f"  Error: {e}")


def prompt_and_bulk_insert():
    print("\n──── Bulk Insert ────")
    print("  Enter contacts one by one. Leave username blank to finish.\n")
    entries = []
    while True:
        username = input("  Username (blank to stop): ").strip()
        if not username:
            break
        first_name = input("  First name : ").strip()
        phone      = input("  Phone      : ").strip()
        ptype      = input("  Phone type (home/work/mobile) [mobile]: ").strip() or "mobile"
        entries.append((username, first_name, phone, ptype))
        print()

    if not entries:
        print("  Nothing entered.")
        return
    print(f"\n  Submitting {len(entries)} contact(s)…")
    bulk_insert_contacts(entries)


# ── 5. search ────────────────────────────────────────────────────────────────

def search_contacts(pattern: str):
    try:
        with _conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT * FROM search_contacts(%s::varchar);", (pattern,))
            rows = cur.fetchall()
        print(f"\n──── Search: '{pattern}' ────")
        _print_contacts(rows)
        # Show phones for each result
        for r in rows:
            print(f"  Phones for {r[1]}:")
            _print_phones(r[0])
    except Exception as e:
        print(f"  Error: {e}")


# ── 6. filter by group ────────────────────────────────────────────────────────

def filter_by_group(group_name: str):
    try:
        with _conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT * FROM filter_by_group(%s::varchar);", (group_name,))
            rows = cur.fetchall()
        print(f"\n──── Group: {group_name} ────")
        _print_contacts(rows, headers=["ID", "Username", "First Name", "Email", "Birthday"])
    except Exception as e:
        print(f"  Error: {e}")


def prompt_and_filter_group():
    print("\n──── Filter by Group ────")
    groups = _get_groups()
    print(f"  Available groups: {', '.join(groups)}")
    group_name = input("  Group name: ").strip()
    filter_by_group(group_name)


# ── 7. paginated browsing ─────────────────────────────────────────────────────

def get_contacts_page(page_num: int, page_size: int, sort_by: str = "name"):
    try:
        with _conn() as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM get_contacts_page(%s::int, %s::int, %s::varchar);",
                (page_num, page_size, sort_by)
            )
            rows = cur.fetchall()
        return rows
    except Exception as e:
        print(f"  Error: {e}")
        return []


def paginated_browser():
    """Interactive next/prev/quit page navigator."""
    print("\n──── Browse Contacts ────")
    try:
        page_size = int(input("  Rows per page [5]: ").strip() or "5")
    except ValueError:
        page_size = 5

    print("  Sort by: 1) Name  2) Birthday  3) Date added")
    sort_choice = input("  Choice [1]: ").strip()
    sort_map = {"1": "name", "2": "birthday", "3": "created_at"}
    sort_by = sort_map.get(sort_choice, "name")

    page = 1
    while True:
        rows = get_contacts_page(page, page_size, sort_by)
        print(f"\n──── Page {page}  (sort: {sort_by}) ────")
        _print_contacts(rows)

        if not rows:
            print("  No more records.")
            break

        cmd = input("\n  [n] Next  [p] Prev  [q] Quit: ").strip().lower()
        if cmd == "n":
            page += 1
        elif cmd == "p":
            page = max(1, page - 1)
        elif cmd == "q":
            break


# ── 8. delete ─────────────────────────────────────────────────────────────────

def delete_contact(identifier: str, delete_type: str):
    try:
        with _conn() as conn, conn.cursor() as cur:
            cur.execute("CALL delete_contact(%s::varchar, %s::varchar);", (identifier, delete_type))
        print(f"  ✓  Deleted contact where {delete_type} = '{identifier}'.")
    except Exception as e:
        print(f"  Error: {e}")


def prompt_and_delete():
    print("\n──── Delete Contact ────")
    print("  1 – by username")
    print("  2 – by phone")
    choice = input("  Choice: ").strip()
    if choice == "1":
        val = input("  Username: ").strip()
        if input(f"  Delete '{val}'? (y/n): ").lower() == "y":
            delete_contact(val, "username")
    elif choice == "2":
        val = input("  Phone: ").strip()
        if input(f"  Delete contact with phone '{val}'? (y/n): ").lower() == "y":
            delete_contact(val, "phone")
    else:
        print("  Invalid choice.")


# ── 9. CSV import (extended) ──────────────────────────────────────────────────
# Expected CSV columns (extra columns ignored):
#   username, first_name, phone, phone_type, email, birthday, group

def import_from_csv(filepath: str = "contacts.csv"):
    """
    Extended CSV importer.  Handles original 3-column CSVs gracefully;
    uses new fields when present.
    """
    inserted = 0
    skipped  = 0
    groups   = _get_groups()

    try:
        with open(filepath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            with _conn() as conn, conn.cursor() as cur:
                for row in reader:
                    username   = (row.get("username") or "").strip()
                    first_name = (row.get("first_name") or "").strip()
                    if not username or not first_name:
                        skipped += 1
                        continue

                    email  = (row.get("email") or "").strip() or None
                    bday   = None
                    braw   = (row.get("birthday") or "").strip()
                    if braw:
                        try:
                            bday = datetime.strptime(braw, "%Y-%m-%d").date()
                        except ValueError:
                            pass

                    gname    = (row.get("group") or "").strip()
                    group_id = groups.get(gname)

                    phone  = str(row.get("phone") or "").strip()
                    ptype  = (row.get("phone_type") or "mobile").strip()

                    cur.execute(
                        """
                INSERT INTO contacts (username, first_name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (username) DO UPDATE SET
                    first_name = EXCLUDED.first_name,
                    email      = COALESCE(EXCLUDED.email,    contacts.email),
                    birthday   = COALESCE(EXCLUDED.birthday, contacts.birthday),
                    group_id   = COALESCE(EXCLUDED.group_id, contacts.group_id)
            """,
                        (username, first_name, email, bday, group_id)
                    )

                    if phone:
                        # fetch the contact id to insert the phone
                        cur.execute("SELECT id FROM contacts WHERE username = %s;", (username,))
                        cid = cur.fetchone()
                        if cid and phone.replace("+","").replace("-","").replace(" ","").replace("(","").replace(")","").isdigit():
                            cur.execute(
                                "INSERT INTO phones (contact_id, phone, type) "
                                "VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;",
                                (cid[0], phone, ptype if ptype in ("home","work","mobile") else "mobile")
                            )
                    inserted += 1

        print(f"  ✓  CSV import done: {inserted} processed, {skipped} skipped.")
    except FileNotFoundError:
        print(f"  File '{filepath}' not found.")
    except Exception as e:
        print(f"  Error: {e}")


# ── 10. JSON export ───────────────────────────────────────────────────────────

def export_to_json(filepath: str = "contacts_export.json"):
    """Export all contacts (with phones and group) to JSON."""
    try:
        with _conn() as conn, conn.cursor() as cur:
            cur.execute("""
                SELECT c.id, c.username, c.first_name, c.email,
                       c.birthday, g.name AS group_name, c.created_at
                FROM   contacts c
                LEFT JOIN groups g ON g.id = c.group_id
                ORDER BY c.id;
            """)
            contacts_raw = cur.fetchall()

            records = []
            for cid, username, first_name, email, birthday, group_name, created_at in contacts_raw:
                cur.execute(
                    "SELECT phone, type FROM phones WHERE contact_id = %s ORDER BY type;",
                    (cid,)
                )
                phones = [{"phone": p, "type": t} for p, t in cur.fetchall()]

                records.append({
                    "username":   username,
                    "first_name": first_name,
                    "email":      email,
                    "birthday":   birthday.isoformat() if birthday else None,
                    "group":      group_name,
                    "phones":     phones,
                    "created_at": created_at.isoformat() if created_at else None,
                })

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)

        print(f"  ✓  Exported {len(records)} contacts to '{filepath}'.")
    except Exception as e:
        print(f"  Error: {e}")


# ── 11. JSON import ───────────────────────────────────────────────────────────

def import_from_json(filepath: str = "contacts_import.json"):
    """
    Import contacts from JSON.
    On duplicate username, ask user: skip or overwrite.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            records = json.load(f)
    except FileNotFoundError:
        print(f"  File '{filepath}' not found.")
        return
    except json.JSONDecodeError as e:
        print(f"  Invalid JSON: {e}")
        return

    groups  = _get_groups()
    inserted = skipped = overwritten = 0

    try:
        with _conn() as conn, conn.cursor() as cur:
            for rec in records:
                username   = (rec.get("username") or "").strip()
                first_name = (rec.get("first_name") or "").strip()
                if not username or not first_name:
                    skipped += 1
                    continue

                # Check duplicate
                cur.execute("SELECT id FROM contacts WHERE username = %s;", (username,))
                existing = cur.fetchone()

                if existing:
                    answer = input(
                        f"  '{username}' already exists. Overwrite? (y/n/a=all): "
                    ).strip().lower()
                    if answer not in ("y", "a"):
                        skipped += 1
                        continue
                    overwritten += 1

                email  = rec.get("email")
                bday   = None
                braw   = rec.get("birthday")
                if braw:
                    try:
                        bday = datetime.strptime(braw[:10], "%Y-%m-%d").date()
                    except ValueError:
                        pass

                gname    = (rec.get("group") or "").strip()
                group_id = groups.get(gname)

                cur.execute(
                    """
                INSERT INTO contacts (username, first_name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (username) DO UPDATE SET
                    first_name = EXCLUDED.first_name,
                    email      = COALESCE(EXCLUDED.email,    contacts.email),
                    birthday   = COALESCE(EXCLUDED.birthday, contacts.birthday),
                    group_id   = COALESCE(EXCLUDED.group_id, contacts.group_id)
            """,
                    (username, first_name, email, bday, group_id)
                )

                # Re-fetch id (needed for phone insert)
                cur.execute("SELECT id FROM contacts WHERE username = %s;", (username,))
                cid = cur.fetchone()[0]

                for ph in rec.get("phones", []):
                    phone = (ph.get("phone") or "").strip()
                    ptype = (ph.get("type") or "mobile").strip()
                    if phone:
                        cur.execute(
                            "INSERT INTO phones (contact_id, phone, type) "
                            "VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;",
                            (cid, phone, ptype if ptype in ("home","work","mobile") else "mobile")
                        )
                inserted += 1

        print(f"\n  ✓  JSON import done: {inserted} inserted, "
              f"{overwritten} overwritten, {skipped} skipped.")
    except Exception as e:
        print(f"  Error: {e}")


# ── main menu ─────────────────────────────────────────────────────────────────

def main():
    print("\n  Setting up database…")
    setup_database()

    while True:
        print("\n" + "═" * 46)
        print("  PhoneBook  –  PostgreSQL + PL/pgSQL  (TSIS1)")
        print("═" * 46)
        print("  1  │  Import contacts from CSV")
        print("  2  │  Add / Update contact")
        print("  3  │  Add phone number to contact")
        print("  4  │  Move contact to group")
        print("  5  │  Bulk insert with validation")
        print("  6  │  Search  (name / username / email / phone)")
        print("  7  │  Filter by group")
        print("  8  │  Browse contacts  (paginated)")
        print("  9  │  Delete contact")
        print(" 10  │  Export to JSON")
        print(" 11  │  Import from JSON")
        print("  0  │  Exit")
        print("═" * 46)
        choice = input("  Choice: ").strip()

        if   choice == "1":  import_from_csv()
        elif choice == "2":  prompt_and_upsert()
        elif choice == "3":  prompt_and_add_phone()
        elif choice == "4":  prompt_and_move_group()
        elif choice == "5":  prompt_and_bulk_insert()
        elif choice == "6":
            pattern = input("  Search pattern: ").strip()
            search_contacts(pattern)
        elif choice == "7":  prompt_and_filter_group()
        elif choice == "8":  paginated_browser()
        elif choice == "9":  prompt_and_delete()
        elif choice == "10": export_to_json()
        elif choice == "11":
            fp = input("  JSON file path [contacts_import.json]: ").strip() or "contacts_import.json"
            import_from_json(fp)
        elif choice == "0":
            print("  Bye!")
            break
        else:
            print("  Invalid choice.")


if __name__ == "__main__":
    main()
import psycopg2
from config import load_config
from pathlib import Path

SQL_DIR = Path(__file__).resolve().parent

CREATE_TABLES_SQL = '''
CREATE TABLE IF NOT EXISTS students(
    student_id SERIAL PRIMARY KEY,
    student_name VARCHAR(255) NOT NULL UNIQUE,
    student_phone VARCHAR(20) NOT NULL,
    student_faculty VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS teachers(
    teacher_id SERIAL PRIMARY KEY,
    teacher_name VARCHAR(255) NOT NULL,
    teacher_phone VARCHAR(20) NOT NULL,
    outlook VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS parents(
    parent_id SERIAL PRIMARY KEY,
    parent_name VARCHAR(255) NOT NULL,
    parent_phone VARCHAR(20) NOT NULL,
    student_name VARCHAR(255) NOT NULL REFERENCES students(student_name)
);
'''


def execute_sql(conn, sql):
    with conn.cursor() as cur:
        cur.execute(sql)


def execute_sql_file(conn, path):
    with open(path, 'r', encoding='utf-8') as f:
        execute_sql(conn, f.read())


def setup_database():
    config = load_config()
    with psycopg2.connect(**config) as conn:
        execute_sql(conn, CREATE_TABLES_SQL)
        execute_sql_file(conn, SQL_DIR / 'functions.sql')
        execute_sql_file(conn, SQL_DIR / 'procedures.sql')


def query_all_students(conn):
    with conn.cursor() as cur:
        cur.execute('SELECT student_id, student_name, student_phone, student_faculty FROM students ORDER BY student_id')
        return cur.fetchall()


def get_students_by_pattern(conn, pattern):
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM get_students_by_pattern(%s)', (pattern,))
        return cur.fetchall()


def get_students_paginated(conn, limit, offset):
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM get_students_paginated(%s, %s)', (limit, offset))
        return cur.fetchall()


def call_upsert_student(conn, name, phone, faculty='General'):
    with conn.cursor() as cur:
        cur.execute('CALL upsert_student(%s, %s, %s)', (name, phone, faculty))


def call_bulk_upsert_students(conn, records):
    with conn.cursor() as cur:
        cur.callproc('bulk_upsert_students', [records])
        # OUT parameter returns a single row with p_invalid_records
        result = cur.fetchone()
        return result[0] if result else []


def call_delete_student(conn, name=None, phone=None):
    with conn.cursor() as cur:
        cur.execute('CALL delete_student(%s, %s)', (name, phone))


if __name__ == '__main__':
    setup_database()
    config = load_config()
    with psycopg2.connect(**config) as conn:
        print('Inserting sample contacts...')
        call_upsert_student(conn, 'Alice Johnson', '555-0123', 'Engineering')
        call_upsert_student(conn, 'Bob Smith', '555-0456', 'Mathematics')
        call_upsert_student(conn, 'Cara Lee', '555-0789', 'Computer Science')

        print('Query by pattern "Smith":', get_students_by_pattern(conn, 'Smith'))
        print('Query paginated (limit 2 offset 0):', get_students_paginated(conn, 2, 0))

        print('Bulk upsert with 1 invalid record...')
        invalids = call_bulk_upsert_students(conn, [
            'David Patel|555-1011|Physics',
            'InvalidEntryNoSep',
            'Elena Martinez|12345|Biology'
        ])
        print('Invalid records returned:', invalids)

        print('Deleting by phone...')
        call_delete_student(conn, phone='555-0456')
        print('All students after delete:', query_all_students(conn))

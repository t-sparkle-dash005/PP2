import psycopg2
from config import load_config
import csv

def phonebook():
    commands = (
        """
        CREATE TABLE students(
            student_id SERIAL PRIMARY KEY,
            student_name VARCHAR(255) NOT NULL UNIQUE,
            student_phone VARCHAR(20) NOT NULL,
            student_faculty VARCHAR(20) NOT NULL
        )
        """,
        """
        CREATE TABLE teachers(
            teacher_id SERIAL PRIMARY KEY,
            teacher_name VARCHAR(255) NOT NULL,
            teacher_phone VARCHAR(20) NOT NULL,
            outlook VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE parents(
            parent_id SERIAL PRIMARY KEY,
            parent_name VARCHAR(255) NOT NULL,
            parent_phone VARCHAR(20) NOT NULL,
            student_name VARCHAR(255) NOT NULL,
            FOREIGN KEY (student_name)
            REFERENCES students (student_name)
        )
        """)
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                for command in commands:
                    cur.execute(command)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
if __name__ == '__main__':
    phonebook()


def read_phonebook(filename):
    phonebook = []
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            phonebook.append(row)
    return phonebook

def display_phonebook(phonebook):
    for person in phonebook:
        print(f"Name: {person['student_name']}, Phone: {person['student_phone']}, Faculty: {person['student_faculty']}")

filename = "contacts.csv"
data = read_phonebook(filename)
display_phonebook(data)
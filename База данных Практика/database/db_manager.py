# database/db_manager.py
import sqlite3
from config import DB_NAME

def get_connection():
    """Устанавливает соединение с базой данных"""
    return sqlite3.connect(DB_NAME)

def initialize_db():
    """Инициализирует базу данных: создаёт все таблицы, если они ещё не существуют"""
    conn = get_connection()
    cursor = conn.cursor()

    # Таблица "Преподаватели"
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            department TEXT,
            phone TEXT,
            email TEXT
        )
    ''')

    # Таблица "Аудитории"
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS classrooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_number TEXT NOT NULL,
            capacity INTEGER,
            building TEXT,
            has_projector INTEGER DEFAULT 0,
            has_computers INTEGER DEFAULT 0
        )
    ''')

    # Таблица "Группы студентов"
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT NOT NULL,
            course INTEGER,
            specialty TEXT,
            student_count INTEGER
        )
    ''')

    # Таблица "Дисциплины"
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            hours_per_semester INTEGER,
            teacher_id INTEGER,
            FOREIGN KEY (teacher_id) REFERENCES teachers(id)
        )
    ''')

    # Таблица "Занятия" (основная таблица расписания)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER,
            group_id INTEGER,
            teacher_id INTEGER,
            classroom_id INTEGER,
            lesson_date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            lesson_type TEXT CHECK(lesson_type IN ('лекция', 'практика', 'лабораторная')) DEFAULT 'лекция',
            week_type TEXT CHECK(week_type IN ('числитель', 'знаменатель', 'обе')) DEFAULT 'обе',
            FOREIGN KEY (subject_id) REFERENCES subjects(id),
            FOREIGN KEY (group_id) REFERENCES groups(id),
            FOREIGN KEY (teacher_id) REFERENCES teachers(id),
            FOREIGN KEY (classroom_id) REFERENCES classrooms(id)
        )
    ''')

    # Таблица "Расписание занятий" (связь многие-ко-многим)
    # Позволяет создавать сложные расписания
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            semester INTEGER,
            academic_year TEXT,
            is_active INTEGER DEFAULT 1
        )
    ''')

    # Таблица-связка "Расписание-Занятия"
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedule_lessons (
            schedule_id INTEGER,
            lesson_id INTEGER,
            FOREIGN KEY (schedule_id) REFERENCES schedules(id),
            FOREIGN KEY (lesson_id) REFERENCES lessons(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("База данных успешно инициализирована")
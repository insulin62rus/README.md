# models/lesson.py
from database.db_manager import get_connection

class Lesson:
    def __init__(self, id=None, subject_id=None, group_id=None, teacher_id=None, 
                 classroom_id=None, lesson_date=None, start_time=None, 
                 end_time=None, lesson_type="лекция", week_type="обе"):
        self.id = id
        self.subject_id = subject_id
        self.group_id = group_id
        self.teacher_id = teacher_id
        self.classroom_id = classroom_id
        self.lesson_date = lesson_date
        self.start_time = start_time
        self.end_time = end_time
        self.lesson_type = lesson_type
        self.week_type = week_type

    def save(self):
        """Сохраняет занятие в базу данных"""
        conn = get_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            cursor.execute('''
                INSERT INTO lessons (subject_id, group_id, teacher_id, classroom_id, 
                                    lesson_date, start_time, end_time, lesson_type, week_type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (self.subject_id, self.group_id, self.teacher_id, self.classroom_id,
                  self.lesson_date, self.start_time, self.end_time, self.lesson_type, self.week_type))
            self.id = cursor.lastrowid
        else:
            cursor.execute('''
                UPDATE lessons 
                SET subject_id = ?, group_id = ?, teacher_id = ?, classroom_id = ?,
                    lesson_date = ?, start_time = ?, end_time = ?, lesson_type = ?, week_type = ?
                WHERE id = ?
            ''', (self.subject_id, self.group_id, self.teacher_id, self.classroom_id,
                  self.lesson_date, self.start_time, self.end_time, self.lesson_type, 
                  self.week_type, self.id))
        
        conn.commit()
        conn.close()

    def delete(self):
        """Удаляет занятие"""
        if self.id is not None:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM lessons WHERE id = ?", (self.id,))
            conn.commit()
            conn.close()


# Функции для работы с расписанием
def get_all_lessons():
    """Возвращает список всех занятий"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, subject_id, group_id, teacher_id, classroom_id, 
               lesson_date, start_time, end_time, lesson_type, week_type 
        FROM lessons
        ORDER BY lesson_date, start_time
    ''')
    rows = cursor.fetchall()
    conn.close()
    
    lessons = []
    for row in rows:
        lesson = Lesson(
            id=row[0], subject_id=row[1], group_id=row[2], 
            teacher_id=row[3], classroom_id=row[4], lesson_date=row[5],
            start_time=row[6], end_time=row[7], lesson_type=row[8], week_type=row[9]
        )
        lessons.append(lesson)
    return lessons


def get_lessons_by_group_and_date(group_id, lesson_date):
    """Возвращает занятия группы на конкретную дату"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, subject_id, group_id, teacher_id, classroom_id, 
               lesson_date, start_time, end_time, lesson_type, week_type 
        FROM lessons
        WHERE group_id = ? AND lesson_date = ?
        ORDER BY start_time
    ''', (group_id, lesson_date))
    rows = cursor.fetchall()
    conn.close()
    
    lessons = []
    for row in rows:
        lesson = Lesson(
            id=row[0], subject_id=row[1], group_id=row[2], 
            teacher_id=row[3], classroom_id=row[4], lesson_date=row[5],
            start_time=row[6], end_time=row[7], lesson_type=row[8], week_type=row[9]
        )
        lessons.append(lesson)
    return lessons


def get_lessons_by_teacher_and_date(teacher_id, lesson_date):
    """Возвращает занятия преподавателя на конкретную дату"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT l.id, l.subject_id, l.group_id, l.teacher_id, l.classroom_id, 
               l.lesson_date, l.start_time, l.end_time, l.lesson_type, l.week_type,
               g.group_name
        FROM lessons l
        LEFT JOIN groups g ON l.group_id = g.id
        WHERE l.teacher_id = ? AND l.lesson_date = ?
        ORDER BY l.start_time
    ''', (teacher_id, lesson_date))
    rows = cursor.fetchall()
    conn.close()
    
    lessons = []
    for row in rows:
        lesson = Lesson(
            id=row[0], subject_id=row[1], group_id=row[2], 
            teacher_id=row[3], classroom_id=row[4], lesson_date=row[5],
            start_time=row[6], end_time=row[7], lesson_type=row[8], week_type=row[9]
        )
        lesson.group_name = row[10] if len(row) > 10 else f"Группа ID:{lesson.group_id}"
        lessons.append(lesson)
    return lessons
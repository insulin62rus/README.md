# models/group.py
from database.db_manager import get_connection

class Group:
    def __init__(self, id=None, group_name=None, course=None, specialty=None, student_count=None):
        self.id = id
        self.group_name = group_name
        self.course = course
        self.specialty = specialty
        self.student_count = student_count

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            cursor.execute('''
                INSERT INTO groups (group_name, course, specialty, student_count)
                VALUES (?, ?, ?, ?)
            ''', (self.group_name, self.course, self.specialty, self.student_count))
            self.id = cursor.lastrowid
        else:
            cursor.execute('''
                UPDATE groups SET group_name = ?, course = ?, specialty = ?, student_count = ?
                WHERE id = ?
            ''', (self.group_name, self.course, self.specialty, self.student_count, self.id))
        
        conn.commit()
        conn.close()

    def delete(self):
        if self.id is not None:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM groups WHERE id = ?", (self.id,))
            conn.commit()
            conn.close()

def get_all_groups():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, group_name, course, specialty, student_count FROM groups")
    rows = cursor.fetchall()
    conn.close()
    return [Group(id=row[0], group_name=row[1], course=row[2], 
                  specialty=row[3], student_count=row[4]) for row in rows]
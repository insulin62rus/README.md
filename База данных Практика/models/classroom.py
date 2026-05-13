# models/classroom.py
from database.db_manager import get_connection

class Classroom:
    def __init__(self, id=None, room_number=None, capacity=None, building=None, 
                 has_projector=0, has_computers=0):
        self.id = id
        self.room_number = room_number
        self.capacity = capacity
        self.building = building
        self.has_projector = has_projector
        self.has_computers = has_computers

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            cursor.execute('''
                INSERT INTO classrooms (room_number, capacity, building, has_projector, has_computers)
                VALUES (?, ?, ?, ?, ?)
            ''', (self.room_number, self.capacity, self.building, self.has_projector, self.has_computers))
            self.id = cursor.lastrowid
        else:
            cursor.execute('''
                UPDATE classrooms SET room_number = ?, capacity = ?, building = ?, 
                                    has_projector = ?, has_computers = ?
                WHERE id = ?
            ''', (self.room_number, self.capacity, self.building, 
                  self.has_projector, self.has_computers, self.id))
        
        conn.commit()
        conn.close()

    def delete(self):
        if self.id is not None:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM classrooms WHERE id = ?", (self.id,))
            conn.commit()
            conn.close()

def get_all_classrooms():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, room_number, capacity, building, has_projector, has_computers FROM classrooms")
    rows = cursor.fetchall()
    conn.close()
    return [Classroom(id=row[0], room_number=row[1], capacity=row[2], 
                      building=row[3], has_projector=row[4], has_computers=row[5]) for row in rows]
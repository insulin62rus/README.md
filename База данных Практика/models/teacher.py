# models/teacher.py
from database.db_manager import get_connection

class Teacher:
    def __init__(self, id=None, full_name=None, department=None, phone=None, email=None):
        self.id = id
        self.full_name = full_name
        self.department = department
        self.phone = phone
        self.email = email

    def save(self):
        """Добавляет нового преподавателя или обновляет существующего"""
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            if self.id is None:
                cursor.execute('''
                    INSERT INTO teachers (full_name, department, phone, email)
                    VALUES (?, ?, ?, ?)
                ''', (self.full_name, self.department, self.phone, self.email))
                self.id = cursor.lastrowid
            else:
                cursor.execute('''
                    UPDATE teachers 
                    SET full_name = ?, department = ?, phone = ?, email = ?
                    WHERE id = ?
                ''', (self.full_name, self.department, self.phone, self.email, self.id))
            
            conn.commit()
            return True
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Ошибка при сохранении преподавателя: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete(self):
        """Удаляет преподавателя"""
        if self.id is not None:
            conn = None
            cursor = None
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM teachers WHERE id = ?", (self.id,))
                conn.commit()
                return True
            except Exception as e:
                if conn:
                    conn.rollback()
                print(f"Ошибка при удалении преподавателя: {e}")
                return False
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
        return False

    def update(self):
        """Обновляет данные преподавателя"""
        if self.id is not None:
            return self.save()
        return False

    def __str__(self):
        return f"{self.full_name} ({self.department})"

    def __repr__(self):
        return f"Teacher(id={self.id}, full_name='{self.full_name}', department='{self.department}')"


def get_all_teachers():
    """Возвращает список всех преподавателей"""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, full_name, department, phone, email FROM teachers ORDER BY full_name")
        rows = cursor.fetchall()
        
        teachers = []
        for row in rows:
            teacher = Teacher(
                id=row[0], 
                full_name=row[1], 
                department=row[2], 
                phone=row[3], 
                email=row[4]
            )
            teachers.append(teacher)
        
        return teachers
    except Exception as e:
        print(f"Ошибка при получении списка преподавателей: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_teacher_by_id(teacher_id):
    """Возвращает преподавателя по ID"""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, full_name, department, phone, email FROM teachers WHERE id = ?", (teacher_id,))
        row = cursor.fetchone()
        
        if row:
            return Teacher(
                id=row[0], 
                full_name=row[1], 
                department=row[2], 
                phone=row[3], 
                email=row[4]
            )
        return None
    except Exception as e:
        print(f"Ошибка при получении преподавателя по ID {teacher_id}: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def search_teachers_by_name(search_term):
    """Поиск преподавателей по имени"""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, full_name, department, phone, email 
            FROM teachers 
            WHERE full_name LIKE ? 
            ORDER BY full_name
        ''', (f'%{search_term}%',))
        rows = cursor.fetchall()
        
        teachers = []
        for row in rows:
            teacher = Teacher(
                id=row[0], 
                full_name=row[1], 
                department=row[2], 
                phone=row[3], 
                email=row[4]
            )
            teachers.append(teacher)
        
        return teachers
    except Exception as e:
        print(f"Ошибка при поиске преподавателей: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def count_teachers():
    """Возвращает количество преподавателей в базе"""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM teachers")
        count = cursor.fetchone()[0]
        return count
    except Exception as e:
        print(f"Ошибка при подсчёте преподавателей: {e}")
        return 0
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
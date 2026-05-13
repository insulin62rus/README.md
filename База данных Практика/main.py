# main.py
from database.db_manager import initialize_db
from models.teacher import Teacher, get_all_teachers
from models.group import Group, get_all_groups
from models.classroom import Classroom, get_all_classrooms
from models.lesson import Lesson, get_all_lessons, get_lessons_by_group_and_date, get_lessons_by_teacher_and_date
from datetime import datetime

def show_main_menu():
    print("\n" + "="*50)
    print("        СИСТЕМА СОСТАВЛЕНИЯ РАСПИСАНИЯ ЗАНЯТИЙ")
    print("="*50)
    print("1. Управление преподавателями")
    print("2. Управление группами")
    print("3. Управление аудиториями")
    print("4. Управление расписанием занятий")
    print("5. Просмотр расписания")
    print("0. Выход")
    return input("Выберите действие: ")


def menu_teachers():
    while True:
        print("\n=== УПРАВЛЕНИЕ ПРЕПОДАВАТЕЛЯМИ ===")
        print("1. Показать всех преподавателей")
        print("2. Добавить преподавателя")
        print("3. Удалить преподавателя")
        print("0. Назад")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            teachers = get_all_teachers()
            if not teachers:
                print("Список преподавателей пуст.")
            else:
                print("\nСписок преподавателей:")
                for t in teachers:
                    teacher_id = getattr(t, 'id', '?')
                    full_name = getattr(t, 'full_name', 'Не указано')
                    department = getattr(t, 'department', 'Не указана')
                    phone = getattr(t, 'phone', 'Не указан')
                    print(f"{teacher_id}. {full_name} | Кафедра: {department} | Тел.: {phone}")
        
        elif choice == "2":
            print("\n=== Добавление преподавателя ===")
            full_name = input("ФИО: ")
            department = input("Кафедра: ")
            phone = input("Телефон: ")
            email = input("Email: ")
            teacher = Teacher(full_name=full_name, department=department, phone=phone, email=email)
            teacher.save()
            print("✓ Преподаватель добавлен.")
        
        elif choice == "3":
            try:
                teacher_id = int(input("Введите ID преподавателя для удаления: "))
                teacher = Teacher(id=teacher_id)
                teacher.delete()
                print("✓ Преподаватель удалён.")
            except ValueError:
                print("Ошибка: ID должен быть числом.")
            except Exception as e:
                print(f"Ошибка при удалении: {e}")
        
        elif choice == "0":
            break


def menu_groups():
    while True:
        print("\n=== УПРАВЛЕНИЕ ГРУППАМИ ===")
        print("1. Показать все группы")
        print("2. Добавить группу")
        print("3. Удалить группу")
        print("0. Назад")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            groups = get_all_groups()
            if not groups:
                print("Список групп пуст.")
            else:
                print("\nСписок групп:")
                for g in groups:
                    group_id = getattr(g, 'id', '?')
                    group_name = getattr(g, 'group_name', 'Не указано')
                    course = getattr(g, 'course', '?')
                    specialty = getattr(g, 'specialty', 'Не указана')
                    student_count = getattr(g, 'student_count', '?')
                    print(f"{group_id}. {group_name} | {course} курс | Спец.: {specialty} | {student_count} чел.")
        
        elif choice == "2":
            print("\n=== Добавление группы ===")
            try:
                group_name = input("Название группы: ")
                course = int(input("Курс: "))
                specialty = input("Специальность: ")
                student_count = int(input("Количество студентов: "))
                group = Group(group_name=group_name, course=course, specialty=specialty, student_count=student_count)
                group.save()
                print("✓ Группа добавлена.")
            except ValueError:
                print("Ошибка: Курс и количество студентов должны быть числами.")
        
        elif choice == "3":
            try:
                group_id = int(input("Введите ID группы для удаления: "))
                group = Group(id=group_id)
                group.delete()
                print("✓ Группа удалена.")
            except ValueError:
                print("Ошибка: ID должен быть числом.")
            except Exception as e:
                print(f"Ошибка при удалении: {e}")
        
        elif choice == "0":
            break


def menu_classrooms():
    while True:
        print("\n=== УПРАВЛЕНИЕ АУДИТОРИЯМИ ===")
        print("1. Показать все аудитории")
        print("2. Добавить аудиторию")
        print("3. Удалить аудиторию")
        print("0. Назад")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            classrooms = get_all_classrooms()
            if not classrooms:
                print("Список аудиторий пуст.")
            else:
                print("\nСписок аудиторий:")
                for c in classrooms:
                    proj = "✅" if getattr(c, 'has_projector', False) else "❌"
                    comp = "✅" if getattr(c, 'has_computers', False) else "❌"
                    classroom_id = getattr(c, 'id', '?')
                    building = getattr(c, 'building', '?')
                    room_number = getattr(c, 'room_number', '?')
                    capacity = getattr(c, 'capacity', '?')
                    print(f"{classroom_id}. {building}-{room_number} | Вмест.: {capacity} | Проектор: {proj} | Компы: {comp}")
        
        elif choice == "2":
            print("\n=== Добавление аудитории ===")
            try:
                room_number = input("Номер аудитории: ")
                capacity = int(input("Вместимость: "))
                building = input("Корпус: ")
                has_projector = int(input("Есть проектор? (1 - да, 0 - нет): "))
                has_computers = int(input("Есть компьютеры? (1 - да, 0 - нет): "))
                classroom = Classroom(room_number=room_number, capacity=capacity, building=building,
                                      has_projector=bool(has_projector), has_computers=bool(has_computers))
                classroom.save()
                print("✓ Аудитория добавлена.")
            except ValueError:
                print("Ошибка: Вместимость должна быть числом.")
        
        elif choice == "3":
            try:
                classroom_id = int(input("Введите ID аудитории для удаления: "))
                classroom = Classroom(id=classroom_id)
                classroom.delete()
                print("✓ Аудитория удалена.")
            except ValueError:
                print("Ошибка: ID должен быть числом.")
            except Exception as e:
                print(f"Ошибка при удалении: {e}")
        
        elif choice == "0":
            break


def menu_lessons():
    while True:
        print("\n=== УПРАВЛЕНИЕ РАСПИСАНИЕМ ===")
        print("1. Показать все занятия")
        print("2. Добавить занятие")
        print("3. Удалить занятие")
        print("0. Назад")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            lessons = get_all_lessons()
            if not lessons:
                print("Расписание пусто.")
            else:
                print("\nСписок занятий:")
                for l in lessons:
                    lesson_id = getattr(l, 'id', '?')
                    group_id = getattr(l, 'group_id', '?')
                    teacher_id = getattr(l, 'teacher_id', '?')
                    classroom_id = getattr(l, 'classroom_id', '?')
                    lesson_date = getattr(l, 'lesson_date', '?')
                    start_time = getattr(l, 'start_time', '?')
                    end_time = getattr(l, 'end_time', '?')
                    lesson_type = getattr(l, 'lesson_type', '?')
                    print(f"{lesson_id}. Группа ID:{group_id} | Преп. ID:{teacher_id} | Ауд. ID:{classroom_id}")
                    print(f"   Дата: {lesson_date} | {start_time}-{end_time} | {lesson_type}")
        
        elif choice == "2":
            print("\n=== Добавление занятия ===")
            try:
                groups = get_all_groups()
                if not groups:
                    print("Сначала добавьте группы.")
                    continue
                print("\nДоступные группы:")
                for g in groups:
                    print(f"{g.id} - {g.group_name}")
                group_id = int(input("ID группы: "))
                
                teachers = get_all_teachers()
                if not teachers:
                    print("Сначала добавьте преподавателей.")
                    continue
                print("\nДоступные преподаватели:")
                for t in teachers:
                    print(f"{t.id} - {t.full_name}")
                teacher_id = int(input("ID преподавателя: "))
                
                classrooms = get_all_classrooms()
                if not classrooms:
                    print("Сначала добавьте аудитории.")
                    continue
                print("\nДоступные аудитории:")
                for c in classrooms:
                    print(f"{c.id} - {c.building}-{c.room_number}")
                classroom_id = int(input("ID аудитории: "))
                
                lesson_date = input("Дата (ГГГГ-ММ-ДД): ")
                try:
                    datetime.strptime(lesson_date, "%Y-%m-%d")
                except ValueError:
                    print("Ошибка: Неверный формат даты. Используйте ГГГГ-ММ-ДД")
                    continue
                
                start_time = input("Время начала (ЧЧ:ММ): ")
                end_time = input("Время окончания (ЧЧ:ММ): ")
                
                try:
                    datetime.strptime(start_time, "%H:%M")
                    datetime.strptime(end_time, "%H:%M")
                except ValueError:
                    print("Ошибка: Неверный формат времени. Используйте ЧЧ:ММ")
                    continue
                
                print("\nТип занятия: 1 - лекция, 2 - практика, 3 - лабораторная")
                type_choice = input("Выберите тип: ")
                lesson_type = {"1": "лекция", "2": "практика", "3": "лабораторная"}.get(type_choice, "лекция")
                
                lesson = Lesson(group_id=group_id, teacher_id=teacher_id, classroom_id=classroom_id,
                               lesson_date=lesson_date, start_time=start_time, end_time=end_time,
                               lesson_type=lesson_type)
                lesson.save()
                print("✓ Занятие добавлено в расписание.")
            
            except ValueError:
                print("Ошибка: ID должен быть числом.")
            except Exception as e:
                print(f"Ошибка при добавлении занятия: {e}")
        
        elif choice == "3":
            try:
                lesson_id = int(input("Введите ID занятия для удаления: "))
                lesson = Lesson(id=lesson_id)
                lesson.delete()
                print("✓ Занятие удалено.")
            except ValueError:
                print("Ошибка: ID должен быть числом.")
            except Exception as e:
                print(f"Ошибка при удалении: {e}")
        
        elif choice == "0":
            break


def view_schedule():
    while True:
        print("\n=== ПРОСМОТР РАСПИСАНИЯ ===")
        print("1. Расписание группы на день")
        print("2. Расписание преподавателя на день")
        print("0. Назад")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            try:
                groups = get_all_groups()
                if not groups:
                    print("Нет доступных групп.")
                    continue
                    
                print("\nДоступные группы:")
                for g in groups:
                    print(f"{g.id} - {g.group_name}")
                group_id = int(input("Введите ID группы: "))
                lesson_date = input("Введите дату (ГГГГ-ММ-ДД): ")
                
                try:
                    datetime.strptime(lesson_date, "%Y-%m-%d")
                except ValueError:
                    print("Ошибка: Неверный формат даты. Используйте ГГГГ-ММ-ДД")
                    continue
                
                lessons = get_lessons_by_group_and_date(group_id, lesson_date)
                print(f"\n{'='*50}")
                print(f"РАСПИСАНИЕ ГРУППЫ НА {lesson_date}")
                print(f"{'='*50}")
                
                if lessons:
                    for l in lessons:
                        start_time = getattr(l, 'start_time', '??:??')
                        end_time = getattr(l, 'end_time', '??:??')
                        lesson_type = getattr(l, 'lesson_type', '?')
                        classroom_id = getattr(l, 'classroom_id', '?')
                        print(f"{start_time} - {end_time} | {lesson_type} | Ауд. ID: {classroom_id}")
                else:
                    print("Занятий нет")
            except ValueError:
                print("Ошибка: ID группы должен быть числом.")
        
        elif choice == "2":
            try:
                teachers = get_all_teachers()
                if not teachers:
                    print("Нет доступных преподавателей.")
                    continue
                    
                print("\nДоступные преподаватели:")
                for t in teachers:
                    print(f"{t.id} - {t.full_name}")
                teacher_id = int(input("Введите ID преподавателя: "))
                lesson_date = input("Введите дату (ГГГГ-ММ-ДД): ")
                
                try:
                    datetime.strptime(lesson_date, "%Y-%m-%d")
                except ValueError:
                    print("Ошибка: Неверный формат даты. Используйте ГГГГ-ММ-ДД")
                    continue
                
                lessons = get_lessons_by_teacher_and_date(teacher_id, lesson_date)
                print(f"\n{'='*50}")
                print(f"РАСПИСАНИЕ ПРЕПОДАВАТЕЛЯ НА {lesson_date}")
                print(f"{'='*50}")
                
                if lessons:
                    for l in lessons:
                        start_time = getattr(l, 'start_time', '??:??')
                        end_time = getattr(l, 'end_time', '??:??')
                        lesson_type = getattr(l, 'lesson_type', '?')
                        classroom_id = getattr(l, 'classroom_id', '?')
                        group_name = getattr(l, 'group_name', 'Группа ?')
                        print(f"{start_time} - {end_time} | {lesson_type} | Группа: {group_name} | Ауд. ID: {classroom_id}")
                else:
                    print("Занятий нет")
            except ValueError:
                print("Ошибка: ID преподавателя должен быть числом.")
        
        elif choice == "0":
            break


def main():
    try:
        initialize_db()
        print("База данных успешно инициализирована.")
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")
        return
    
    while True:
        try:
            user_choice = show_main_menu()
            
            if user_choice == "1":
                menu_teachers()
            elif user_choice == "2":
                menu_groups()
            elif user_choice == "3":
                menu_classrooms()
            elif user_choice == "4":
                menu_lessons()
            elif user_choice == "5":
                view_schedule()
            elif user_choice == "0":
                print("Выход из программы. До свидания!")
                break
            else:
                print("Неверный ввод. Пожалуйста, выберите действие от 0 до 5.")
        except KeyboardInterrupt:
            print("\nПрограмма прервана пользователем.")
            break
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            continue

if __name__ == "__main__":
    main()
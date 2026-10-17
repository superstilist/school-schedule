"""Консольний інтерфейс для керування шкільним розкладом."""

import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdin.reconfigure(encoding="utf-8")
except Exception:
    pass

from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist

from .models import Subject, Teacher, Class, Student, Schedule, Grade, DAYS_OF_WEEK


def _input(prompt):
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        return ""


def _print_subjects():
    print("\nПредмети:")
    for s in Subject.objects.all():
        print(f"  - {s.name}: {s.description}")


def _print_classes():
    print("\nКласи:")
    for c in Class.objects.all():
        print(f"  - {c.name} (рік: {c.year})")


def _print_teachers():
    print("\nВчителі:")
    for t in Teacher.objects.select_related("subject").all():
        print(f"  - {t.last_name} {t.first_name} ({t.subject})")


def _print_students():
    print("\nУчні:")
    for s in Student.objects.select_related("school_class").all():
        print(f"  - {s.last_name} {s.first_name} ({s.school_class})")


def add_subject():
    print("\n--- Додавання предмету ---")
    name = _input("Назва предмету: ")
    if not name:
        print("Назва не може бути порожньою.")
        return
    if Subject.objects.filter(name__iexact=name).exists():
        print("Предмет з такою назвою вже існує.")
        return
    description = _input("Опис: ")
    Subject.objects.create(name=name, description=description)
    print("Предмет успішно збережено.")


def edit_subject():
    print("\n--- Редагування предмету ---")
    name = _input("Назва предмету для редагування: ")
    try:
        subject = Subject.objects.get(name__iexact=name)
    except Subject.DoesNotExist:
        print("Предмет не знайдено.")
        return
    new_name = _input(f"Нова назва (поточна: {subject.name}): ")
    if new_name and new_name.lower() != subject.name.lower():
        if Subject.objects.filter(name__iexact=new_name).exists():
            print("Предмет з такою назвою вже існує.")
            return
        subject.name = new_name
    new_desc = _input(f"Новий опис (поточний: {subject.description}): ")
    if new_desc:
        subject.description = new_desc
    subject.save()
    print("Предмет оновлено.")


def delete_subject():
    print("\n--- Видалення предмету ---")
    name = _input("Назва предмету для видалення: ")
    try:
        subject = Subject.objects.get(name__iexact=name)
    except Subject.DoesNotExist:
        print("Предмет не знайдено.")
        return
    confirm = _input(f"Видалити '{subject.name}'? (т/н): ")
    if confirm.lower() in ("т", "y", "yes", "так"):
        subject.delete()
        print("Предмет видалено.")
    else:
        print("Скасовано.")


def add_teacher():
    print("\n--- Додавання вчителя ---")
    first_name = _input("Ім'я: ")
    last_name = _input("Прізвище: ")
    subject_name = _input("Назва предмету: ")
    try:
        subject = Subject.objects.get(name__iexact=subject_name)
    except Subject.DoesNotExist:
        print("Предмет не знайдено. Спочатку додайте предмет.")
        return
    Teacher.objects.create(first_name=first_name, last_name=last_name, subject=subject)
    print("Вчителя успішно збережено.")


def add_class():
    print("\n--- Додавання класу ---")
    name = _input("Назва класу: ")
    if not name:
        print("Назва не може бути порожньою.")
        return
    if Class.objects.filter(name__iexact=name).exists():
        print("Клас з такою назвою вже існує.")
        return
    year_str = _input("Рік навчання: ")
    try:
        year = int(year_str)
    except ValueError:
        print("Некоректний рік.")
        return
    Class.objects.create(name=name, year=year)
    print("Клас успішно збережено.")


def edit_class():
    print("\n--- Редагування класу ---")
    name = _input("Назва класу для редагування: ")
    try:
        school_class = Class.objects.get(name__iexact=name)
    except Class.DoesNotExist:
        print("Клас не знайдено.")
        return
    new_name = _input(f"Нова назва (поточна: {school_class.name}): ")
    if new_name and new_name.lower() != school_class.name.lower():
        if Class.objects.filter(name__iexact=new_name).exists():
            print("Клас з такою назвою вже існує.")
            return
        school_class.name = new_name
    new_year = _input(f"Новий рік (поточний: {school_class.year}): ")
    if new_year:
        try:
            school_class.year = int(new_year)
        except ValueError:
            print("Некоректний рік.")
            return
    school_class.save()
    print("Клас оновлено.")


def delete_class():
    print("\n--- Видалення класу ---")
    name = _input("Назва класу для видалення: ")
    try:
        school_class = Class.objects.get(name__iexact=name)
    except Class.DoesNotExist:
        print("Клас не знайдено.")
        return
    confirm = _input(f"Видалити '{school_class.name}'? (т/н): ")
    if confirm.lower() in ("т", "y", "yes", "так"):
        school_class.delete()
        print("Клас видалено.")
    else:
        print("Скасовано.")


def add_student():
    print("\n--- Додавання учня ---")
    first_name = _input("Ім'я: ")
    last_name = _input("Прізвище: ")
    class_name = _input("Назва класу: ")
    try:
        school_class = Class.objects.get(name__iexact=class_name)
    except Class.DoesNotExist:
        print("Клас не знайдено. Спочатку додайте клас.")
        return
    Student.objects.create(first_name=first_name, last_name=last_name, school_class=school_class)
    print("Учня успішно збережено.")


def _get_teacher():
    last_name = _input("Прізвище вчителя: ")
    first_name = _input("Ім'я вчителя (можна порожнє): ")
    qs = Teacher.objects.filter(last_name__iexact=last_name)
    if first_name:
        qs = qs.filter(first_name__iexact=first_name)
    teachers = list(qs)
    if not teachers:
        print("Вчителя не знайдено.")
        return None
    if len(teachers) > 1:
        print("Знайдено кілька вчителів:")
        for i, t in enumerate(teachers, 1):
            print(f"  {i}. {t.last_name} {t.first_name} ({t.subject})")
        choice = _input("Оберіть номер: ")
        try:
            idx = int(choice) - 1
            return teachers[idx]
        except (ValueError, IndexError):
            print("Некоректний вибір.")
            return None
    return teachers[0]


def _get_student():
    last_name = _input("Прізвище учня: ")
    first_name = _input("Ім'я учня (можна порожнє): ")
    qs = Student.objects.filter(last_name__iexact=last_name)
    if first_name:
        qs = qs.filter(first_name__iexact=first_name)
    students = list(qs.select_related("school_class"))
    if not students:
        print("Учня не знайдено.")
        return None
    if len(students) > 1:
        print("Знайдено кілька учнів:")
        for i, s in enumerate(students, 1):
            print(f"  {i}. {s.last_name} {s.first_name} ({s.school_class})")
        choice = _input("Оберіть номер: ")
        try:
            idx = int(choice) - 1
            return students[idx]
        except (ValueError, IndexError):
            print("Некоректний вибір.")
            return None
    return students[0]


def add_schedule():
    print("\n--- Додавання заняття в розклад ---")
    print("Дні тижня: " + ", ".join(f"{k}={v}" for k, v in DAYS_OF_WEEK))
    day = _input("День тижня (код або назва): ").lower()
    day_code = None
    for code, name in DAYS_OF_WEEK:
        if day == code or day == name.lower():
            day_code = code
            break
    if day_code is None:
        print("Некоректний день тижня.")
        return
    time_str = _input("Година початку (HH:MM): ")
    try:
        start_time = datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        print("Некоректний час. Використовуйте формат HH:MM.")
        return
    subject_name = _input("Назва предмету: ")
    try:
        subject = Subject.objects.get(name__iexact=subject_name)
    except Subject.DoesNotExist:
        print("Предмет не знайдено.")
        return
    class_name = _input("Назва класу: ")
    try:
        school_class = Class.objects.get(name__iexact=class_name)
    except Class.DoesNotExist:
        print("Клас не знайдено.")
        return
    teacher = _get_teacher()
    if teacher is None:
        return
    Schedule.objects.create(
        day_of_week=day_code,
        start_time=start_time,
        subject=subject,
        school_class=school_class,
        teacher=teacher,
    )
    print("Заняття успішно додано до розкладу.")


def add_grade():
    print("\n--- Додавання оцінки ---")
    student = _get_student()
    if student is None:
        return
    subject_name = _input("Назва предмету: ")
    try:
        subject = Subject.objects.get(name__iexact=subject_name)
    except Subject.DoesNotExist:
        print("Предмет не знайдено.")
        return
    grade_str = _input("Оцінка: ")
    try:
        grade_val = int(grade_str)
    except ValueError:
        print("Некоректна оцінка.")
        return
    date_str = _input("Дата (РРРР-ММ-ДД, порожньо = сьогодні): ")
    if date_str:
        try:
            grade_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Некоректна дата.")
            return
    else:
        grade_date = datetime.today().date()
    Grade.objects.create(student=student, subject=subject, grade=grade_val, date=grade_date)
    print("Оцінку успішно збережено.")


MENU = [
    ("1", "Додати предмет", add_subject),
    ("2", "Редагувати предмет", edit_subject),
    ("3", "Видалити предмет", delete_subject),
    ("4", "Додати вчителя", add_teacher),
    ("5", "Додати клас", add_class),
    ("6", "Редагувати клас", edit_class),
    ("7", "Видалити клас", delete_class),
    ("8", "Додати учня", add_student),
    ("9", "Додати заняття в розклад", add_schedule),
    ("10", "Додати оцінку", add_grade),
    ("11", "Показати предмети", _print_subjects),
    ("12", "Показати класи", _print_classes),
    ("13", "Показати вчителів", _print_teachers),
    ("14", "Показати учнів", _print_students),
    ("0", "Вихід", None),
]


def run():
    while True:
        print("\n===== Керування шкільним розкладом =====")
        for code, label, _ in MENU:
            print(f"  {code}. {label}")
        choice = _input("Оберіть дію: ")
        if choice == "0":
            print("До побачення!")
            break
        action = None
        for code, _, fn in MENU:
            if code == choice:
                action = fn
                break
        if action is None:
            print("Невірний вибір.")
            continue
        try:
            action()
        except Exception as exc:  # noqa: BLE001
            print(f"Помилка: {exc}")

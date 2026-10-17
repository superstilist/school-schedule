from django.test import TestCase

from .models import Subject, Teacher, Class, Student, Schedule, Grade


class SubjectModelTest(TestCase):
    def test_create_subject(self):
        subject = Subject.objects.create(name="Математика", description="Алгебра")
        self.assertEqual(str(subject), "Математика")
        self.assertEqual(Subject.objects.count(), 1)

    def test_subject_name_unique(self):
        Subject.objects.create(name="Фізика")
        with self.assertRaises(Exception):
            Subject.objects.create(name="Фізика")


class ClassModelTest(TestCase):
    def test_create_class(self):
        school_class = Class.objects.create(name="10-А", year=2024)
        self.assertEqual(str(school_class), "10-А")


class TeacherModelTest(TestCase):
    def test_teacher_linked_to_subject(self):
        subject = Subject.objects.create(name="Історія")
        teacher = Teacher.objects.create(first_name="Іван", last_name="Петренко", subject=subject)
        self.assertEqual(teacher.subject, subject)
        self.assertIn(teacher, subject.teachers.all())


class StudentModelTest(TestCase):
    def test_student_linked_to_class(self):
        school_class = Class.objects.create(name="9-Б", year=2023)
        student = Student.objects.create(first_name="Олена", last_name="Коваль", school_class=school_class)
        self.assertEqual(student.school_class, school_class)


class ScheduleModelTest(TestCase):
    def test_schedule_creation(self):
        subject = Subject.objects.create(name="Біологія")
        school_class = Class.objects.create(name="8-В", year=2022)
        teacher = Teacher.objects.create(first_name="Марія", last_name="Шевченко", subject=subject)
        schedule = Schedule.objects.create(
            day_of_week="mon", start_time="08:30", subject=subject,
            school_class=school_class, teacher=teacher,
        )
        self.assertEqual(schedule.subject, subject)


class GradeModelTest(TestCase):
    def test_grade_creation(self):
        subject = Subject.objects.create(name="Хімія")
        school_class = Class.objects.create(name="7-Г", year=2021)
        student = Student.objects.create(first_name="Андрій", last_name="Бондар", school_class=school_class)
        grade = Grade.objects.create(student=student, subject=subject, grade=5, date="2024-10-01")
        self.assertEqual(grade.grade, 5)
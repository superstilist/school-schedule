from django.test import TestCase

from .models import Class, Student, Subject, Teacher


class SubjectModelTest(TestCase):
    def test_str_returns_name(self):
        subject = Subject.objects.create(name="Mathematics")
        self.assertEqual(str(subject), "Mathematics")


class TeacherModelTest(TestCase):
    def test_teacher_linked_to_subject(self):
        subject = Subject.objects.create(name="Physics")
        teacher = Teacher.objects.create(name="John Doe", subject=subject)
        self.assertEqual(teacher.subject, subject)
        self.assertIn(teacher, subject.teachers.all())


class ClassModelTest(TestCase):
    def test_str_returns_name(self):
        school_class = Class.objects.create(name="5-A", grade=5)
        self.assertEqual(str(school_class), "5-A")


class StudentModelTest(TestCase):
    def test_student_linked_to_class(self):
        school_class = Class.objects.create(name="6-B", grade=6)
        student = Student.objects.create(name="Jane Smith", school_class=school_class)
        self.assertEqual(student.school_class, school_class)
        self.assertIn(student, school_class.students.all())

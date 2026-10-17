from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва")
    description = models.TextField(blank=True, verbose_name="Опис")

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предмети"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Teacher(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Ім'я")
    last_name = models.CharField(max_length=50, verbose_name="Прізвище")
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="teachers", verbose_name="Предмет"
    )

    class Meta:
        verbose_name = "Вчитель"
        verbose_name_plural = "Вчителі"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Class(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name="Назва класу")
    year = models.PositiveIntegerField(verbose_name="Рік навчання")

    class Meta:
        verbose_name = "Клас"
        verbose_name_plural = "Класи"
        ordering = ["year", "name"]

    def __str__(self):
        return self.name


class Student(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Ім'я")
    last_name = models.CharField(max_length=50, verbose_name="Прізвище")
    school_class = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name="students", verbose_name="Клас"
    )

    class Meta:
        verbose_name = "Учень"
        verbose_name_plural = "Учні"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


DAYS_OF_WEEK = [
    ("mon", "Понеділок"),
    ("tue", "Вівторок"),
    ("wed", "Середа"),
    ("thu", "Четвер"),
    ("fri", "П'ятниця"),
    ("sat", "Субота"),
]


class Schedule(models.Model):
    day_of_week = models.CharField(
        max_length=3, choices=DAYS_OF_WEEK, verbose_name="День тижня"
    )
    start_time = models.TimeField(verbose_name="Година початку")
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="schedules", verbose_name="Предмет"
    )
    school_class = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name="schedules", verbose_name="Клас"
    )
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name="schedules", verbose_name="Вчитель"
    )

    class Meta:
        verbose_name = "Заняття в розкладі"
        verbose_name_plural = "Розклад"
        ordering = ["day_of_week", "start_time"]

    def __str__(self):
        return f"{self.get_day_of_week_display()} {self.start_time} - {self.subject} ({self.school_class})"


class Grade(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="grades", verbose_name="Учень"
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="grades", verbose_name="Предмет"
    )
    grade = models.PositiveSmallIntegerField(verbose_name="Оцінка")
    date = models.DateField(verbose_name="Дата")

    class Meta:
        verbose_name = "Оцінка"
        verbose_name_plural = "Оцінки"
        ordering = ["-date"]

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.grade} ({self.date})"
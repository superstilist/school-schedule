from django.db import models


class Subject(models.Model):
    """School subject (Предмет)."""

    name = models.CharField(max_length=100, verbose_name="Назва предмету")
    description = models.TextField(blank=True, verbose_name="Опис")

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предмети"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Teacher(models.Model):
    """Teacher (Вчитель). Linked to a subject via ForeignKey."""

    name = models.CharField(max_length=100, verbose_name="Ім'я вчителя")
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="teachers",
        verbose_name="Предмет",
    )

    class Meta:
        verbose_name = "Вчитель"
        verbose_name_plural = "Вчителі"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.subject})"


class Class(models.Model):
    """Class (Клас)."""

    name = models.CharField(max_length=50, verbose_name="Назва класу")
    grade = models.PositiveIntegerField(default=1, verbose_name="Паралель")

    class Meta:
        verbose_name = "Клас"
        verbose_name_plural = "Класи"
        ordering = ["grade", "name"]

    def __str__(self):
        return self.name


class Student(models.Model):
    """Student (Учень). Linked to a class via ForeignKey."""

    name = models.CharField(max_length=100, verbose_name="Ім'я учня")
    school_class = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name="students",
        verbose_name="Клас",
    )

    class Meta:
        verbose_name = "Учень"
        verbose_name_plural = "Учні"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.school_class})"

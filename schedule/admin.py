from django.contrib import admin

from .models import Subject, Teacher, Class, Student


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("name", "subject")
    list_filter = ("subject",)
    search_fields = ("name",)


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ("name", "grade")
    list_filter = ("grade",)
    search_fields = ("name",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "school_class")
    list_filter = ("school_class",)
    search_fields = ("name",)

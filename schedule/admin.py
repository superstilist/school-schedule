from django.contrib import admin

from .models import Subject, Teacher, Class, Student, Schedule, Grade


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "subject")
    list_filter = ("subject",)
    search_fields = ("first_name", "last_name")


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ("name", "year")
    search_fields = ("name",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "school_class")
    list_filter = ("school_class",)
    search_fields = ("first_name", "last_name")


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("day_of_week", "start_time", "subject", "school_class", "teacher")
    list_filter = ("day_of_week", "school_class", "subject")


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "grade", "date")
    list_filter = ("subject", "date")
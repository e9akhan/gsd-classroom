"""
    Module name :- admin
"""

from django.contrib import admin

from .models import (
    Faculty,
    Content,
    Program,
    Course,
    Student,
    Assignment,
    StudentAssignment,
)


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    """
    Faculty Admin class.
    """

    list_display = [
        "user",
        "github",
        "courses",
        "assignments",
        "assignments_graded",
        "is_active",
    ]

    def assignments(self, obj):
        """
        Assignments.
        """
        return obj.assignments()

    def assigments_graded(self, obj):
        """
        Assignments graded.
        """
        return obj.assignments_graded()

    def courses(self, obj):
        """
        Courses.
        """
        return obj.courses()


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    Student Admin.
    """

    list_display = ["user", "github", "is_active", "program", "grade"]

    def grade(self, obj):
        """
        Grade.
        """
        return obj.grade()


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    """
    Content Admin class.
    """

    list_display = ["name", "faculty", "repo", "assignments", "no_of_courses"]

    def assignments(self, obj):
        """
        Assignments.
        """
        return obj.assignments()

    def no_of_courses(self, obj):
        """
        No of courses.
        """
        return obj.courses()


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    """
    Program Admin class.
    """

    list_display = ["name", "start", "end", "no_of_courses", "no_of_students"]

    def no_of_courses(self, obj):
        """
        No of courses.
        """
        return obj.courses()

    def no_of_students(self, obj):
        """
        No of students.
        """
        return obj.students()


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Course Admin class.
    """

    list_display = ["name", "assignment", "assignment_full_checked"]

    def assignment(self, obj):
        """
        Assignment.
        """
        return obj.assignments()

    def assignment_full_checked(self, obj):
        """
        All assignment checked.
        """
        return obj.assignment_completed_and_graded_100()


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    """
    Assignment Admin class.
    """

    list_display = ["program", "course", "content", "due"]

    def student(self, obj):
        """
        Student.
        """
        return obj.students()


@admin.register(StudentAssignment)
class StudentAssignmentAdmin(admin.ModelAdmin):
    """
    Student Assignment Admin class.
    """

    list_display = ["student", "assignment", "reviewer", "grade", "submitted"]
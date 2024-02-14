"""
    Module name :- admin
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

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
        "courses",
        "assignments",
        "assignments_graded",
        "is_active",
    ]

    def assignments(self, obj):
        """
        Assignments.
        """
        url = "admin:voyage_assignment_change"
        assignments = obj.assignments()
        dropdown = "<ul>"

        for assignment in assignments:
            dropdown += f"""
            <li>
                <a href={reverse(url, kwargs={'object_id': assignment.id})}>
                    {assignment}
                </a>
            </li>
        """

        dropdown += "</ul>"
        return format_html(dropdown)

    def assignments_graded(self, obj):
        """
        Assignments graded.
        """
        url = "admin:voyage_studentassignment_change"
        assignments = obj.assignments_graded()
        dropdown = "<ul>"

        for assignment in assignments:
            dropdown += f"""
            <li>
                <a href={reverse(url, kwargs={'object_id': assignment.id})}>
                    {assignment}
                </a>
            </li>
        """

        dropdown += "</ul>"
        return format_html(dropdown)

    def courses(self, obj):
        """
        Courses.
        """
        url = "admin:voyage_course_change"
        courses = obj.courses()
        dropdown = "<ul>"

        for course in courses:
            dropdown += f"""
            <li>
                <a href={reverse(url, kwargs={'object_id': course.id})}>
                    {course}
                </a>
            </li>
        """

        dropdown += "</ul>"
        return format_html(dropdown)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    Student Admin.
    """

    list_display = [
        "user",
        "programs",
        "courses",
        "assignments",
        "assignments_submitted",
        "grade",
    ]

    def programs(self, obj):
        """
        Programs
        """
        url = "admin:voyage_program_change"
        program = obj.programs()
        return format_html(
            f"""
                <a href={reverse(url, kwargs={'object_id': program.id})}>
                    {program.name} 
                </a>
            """
        )

    def courses(self, obj):
        """
        Courses.
        """
        url = "admin:voyage_course_change"
        courses = obj.courses()

        dropdown = "<ul>"
        for course in courses:
            dropdown += f"""
            <li>
                <a href={reverse(url, kwargs={"object_id": course.id})}>
                    {course}
                </a>
            </li>
        """
        dropdown += "</ul>"

        return format_html(dropdown)

    def assignments(self, obj):
        """
        assignments.
        """
        url = "admin:voyage_studentassignment_change"
        assignments = obj.assignments()

        dropdown = "<ul>"
        for assignment in assignments:
            dropdown += f"""
            <li>
                <a href={reverse(url, kwargs={'object_id': assignment.id})}>
                    {assignment}
                </a>
            </li>
            """
        dropdown += "</ul>"

        return format_html(dropdown)

    def grade(self, obj):
        """
        Grade.
        """
        return obj.grade()

    def assignments_submitted(self, obj):
        """
        No of assignments submitted.
        """
        url = "admin:voyage_studentassignment_change"
        assignments = obj.assignments_submitted()

        dropdown = "<ul>"
        for assignment in assignments:
            dropdown += f"""
            <li>
                <a href={reverse(url, kwargs={"object_id": assignment.id})}>
                    {assignment}
                </a>
            </li>
        """
        dropdown += "</ul>"

        return format_html(dropdown)


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    """
    Content Admin class.
    """

    list_display = ["name", "faculty", "repo", "no_of_courses", "assignments"]

    def assignments(self, obj):
        """
        Assignments.
        """
        return obj.assignments().count()

    def no_of_courses(self, obj):
        """
        No of courses.
        """
        return obj.courses().count()


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
        return obj.courses().count()

    def no_of_students(self, obj):
        """
        No of students.
        """
        return obj.students().count()


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
        return obj.assignments().count()

    def assignment_full_checked(self, obj):
        """
        All assignment checked.
        """
        return len(obj.assignment_completed_and_graded_100())


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    """
    Assignment Admin class.
    """

    list_display = ["program", "course", "content", "due", "average"]

    def average(self, obj):
        """
        Average.
        """
        return obj.assignment_avg_grade()


@admin.register(StudentAssignment)
class StudentAssignmentAdmin(admin.ModelAdmin):
    """
    Student Assignment Admin class.
    """

    list_display = ["student", "assignment", "reviewer", "grade", "submitted"]

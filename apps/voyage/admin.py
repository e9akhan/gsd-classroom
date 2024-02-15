"""
    Module name :- admin
"""

from django.contrib import admin
from django.utils.html import format_html

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
        assignments = obj.assignments()
        if assignments:
            html = '<a href="/admin/voyage/assignment/?id__in='
            for assignment in assignments:
                html = "".join((html, f"{assignment.id},"))
            return format_html(html[:-1] + f'">{len(assignments)}</a>')
        return 0

    def assignments_graded(self, obj):
        """
        Assignments graded.
        """
        assignments = obj.assignments_graded()
        if assignments:
            html = '<a href="/admin/voyage/studentassignment/?id__in='
            for assignment in assignments:
                html = "".join((html, f"{assignment.id},"))
            return format_html(html[:-1] + f'">{len(assignments)}</a>')
        return 0

    def courses(self, obj):
        """
        Courses.
        """
        courses = obj.courses

        if courses:
            html = '<a href="/admin/voyage/course/?id__in='
            for course in courses:
                html = "".join((html, f"{course.id},"))
            return format_html(html[:-1] + f'">{len(courses)}</a>')
        return 0


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
        program = obj.programs()
        if program:
            html = f'<a href="/admin/voyage/program/{program.id}/change/'
            return format_html(html[:-1] + f'">{program}</a>')
        return 0

    def courses(self, obj):
        """
        Courses.
        """
        courses = obj.courses
        if courses:
            html = '<a href="/admin/voyage/course/?id__in='
            for course in courses:
                html = "".join((html, f"{course.id},"))
            return format_html(html[:-1] + f'">{len(courses)}</a>')
        return 0

    def assignments(self, obj):
        """
        assignments.
        """
        assignments = obj.assignments
        if assignments:
            html = '<a href="/admin/voyage/studentassignment/?id__in='
            for assignment in assignments:
                html = "".join((html, f"{assignment.id},"))
            return format_html(html[:-1] + f'">{len(assignments)}</a>')
        return 0

    def grade(self, obj):
        """
        Grade.
        """
        return obj.grade()

    def assignments_submitted(self, obj):
        """
        No of assignments submitted.
        """
        assignments = obj.assignments_submitted()
        if assignments:
            html = '<a href="/admin/voyage/studentassignment/?id__in='
            for assignment in assignments:
                html = "".join((html, f"{assignment.id},"))
            return format_html(html[:-1] + f'">{len(assignments)}</a>')
        return 0


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    """
    Content Admin class.
    """

    list_display = ["name", "facultys", "repo", "no_of_courses", "assignments"]

    def facultys(self, obj):
        """
        Faculty.
        """
        faculty = obj.faculty
        html = f'<a href="/admin/voyage/faculty/{faculty.id}/change/">{faculty}</a>'
        return format_html(html)

    def assignments(self, obj):
        """
        Assignments.
        """
        assignments = obj.assignments()
        if assignments:
            html = '<a href="/admin/voyage/assignment/?id__in='
            for assignment in assignments:
                html = "".join((html, f"{assignment.id},"))
            return format_html(html[:-1] + f'">{len(assignments)}</a>')
        return 0

    def no_of_courses(self, obj):
        """
        No of courses.
        """
        courses = obj.courses()
        if courses:
            html = '<a href="/admin/voyage/course/?id__in='
            for course in courses:
                html = "".join((html, f"{course.id},"))
            return format_html(html[:-1] + f'">{len(courses)}</a>')
        return 0


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
        courses = obj.courses()
        if courses:
            html = '<a href="/admin/voyage/course/?id__in='
            for course in courses:
                html = "".join((html, f"{course.id},"))
            return format_html(html[:-1] + f'">{len(courses)}</a>')
        return 0

    def no_of_students(self, obj):
        """
        No of students.
        """
        students = obj.students()
        if students:
            html = '<a href="/admin/voyage/student/?id__in='
            for student in students:
                html = "".join((html, f"{student.id},"))
            return format_html(html[:-1] + f'">{len(students)}</a>')
        return 0


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
        assignments = obj.assignments
        if assignments:
            html = '<a href="/admin/voyage/assignment/?id__in='
            for assignment in assignments:
                html = "".join((html, f"{assignment.id},"))
            return format_html(html[:-1] + f'">{len(assignments)}</a>')
        return 0

    def assignment_full_checked(self, obj):
        """
        All assignment checked.
        """
        assignments = obj.assignment_completed_and_graded_100()
        if assignments:
            html = '<a href="/admin/voyage/assignment/?id__in='
            for assignment in assignments:
                html = "".join((html, f"{assignment.id},"))
            return format_html(html[:-1] + f'">{len(assignments)}</a>')
        return 0


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    """
    Assignment Admin class.
    """

    list_display = ["program", "courses", "contents", "due", "average"]

    def average(self, obj):
        """
        Average.
        """
        return obj.assignment_avg_grade

    def courses(self, obj):
        """
        Courses.
        """
        course = obj.course
        html = f'<a href="/admin/voyage/course/{course.id}/change/">{course}</a>'
        return format_html(html)

    def contents(self, obj):
        """
        Contents.
        """
        content = obj.content
        html = f'<a href="/admin/voyage/content/{content.id}/change/">{content}</a>'
        return format_html(html)


@admin.register(StudentAssignment)
class StudentAssignmentAdmin(admin.ModelAdmin):
    """
    Student Assignment Admin class.
    """

    list_display = ["student", "assignments", "reviewers", "grade", "submitted"]

    def reviewers(self, obj):
        """
        Reviewer.
        """
        reviewer = obj.reviewer
        html = f'<a href="/admin/voyage/faculty/{reviewer.id}/change/">{reviewer}</a>'
        return format_html(html)

    def assignments(self, obj):
        """
        Assignment.
        """
        assignment = obj.assignment
        html = f'<a href="/admin/voyage/assignment/{assignment.id}/change/">{assignment}</a>'
        return format_html(html)

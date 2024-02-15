"""
    Module name :- appurls
"""

from django.urls import path

from apps.voyage.views.appviews import (
    FacultyDashboardView,
    StudentCoursesView,
    StudentAssignmentView,
    StudentSubmissionView,
    CreateNewCourse,
    CreateNewAssignment,
)


urlpatterns = [
    path("faculty/<int:id>/", FacultyDashboardView.as_view(), name="faculty_dashboard"),
    path("student/<int:id>/", StudentCoursesView.as_view(), name="student_dashboard"),
    path(
        "student/assignments/",
        StudentAssignmentView.as_view(),
        name="student_assignments",
    ),
    path(
        "student/submissions/",
        StudentSubmissionView.as_view(),
        name="student_submissions",
    ),
    path("course/new/", CreateNewCourse.as_view(), name="new_course"),
    path("assignment/new/", CreateNewAssignment.as_view(), name="new_assignment"),
]

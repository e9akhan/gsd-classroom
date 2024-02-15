"""
    Module name :- appviews.
"""

from django.views.generic import TemplateView, ListView
from django.shortcuts import redirect

from qux.seo.mixin import SEOMixin
from apps.voyage.models import Assignment, Faculty
from apps.voyage.forms import CourseForm, AssignmentForm


class VoyageDefaultView(SEOMixin, TemplateView):
    """
    VoyageDefaultView.
    """

    template_name = "voyage/index.html"


class FacultyDashboardView(ListView):
    """
    FacultyDashboardView.
    """

    template_name = "voyage/faculty_dashboard.html"

    def get_queryset(self):
        """
        Get queryset.
        """
        faculty_id = self.kwargs["id"]
        faculty = Faculty.objects.get(id=faculty_id)
        return faculty.courses


class StudentCoursesView(ListView):
    """
    StudentCoursesView.
    """

    template_name = "voyage/student_dashboard.html"

    def get_queryset(self):
        """
        Get queryset.
        """
        student_id = self.kwargs["id"]
        student = Faculty.objects.get(id=student_id)
        return student.courses


class StudentAssignmentView(ListView):
    """
    StudentAssignmentView.
    """

    template_name = "voyage/assignments.html"
    model = Assignment


class StudentSubmissionView(ListView):
    """
    StudentSubmissionView.
    """

    template_name = "voyage/submissions.html"
    model = Assignment


class CreateNewCourse(TemplateView):
    """
    CreateNewCourse.
    """

    template_name = "voyage/form.html"

    def post(self, request, *args, **kwargs):
        """
        Post method.
        """
        context = self.get_context_data()
        form = context["form"]

        if form.is_valid():
            form.save()
            return redirect("faculty_dashboard", id=2)
        return self.render_to_response(context=context)

    def get_context_data(self, **kwargs):
        """
        Get context data.
        """
        context = super().get_context_data(**kwargs)
        context["form"] = CourseForm(self.request.POST or None)
        context["title"] = "Create Course"
        return context


class CreateNewAssignment(TemplateView):
    """
    Create New Assignment.
    """

    template_name = "voyage/form.html"

    def post(self, request, *args, **kwargs):
        """
        Post method.
        """
        context = self.get_context_data()
        form = context["form"]

        if form.is_valid():
            form.save()
            return redirect("faculty_dashboard", id=2)
        return self.render_to_response(context=context)

    def get_context_data(self, **kwargs):
        """
        Get context data.
        """
        context = super().get_context_data(**kwargs)
        context["form"] = AssignmentForm(self.request.POST or None)
        context["title"] = "Create Assignment"
        return context

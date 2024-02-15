"""
    Module name :- forms.
"""

from django import forms

from apps.voyage.models import Course, Assignment


class CourseForm(forms.ModelForm):
    """
    Create a form.
    """

    class Meta:
        """
        Meta class.
        """

        model = Course
        fields = "__all__"

        widgets = {"name": forms.TextInput(attrs={"class": "form-control"})}


class AssignmentForm(forms.ModelForm):
    """
    Create a form.
    """

    class Meta:
        """
        Meta class.
        """

        model = Assignment
        fields = "__all__"

        widgets = {
            "program": forms.Select(attrs={"class": "form-select"}),
            "course": forms.Select(attrs={"class": "form-select"}),
            "content": forms.Select(attrs={"class": "form-select"}),
            "due": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "instructions": forms.Textarea(attrs={"class": "form-control"}),
            "rubric": forms.Textarea(attrs={"class": "form-control"}),
        }

"""
    Module name :- models
"""

import random
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.db import models
from qux.models import QuxModel


class Faculty(QuxModel):
    """
    Faculty Model.
    """

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    github = models.CharField(max_length=39, unique=True)
    is_active = models.BooleanField(default=True)

    def programs(self):
        """
        program().
        """
        students = [
            stu_assign.student for stu_assign in self.studentassignment_set.all()
        ]
        return {student.program for student in students}

    def assignments(self):
        """
        assignments.
        """
        return sum(content.assignments() for content in self.content_set.all())

    def courses(self):
        """
        courses.
        """
        return sum(content.courses() for content in self.content_set.all())

    def content(self, program=None, course=None):
        """
        Content.
        """

        if program and course:
            program_id, course_id = (
                Program.objects.filter(name=program)[0],
                Course.objects.filter(name=course)[0],
            )
            return [
                content
                for content in self.content_set.all()
                if content.assignment_set.all().filter(
                    program=program_id, course=course_id
                )
            ]

        if program:
            program_id = Program.objects.filter(name=program)[0]
            return [
                content
                for content in self.content_set.all()
                if content.assignment_set.all().filter(program=program_id)
            ]

        if course:
            course_id = Course.objects.filter(name=course)[0]
            return [
                content
                for content in self.content_set.all()
                if content.assignment_set.all().filter(course=course_id)
            ]

        return self.content_set.all()

    def assignments_graded(self, assignment=None):
        """
        Assignment graded.
        """
        query = self.studentassignment_set.all().exclude(grade=None)

        if assignment:
            return query.filter(assignment=assignment).count()
        return query.count()

    @classmethod
    def create_random_faculty(cls):
        """
        Create random faculty.
        """
        first_names = ["John", "David", "Vicky", "Victor", "Stephen"]
        last_names = ["Beckham", "Ceaser", "Watson", "McMahon", "Hawking"]

        user_model = get_user_model()

        user_list = []
        for i in range(5):
            first_name, last_name = first_names[i], last_names[i]

            user = user_model(
                username=first_name + last_name + "@123",
                first_name=first_name,
                last_name=last_name,
                email=first_name + "@gmail.com",
            )
            user.set_password(first_name + "@123")

            user_list.append(user)

        user_model.objects.bulk_create(user_list)

        users = list(user_model.objects.all())
        faculty_list = []

        for i in range(5):
            user = users[i]
            faculty = Faculty(user=user, github=user.first_name + "@github.com")
            faculty_list.append(faculty)

        cls.objects.bulk_create(faculty_list)

    def __str__(self):
        """
        String representation.
        """
        return self.user.username


class Program(QuxModel):
    """
    Example: Cohort-2
    """

    name = models.CharField(max_length=128)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        """
        String representation.
        """
        return self.name

    def students(self):
        """
        List of students in the program
        """
        return self.student_set.all().count()

    def courses(self):
        """
        No of courses.
        """
        return len({assignment.course for assignment in self.assignment_set.all()})

    @classmethod
    def create_random_programs(cls):
        """
        Create random programs.
        """
        programs = ["Entropy-1", "Entropy-2", "Entropy-3"]
        program_list = []

        for i in range(3):
            program = cls(
                name=programs[i],
                start=datetime.now() - timedelta(days=random.randint(31, 40)),
                end=datetime.now() + timedelta(days=random.randint(31, 40)),
            )
            program_list.append(program)

        cls.objects.bulk_create(program_list)


class Course(QuxModel):
    """
    Example: Python, or Django, or Logic
    """

    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        """
        String representation.
        """
        return self.name

    def programs(self):
        """
        Program.
        """
        return {assignment.program for assignment in self.assignment_set.all()}

    def students(self):
        """
        Students.
        """
        students = []

        for assignment in self.assignment_set.all():
            students += assignment.students()
        return set(students)

    def content(self):
        """
        Contents.
        """
        return {assignment.content for assignment in self.assignment_set.all()}

    def assignments(self):
        """
        No of assignments.
        """
        return self.assignment_set.all().count()

    def assignment_completed_and_graded_100(self):
        """
        No of assignments completed and graded 100%.
        """
        return len(
            [
                assignment
                for assignment in self.assignment_set.all()
                if assignment.is_assignment_submitted_graded_100()
            ]
        )

    @classmethod
    def create_random_courses(cls):
        """
        Create random courses.
        """
        names = ["Cohort-1", "Cohort-2", "Cohort-3"]

        for i in range(3):
            cls.objects.create(name=names[i])


class Content(QuxModel):
    """
    Meta information related to a GitHub repo
    """

    name = models.CharField(max_length=128)
    faculty = models.ForeignKey(Faculty, on_delete=models.DO_NOTHING)
    repo = models.URLField(max_length=240, unique=True)

    class _Meta:
        """
        Meta class.
        """

        verbose_name = "Content"
        verbose_name_plural = "Content"

    def courses(self):
        """
        No of courses.
        """
        return len({assignment.course for assignment in self.assignment_set.all()})

    def assignments(self):
        """
        No of assignments.
        """
        return self.assignment_set.all().count()

    @classmethod
    def create_random_contents(cls):
        """
        Create random contents.
        """
        contents = ["Math-" + str(i) for i in range(1, 29)]
        faculties = list(Faculty.objects.all())
        content_list = []

        for i in range(28):
            content = cls(
                name=contents[i],
                faculty=random.choice(faculties),
                repo="https://github.com/" + contents[i],
            )
            content_list.append(content)

        cls.objects.bulk_create(content_list)

    def __str__(self):
        """
        String representation.
        """
        return self.name


class Student(QuxModel):
    """
    Student model.
    """

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    github = models.CharField(max_length=39, unique=True)
    is_active = models.BooleanField(default=True)
    program = models.ForeignKey(Program, on_delete=models.DO_NOTHING)

    def programs(self):
        """
        Programs.
        """
        return self.program.name

    def courses(self):
        """
        Number of courses.
        """
        return self.program.courses()

    def assignments(self):
        """
        No of assignments.
        """
        return self.studentassignment_set.all().count()

    def assignments_submitted(self, assignment=None):
        """
        No of assignments submitted.
        """
        query = self.studentassignment_set.all().exclude(submitted=None)
        if assignment:
            return query.filter(assignment=assignment)

        return query

    def assignments_not_submitted(self, assignment=None):
        """
        Assignments not submitted.
        """
        query = self.studentassignment_set.all().filter(submitted=None)

        if assignment:
            return query.filter(assignment=assignment)

        return query

    def assignments_graded(self, assignment=None):
        """
        No of assignments.
        """
        query = self.studentassignment_set.all().exclude(grade=None)

        if assignment:
            return query.filter(assignment=assignment)

        return query

    def grade(self):
        """
        Avg grade of a student.
        """
        grades = [assignment.grade for assignment in self.assignments_graded()]

        total_assignment_submitted = len(self.assignments_submitted())
        return (
            sum(grades) / total_assignment_submitted
            if total_assignment_submitted
            else 0
        )

    @classmethod
    def create_random_students(cls):
        """
        Create random students.
        """
        names = [
            "Akash",
            "Akbar",
            "Shivansh",
            "Gaurav",
            "Kunal",
            "Khizar",
            "Ankit",
            "Arjun",
            "Priti",
            "David",
        ]

        user_model = get_user_model()
        user_list = []

        for i in range(10):
            name = names[i]
            user = user_model(
                username=name + "@123",
                email=name + "@example.com",
            )
            user.set_password(name + "@123")

            user_list.append(user)

        user_model.objects.bulk_create(user_list)

        programs = list(Program.objects.all())
        users = list(user_model.objects.all())
        student_list = []

        for i in range(10):
            program = random.choice(programs)
            student = cls(
                user=users[i + 5],
                github=names[i] + "@github.com",
                program=program,
            )
            student_list.append(student)

        cls.objects.bulk_create(student_list)

    def __str__(self):
        """
        String representation.
        """
        return self.user.username


class Assignment(QuxModel):
    """
    Assignment Model.
    """

    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    due = models.DateTimeField()
    instructions = models.TextField()
    rubric = models.TextField()

    class Meta:
        """
        Meta class.
        """

        unique_together = ["program", "course", "content"]

    def __str__(self):
        """
        String representation.
        """
        return self.content.name

    def students(self):
        """
        Students.
        """
        return {stu_assign.student for stu_assign in self.studentassignment_set.all()}

    def submissions(self, graded=None):
        """
        Return a queryset of submissions that are either all, graded, or not graded.
        """
        query = self.studentassignment_set.all()
        if graded:
            return query.exclude(grade=None)

        if graded is False:
            return query.filter(grade=None)

        return query

    def is_assignment_submitted_graded_100(self):
        """
        Is assignment completed or graded 100%
        """
        total_assignments = self.studentassignment_set.all().count()
        query = (
            self.studentassignment_set.all().exclude(submitted=None).exclude(grade=None)
        )
        return total_assignments == query.count()

    @classmethod
    def create_random_assignments(cls):
        """
        Create random assignments.
        """
        programs = list(Program.objects.all())
        courses = list(Course.objects.all())
        contents = list(Content.objects.all())
        assignment_list = []

        for i in range(5):
            assignment = cls(
                program=random.choice(programs),
                course=random.choice(courses),
                content=contents[i],
                due=datetime.now() + timedelta(days=random.randint(2, 7)),
                instructions="Please complete the assignment before due date",
                rubric="Nothing",
            )
            assignment_list.append(assignment)

        cls.objects.bulk_create(assignment_list)


class StudentAssignment(QuxModel):
    """
    Student assignment
    """

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    grade = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=None,
        null=True,
        blank=True,
    )
    submitted = models.DateTimeField(default=None, null=True, blank=True)
    reviewed = models.DateTimeField(default=None, null=True, blank=True)
    reviewer = models.ForeignKey(
        Faculty, on_delete=models.DO_NOTHING, default=None, null=True, blank=True
    )
    feedback = models.TextField(default=None, null=True, blank=True)

    @classmethod
    def create_random_student_assignments(cls):
        """
        Create random student assignments.
        """
        students = list(Student.objects.all())
        assignments = list(Assignment.objects.all())
        reviewers = list(Faculty.objects.all())
        student_assignments = []

        for _ in range(10):
            student_assignment = cls(
                student=random.choice(students),
                assignment=random.choice(assignments),
                reviewer=random.choice(reviewers),
            )
            student_assignments.append(student_assignment)

        cls.objects.bulk_create(student_assignments)

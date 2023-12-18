from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

from datetime import date

from django.db import models


class Student(models.Model):
    # Choices for student status
    STUDENT_STATUS_CHOICES = [
        ('ER', 'Enrolled'),
        ('SP', 'Suspended'),
        ('GD', 'Graduated'),
    ]

    # Student details

    date_of_birth = models.DateField()
    status = models.CharField(max_length=10, choices=STUDENT_STATUS_CHOICES, default='ER')
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.user.first_name}"


class Category(models.Model):
    # Category details
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    # Course details
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey('Instructor', on_delete=models.CASCADE,
                                   related_name='courses_instructed')
    # Relationship with Category
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # Relationship with Student
    students = models.ManyToManyField(Student, blank=True)
    interested = models.PositiveIntegerField(default=0)
    # Course schedule details
    start_date = models.DateField()
    end_date = models.DateField()
    # Pricing details
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Course level details
    COURSE_LEVEL_CHOICES = [
        ('BE', 'Beginner'),
        ('IN', 'Intermediate'),
        ('AD', 'Advanced'),
    ]
    level = models.CharField(max_length=2, choices=COURSE_LEVEL_CHOICES)
    levels = models.PositiveIntegerField(
        default=1,  # You can set the default value as needed
    )

    def __str__(self):
        return self.title


class Instructor(models.Model):
    # Instructor details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField()

    # Relationship with student
    students_mentored = models.ManyToManyField(Student)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Instructor"


class Order(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    ORDER_STATUS_CHOICES = [
        (0, 'Order Confirmed'),
        (1, 'Order Cancelled'),
    ]
    order_status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=1)

    order_date = models.DateField(default=date.today)
    order_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    levels = models.PositiveIntegerField(default=1)

    def __str__(self):
        return (f"Order #{self.id} - {self.student.user.first_name} "
                f"{self.student.user.last_name} - {self.course.title}")

    def discount(self):
        original_price = Decimal(self.course.price)  # Convert to Decimal
        discount_amount = original_price * Decimal('0.10')
        discounted_price = original_price - discount_amount

        self.order_price = discounted_price
        self.save()

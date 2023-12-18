from decimal import Decimal

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .forms import OrderForm, InterestForm
from .models import Category, Course, Instructor, Student
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
import datetime


# @login_required()
def index(request):
    # Get up to 5 categories
    category_list = Category.objects.all().order_by('id')[:10]

    # Get up to 5 courses sorted by descending order of price
    course_list = Course.objects.all().order_by('-price')

    response = HttpResponse()
    user_visits = request.COOKIES.get('user_visits')
    last_login_info = request.session.get('last_login_info')

    if last_login_info:
        # If last_login_info exists in session, display this value
        message = f'Your last login was at: {last_login_info}'
    else:
        # If last_login_info doesn't exist or has expired, display the message
        message = 'Your last login was more than 5 minutes ago'
    return render(request, 'myappF23/index.html', {'category_list': category_list, 'course_list': course_list,
                                                   'user_visits': user_visits,
                                                   'message': message})


def about(request):
    # Check if the 'user_visits' cookie exists
    user_visits = request.COOKIES.get('user_visits')
    if user_visits:
        # If the cookie exists, retrieve the value and increment by 1
        user_visits = int(user_visits) + 1

    else:
        # If the cookie does not exist, set the value to 1
        user_visits = 1

    # Store the updated information in a cookie and set it to expire after 10 seconds
    response = render(request, 'myappF23/about.html', {'user_visits': user_visits})
    response.set_cookie('user_visits', user_visits, max_age=5)

    return response


def detail(request, category_no):
    category = get_object_or_404(Category, id=category_no)
    # courses = category.course_set.all()
    courses = Course.objects.filter(category__name=category)
    return render(request, 'myappF23/detail.html', {'category': category, 'courses': courses})


def instructor_detail(request, instructor_id):
    # Get the instructor or return a 404 response if not found
    instructor = get_object_or_404(Instructor, id=instructor_id)

    # Get the courses instructed by the instructor
    courses_taught = instructor.courses_instructed.all()

    # Get the students mentored by the instructor
    students_mentored = instructor.students_mentored.all()

    # Render the instructor_detail.html template with the instructor, courses, and students
    return render(request, 'myappF23/instructor.html', {
        'instructor': instructor,
        'courses_taught': courses_taught,
        'students_mentored': students_mentored,
    })


def courses(request):
    courselist = Course.objects.all().order_by('id')
    return render(request, 'myappF23/courses.html', {
        'courselist': courselist
    })


def place_order(request):
    msg = ''
    courselist = Course.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            course = order.course

            # Check if the ordered levels exceed the maximum allowed for the course
            if order.levels > course.levels:
                msg = 'You exceeded the number of levels for this course.'

            else:
                # Check if the course price is greater than $150.00 and apply discount
                if course.price > Decimal('150.00'):
                    order.discount()
                else:

                    order.order_price = course.price
                order.save()
                msg = 'Your course has been ordered successfully.'
            return render(request, 'myappF23/order_response.html', {'msg': msg})

        else:
            msg = 'Form validation failed.'
    else:
        form = OrderForm()

    return render(request, 'myappF23/placeorder.html',
                  {'form': form, 'msg': msg, 'courselist': courselist})


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        form = InterestForm(request.POST)

        if form.is_valid():
            interested = form.cleaned_data['interested']
            if interested == 1:
                student = request.user.student
                # Check if the student is already interested in the course
                if not course.students.filter(id=student.id).exists():
                    course.students.add(student)
                    course.interested += 1
                    selected_levels = form.cleaned_data['levels']
                    course.levels = selected_levels
                    course.save()
                    return redirect('myappF23:index')

    else:
        form = InterestForm()

    return render(request, 'myappF23/coursedetail.html', {'course': course, 'form': form})


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                # Generate the date and time of the current login
                current_login_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # Store this value as a session parameter (last_login__info).
                request.session['last_login_info'] = current_login_time
                # Set the session expiry to 5 minutes
                request.session.set_expiry(300)  # 300 seconds = 5 minutes

                response = HttpResponseRedirect(reverse('myappF23:index'))

                # response.set_cookie('cookie_test','cookie_test=5')
                response.set_cookie('test_cookie', 'test_value')
                return response
            else:
                return HttpResponse("Your account is disabled")
        else:
            return HttpResponse("Invalid login details")
    else:
        return render(request, 'myappF23/login.html')


def user_logout(request):
    # Clear session data
    request.session.clear()

    # Set the session expiry to 0 (to delete the session)
    request.session.set_expiry(0)

    response = HttpResponseRedirect(reverse('myappF23:index'))

    # Set the max_age of the session cookie to a negative value (to delete the cookie)
    response.set_cookie('test_cookie', 'test_value', max_age=-1)

    return response


@login_required
def myaccount(request):
    user = request.user
    test_cookie_value = request.COOKIES.get('test_cookie')
    if hasattr(user, 'student'):
        student = user.student

        # Get all courses ordered by the student
        courses_ordered = Course.objects.filter(order__student=student)

        # Get all courses interested in by the student
        courses_interested = Course.objects.filter(students=student)

        context = {
            'full_name': f"{student.user.first_name} {student.user.last_name}",
            'courses_ordered': courses_ordered,
            'courses_interested': courses_interested,
        }
        # If 'test_cookie' is present, delete it
        if test_cookie_value:
            response = render(request, 'myappF23/myaccount.html', context)
            response.delete_cookie('test_cookie')
            return response

        return render(request, 'myappF23/myaccount.html', context)
    else:
        return redirect('myappF23:custom_login')


def custom_login(request):
    if request.user.is_authenticated:
        # Redirect authenticated users to the desired page
        return HttpResponseRedirect(reverse('myappF23:index'))
    else:
        # Render the login form
        return render(request, 'myappF23/custom_login.html')

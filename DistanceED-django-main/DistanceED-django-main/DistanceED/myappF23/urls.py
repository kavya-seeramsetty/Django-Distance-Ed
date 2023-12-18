from django.urls import path
from myappF23 import views

app_name = 'myappF23'

urlpatterns = [path('', views.user_login, name='login'),
               path('index/', views.index, name='index'),
               path(r'about/', views.about, name='about'),
               path('detail/<int:category_no>/', views.detail, name='detail'),
               path('instructor/<int:instructor_id>/', views.instructor_detail, name='instructor_detail'),
               path('courses/', views.courses, name='courses'),
               path('placeorder/', views.place_order, name='placeorder'),
               path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
               path('user_logout/', views.user_logout, name='logout'),
               path('myaccount/', views.myaccount, name='myaccount'),
               path('custom_login/', views.custom_login, name='custom_login'),

               ]

from django.urls import path
from .views import DashboardAPIView, StudentAPIView, StudentListAPIView

urlpatterns = [
    path('dashboard/', DashboardAPIView.as_view()),  # Total schools, classes, students count
    path('students/create', StudentAPIView.as_view()),  # Create Student
    path('students/<int:student_id>/', StudentAPIView.as_view()),  # Update Student
    path('students/list/', StudentListAPIView.as_view()),  # List all students with count
]

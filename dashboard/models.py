from django.db import models

class Student(models.Model):
    school_name = models.CharField(max_length=255)  
    student_class = models.CharField(max_length=100) 
    name = models.CharField(max_length=100)
    age = models.IntegerField()

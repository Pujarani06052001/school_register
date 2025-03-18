from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from .models import Student
from .serializers import StudentSerializer
class DashboardAPIView(APIView):
    def get(self, request):
        students = Student.objects.all()

        total_students = students.count()
        student_names = students.values_list("name", flat=True)

        total_schools = students.values_list("school_name", flat=True).distinct()
        total_classes = students.values_list("student_class", flat=True).distinct()

        return Response({
            "total_schools": {
                "count": len(total_schools),
                "names": list(total_schools)
            },
            "total_classes": {
                "count": len(total_classes),
                "names": list(total_classes)
            },
            "total_students": {
                "count": total_students,
                "names": list(student_names)
            }
        }, status=status.HTTP_200_OK)

class StudentAPIView(APIView):
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Student added successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Student updated successfully!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentListAPIView(APIView):
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        total_students = students.count()

        return Response({
            "total_students": total_students,
            "students": serializer.data
        }, status=status.HTTP_200_OK)

from rest_framework import generics
from .models import Employee,Branch,Department
from .serializers import EmployeeSerializer, BranchSerializer,DepartmentSerializer
from django.db.models import Count
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import render

class EmployeeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class BranchListCreateAPIView(generics.ListCreateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [AllowAny]

class BranchDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [AllowAny]


class BranchEmployeesAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, pk):

        employees = Employee.objects.filter(branch_id=pk)

        serializer = EmployeeSerializer(
            employees,
            many=True
        )

        return Response(serializer.data)
    
class BranchStatisticsAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        branches = Branch.objects.annotate(
            total_employees=Count("employees")
        )

        data = []

        for branch in branches:

            data.append({

                "id": branch.id,

                "branch_name": branch.branch_name,

                "branch_code": branch.branch_code,

                "total_employees": branch.total_employees

            })

        return Response(data)


class DepartmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Department.objects.select_related("branch")
    serializer_class = DepartmentSerializer
    permission_classes = [AllowAny]


class DepartmentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.select_related("branch")
    serializer_class = DepartmentSerializer
    permission_classes = [AllowAny]


class DepartmentEmployeesAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, pk):

        employees = Employee.objects.filter(
            department_id=pk
        ).select_related(
            "branch",
            "department",
            "job_title"
        )

        serializer = EmployeeSerializer(
            employees,
            many=True
        )

        return Response(serializer.data)

class home(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, 'genmanagerhr.html')

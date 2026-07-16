from rest_framework import generics
from .models import Employee,Branch,Department
from .serializers import EmployeeSerializer, BranchSerializer,DepartmentSerializer
from django.db.models import Count
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import render, redirect
from .models import LeaveRequest, LeaveStatus, Survey

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
        return redirect('/genmanagerdash/')
    



def branch_hr_dashboard(request):
    return render(request, "branchhrmanager.html")


def employee_dashboard(request):
    return render(request, "employeedash.html")
    

def genmanagerdash(request):
    """Render the General Manager HR dashboard with basic aggregated metrics.

    Uses available models to compute sensible defaults. Where domain-specific
    metrics are not present, placeholders are provided so the template can
    safely render.
    """
    total_employees = Employee.objects.count()
    open_issues = LeaveRequest.objects.filter(status=LeaveStatus.PENDING).count()
    total_branches = Branch.objects.count()
    active_surveys = Survey.objects.filter(status='ACTIVE').count()

    context = {
        'total_employees': total_employees,
        'open_issues': open_issues,
        'escalated_to_executive': 12,
        'hrbp_response_velocity': '42.5',
        'engagement_index': 89,
        'systemic_flags': 2,
        'total_branches': total_branches,
        'active_surveys': active_surveys,
        # Donut breakdown (percent integers)
        'grievance_breakdown': [50, 30, 20],
    }

    return render(request, 'genmanagerdash.html', context)



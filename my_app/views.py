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

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token




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


@login_required(login_url='/login/')
def employee_dashboard(request):
    user = request.user
    try:
        profile = user.profile
    except Exception:
        profile = None

    welcome_name = user.get_full_name().strip() or user.username
    role_display = profile.role if profile and profile.role else getattr(user, 'role', 'Employee').replace('_', ' ').title()
    branch_display = profile.branch if profile and profile.branch else getattr(user, 'branch_name', 'Main Branch')

    context = {
        'welcome_name': welcome_name,
        'profile_role': role_display,
        'profile_branch': branch_display,
    }

    return render(request, 'employeedash.html', context)
    

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

     #code about login

@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'error': 'Please provide both username and password.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(username=username, password=password)

    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        is_employee = user.groups.filter(name='Employee').exists()
        role = 'employee' if is_employee else 'regular'
        redirect_url = '/employeedash/' if is_employee else '/genmanagerdash/'

        return Response(
            {
                'message': 'Login successful',
                'token': token.key,
                'role': role,
                'redirect_url': redirect_url,
            },
            status=status.HTTP_200_OK,
        )

    return Response(
        {'error': 'Invalid username or password. Please try again.'},
        status=status.HTTP_400_BAD_REQUEST,
    )


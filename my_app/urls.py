from django.urls import path
from .views import (
    EmployeeListCreateAPIView,
    EmployeeRetrieveUpdateDeleteAPIView,
    BranchListCreateAPIView,
    BranchDetailAPIView,
    BranchEmployeesAPIView,
    BranchStatisticsAPIView,
    DepartmentListCreateAPIView,
    DepartmentDetailAPIView,
    DepartmentEmployeesAPIView,
)

urlpatterns = [
    path("employees/", EmployeeListCreateAPIView.as_view(), name="employee-list"),
    path(
        "employees/<uuid:pk>/",
        EmployeeRetrieveUpdateDeleteAPIView.as_view(),
        name="employee-detail",
    ),

    path(
        "branches/",
        BranchListCreateAPIView.as_view(),
        name="branches"
    ),

    path(
        "branches/statistics/",
        BranchStatisticsAPIView.as_view(),
        name="branch-statistics"
    ),

    path(
        "branches/<uuid:pk>/",
        BranchDetailAPIView.as_view(),
        name="branch-detail"
    ),

    path(
        "branches/<uuid:pk>/employees/",
        BranchEmployeesAPIView.as_view(),
        name="branch-employees"
        
    ),

    path(
    "departments/",
    DepartmentListCreateAPIView.as_view(),
    name="department-list"
),

    path(
    "departments/<uuid:pk>/",
    DepartmentDetailAPIView.as_view(),
    name="department-detail"
),

    path(
    "departments/<uuid:pk>/employees/",
    DepartmentEmployeesAPIView.as_view(),
    name="department-employees"
),

]

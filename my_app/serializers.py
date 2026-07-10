from rest_framework import serializers
from .models import Employee,Branch,Department

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"

        from rest_framework import serializers
from .models import Branch, Employee


class BranchSerializer(serializers.ModelSerializer):
    employee_count = serializers.SerializerMethodField()

    class Meta:
        model = Branch
        fields = "__all__"

    def get_employee_count(self, obj):
        return Employee.objects.filter(branch=obj).count()
    
class DepartmentSerializer(serializers.ModelSerializer):
    employee_count = serializers.SerializerMethodField()
    branch_name = serializers.CharField(source="branch.branch_name", read_only=True)

    class Meta:
        model = Department
        fields = "__all__"

    def get_employee_count(self, obj):
        return obj.employees.count()
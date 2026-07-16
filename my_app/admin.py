from django.contrib import admin

from .admin_site import hr_admin_site
from .models import (
	Branch, Department, JobTitle, EmploymentType, Employee,
	Attendance, LeaveType, LeaveRequest, PerformanceReview,
	Announcement, Survey, SurveyQuestion, SurveyResponse,
	Recognition, Suggestion, Complaint, EmployeeDocument,
	Notification, AuditLog,
)



@admin.register(Branch, site=hr_admin_site)
class BranchAdmin(admin.ModelAdmin):
	list_display = ('branch_code', 'branch_name', 'city', 'district', 'status')
	search_fields = ('branch_code', 'branch_name', 'city', 'district')
	list_filter = ('status', 'city', 'district')


@admin.register(Department, site=hr_admin_site)
class DepartmentAdmin(admin.ModelAdmin):
	list_display = ('department_name', 'branch', 'status')
	search_fields = ('department_name', 'branch__branch_name', 'branch__branch_code')
	list_filter = ('status', 'branch')


@admin.register(JobTitle, site=hr_admin_site)
class JobTitleAdmin(admin.ModelAdmin):
	list_display = ('title', 'grade')
	search_fields = ('title', 'grade')


@admin.register(EmploymentType, site=hr_admin_site)
class EmploymentTypeAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('name',)


@admin.register(Employee, site=hr_admin_site)
class EmployeeAdmin(admin.ModelAdmin):
	list_display = ('employee_number', 'first_name', 'last_name', 'branch', 'department', 'employment_status')
	search_fields = ('employee_number', 'first_name', 'last_name', 'user__username', 'email')
	list_filter = ('employment_status', 'branch', 'department', 'employment_type', 'gender', 'marital_status')


@admin.register(Attendance, site=hr_admin_site)
class AttendanceAdmin(admin.ModelAdmin):
	list_display = ('employee', 'date', 'check_in', 'check_out', 'attendance_status')
	search_fields = ('employee__employee_number', 'employee__first_name', 'employee__last_name')
	list_filter = ('attendance_status', 'date')


@admin.register(LeaveType, site=hr_admin_site)
class LeaveTypeAdmin(admin.ModelAdmin):
	list_display = ('name', 'days_allowed')
	search_fields = ('name',)


@admin.register(LeaveRequest, site=hr_admin_site)
class LeaveRequestAdmin(admin.ModelAdmin):
	list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'status', 'approved_by')
	search_fields = ('employee__employee_number', 'employee__first_name', 'employee__last_name', 'leave_type__name')
	list_filter = ('status', 'leave_type', 'start_date', 'end_date')


@admin.register(PerformanceReview, site=hr_admin_site)
class PerformanceReviewAdmin(admin.ModelAdmin):
	list_display = ('employee', 'review_period', 'overall_score', 'review_date')
	search_fields = ('employee__employee_number', 'employee__first_name', 'employee__last_name', 'review_period')
	list_filter = ('review_period', 'review_date')


@admin.register(Announcement, site=hr_admin_site)
class AnnouncementAdmin(admin.ModelAdmin):
	list_display = ('title', 'posted_by', 'target_branch', 'publish_date', 'expiry_date')
	search_fields = ('title', 'message')
	list_filter = ('target_branch', 'publish_date', 'expiry_date')


@admin.register(Survey, site=hr_admin_site)
class SurveyAdmin(admin.ModelAdmin):
	list_display = ('title', 'status', 'anonymous', 'created_by', 'start_date', 'end_date')
	search_fields = ('title', 'description')
	list_filter = ('status', 'anonymous', 'created_by')


@admin.register(SurveyQuestion, site=hr_admin_site)
class SurveyQuestionAdmin(admin.ModelAdmin):
	list_display = ('survey', 'question_type', 'required')
	search_fields = ('survey__title', 'question')
	list_filter = ('question_type', 'required')


@admin.register(SurveyResponse, site=hr_admin_site)
class SurveyResponseAdmin(admin.ModelAdmin):
	list_display = ('survey', 'question', 'employee', 'submitted_at')
	search_fields = ('survey__title', 'question__question', 'employee__employee_number', 'answer')
	list_filter = ('survey', 'submitted_at')


@admin.register(Recognition, site=hr_admin_site)
class RecognitionAdmin(admin.ModelAdmin):
	list_display = ('title', 'employee', 'awarded_by', 'award_date')
	search_fields = ('title', 'employee__employee_number', 'employee__first_name', 'employee__last_name')
	list_filter = ('award_date',)


@admin.register(Suggestion, site=hr_admin_site)
class SuggestionAdmin(admin.ModelAdmin):
	list_display = ('subject', 'employee', 'status', 'submitted_at')
	search_fields = ('subject', 'description', 'employee__employee_number')
	list_filter = ('status', 'submitted_at')


@admin.register(Complaint, site=hr_admin_site)
class ComplaintAdmin(admin.ModelAdmin):
	list_display = ('category', 'employee', 'status', 'assigned_to', 'submitted_at')
	search_fields = ('category', 'description', 'employee__employee_number')
	list_filter = ('status', 'assigned_to', 'submitted_at')


@admin.register(EmployeeDocument, site=hr_admin_site)
class EmployeeDocumentAdmin(admin.ModelAdmin):
	list_display = ('title', 'employee', 'document_type', 'uploaded_at')
	search_fields = ('title', 'document_type', 'employee__employee_number')
	list_filter = ('document_type', 'uploaded_at')


@admin.register(Notification, site=hr_admin_site)
class NotificationAdmin(admin.ModelAdmin):
	list_display = ('title', 'recipient', 'notification_type', 'is_read', 'created_at')
	search_fields = ('title', 'message', 'recipient__username')
	list_filter = ('notification_type', 'is_read', 'created_at')


@admin.register(AuditLog, site=hr_admin_site)
class AuditLogAdmin(admin.ModelAdmin):
	list_display = ('created_at', 'user', 'action', 'model_name', 'record_id', 'ip_address')
	search_fields = ('user__username', 'action', 'model_name', 'record_id', 'description', 'ip_address')
	list_filter = ('created_at', 'model_name', 'action')
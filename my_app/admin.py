from django.contrib import admin
from .models import (
	Branch, Department, JobTitle, EmploymentType, Employee,
	Attendance, LeaveType, LeaveRequest, PerformanceReview,
	Announcement, Survey, SurveyQuestion, SurveyResponse,
	Recognition, Suggestion, Complaint, EmployeeDocument,
	Notification, AuditLog,
)


admin.site.register(Branch)
admin.site.register(Department)
admin.site.register(JobTitle)
admin.site.register(EmploymentType)
admin.site.register(Employee)
admin.site.register(Attendance)
admin.site.register(LeaveType)
admin.site.register(LeaveRequest)
admin.site.register(PerformanceReview)
admin.site.register(Announcement)
admin.site.register(Survey)
admin.site.register(SurveyQuestion)
admin.site.register(SurveyResponse)
admin.site.register(Recognition)
admin.site.register(Suggestion)
admin.site.register(Complaint)
admin.site.register(EmployeeDocument)
admin.site.register(Notification)
admin.site.register(AuditLog)
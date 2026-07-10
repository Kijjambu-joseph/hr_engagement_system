import uuid
from django.db import models
from django.conf import settings
from django.core.validators import (
    EmailValidator,
    RegexValidator,
    MinValueValidator,
    MaxValueValidator,
)


class TimeStampedModel(models.Model):
    """Abstract base model that provides `created_at` and `updated_at` timestamps.

    All business models inherit from this to ensure consistent audit timestamps.
    """

    created_at = models.DateTimeField(auto_now_add=True, help_text="Record creation timestamp")
    updated_at = models.DateTimeField(auto_now=True, help_text="Record last updated timestamp")

    class Meta:
        abstract = True


class BranchStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    INACTIVE = 'INACTIVE', 'Inactive'


phone_validator = RegexValidator(r'^\+?[0-9\-\s]{7,20}$', 'Enter a valid phone number.')


class Branch(TimeStampedModel):
    """Master table representing a bank branch.

    Indexes: `branch_code`, `email` for faster lookups.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch_code = models.CharField(max_length=20, unique=True, help_text="Unique branch code")
    branch_name = models.CharField(max_length=200, help_text="Branch display name")
    address = models.TextField(blank=True, help_text="Full postal address for the branch")
    city = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=30, validators=[phone_validator], blank=True)
    email = models.EmailField(blank=True, validators=[EmailValidator()])
    status = models.CharField(max_length=10, choices=BranchStatus.choices, default=BranchStatus.ACTIVE)

    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branches"
        ordering = ['branch_name']
        indexes = [
            models.Index(fields=['branch_code']),
            models.Index(fields=['email']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.branch_name} ({self.branch_code})"


class DepartmentStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    INACTIVE = 'INACTIVE', 'Inactive'


class Department(TimeStampedModel):
    """Department within a branch."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name='departments')
    department_name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=DepartmentStatus.choices, default=DepartmentStatus.ACTIVE)

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        ordering = ['department_name']
        indexes = [models.Index(fields=['branch', 'department_name'])]

    def __str__(self):
        return f"{self.department_name} - {self.branch.branch_code}"


class JobTitle(TimeStampedModel):
    """Job title master data."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150)
    grade = models.CharField(max_length=50, blank=True, help_text="Pay/grade band")
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Job Title"
        verbose_name_plural = "Job Titles"
        ordering = ['title']

    def __str__(self):
        return f"{self.title} {f'({self.grade})' if self.grade else ''}".strip()


class EmploymentType(TimeStampedModel):
    """Employment type (full-time, part-time, contract, etc.)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Employment Type"
        verbose_name_plural = "Employment Types"
        ordering = ['name']

    def __str__(self):
        return self.name


class Gender(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'
    OTHER = 'O', 'Other/Prefer not to say'


class MaritalStatus(models.TextChoices):
    SINGLE = 'SINGLE', 'Single'
    MARRIED = 'MARRIED', 'Married'
    DIVORCED = 'DIVORCED', 'Divorced'
    WIDOWED = 'WIDOWED', 'Widowed'


class EmploymentStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    RESIGNED = 'RESIGNED', 'Resigned'
    TERMINATED = 'TERMINATED', 'Terminated'
    RETIRED = 'RETIRED', 'Retired'


class Employee(TimeStampedModel):
    """Employee profile linked to the custom project user model.

    - `user` is a OneToOneField to the custom user model defined in `users` app.
    - `employee_number` is unique and indexed for fast lookup.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employee_profile')
    employee_number = models.CharField(max_length=30, unique=True, help_text='Unique employee identifier')
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name='employees')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    job_title = models.ForeignKey(JobTitle, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    employment_type = models.ForeignKey(EmploymentType, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    supervisor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')

    first_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150)
    gender = models.CharField(max_length=1, choices=Gender.choices, blank=True)
    marital_status = models.CharField(max_length=10, choices=MaritalStatus.choices, blank=True)
    national_id = models.CharField(max_length=50, blank=True, help_text='National identification number')
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=30, validators=[phone_validator], blank=True)
    email = models.EmailField(validators=[EmailValidator()], blank=True)
    address = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_phone = models.CharField(max_length=30, validators=[phone_validator], blank=True)
    hire_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='employees/profile_pics/%Y/%m/%d/', null=True, blank=True)
    employment_status = models.CharField(max_length=10, choices=EmploymentStatus.choices, default=EmploymentStatus.ACTIVE)

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        ordering = ['-hire_date', 'last_name']
        indexes = [
            models.Index(fields=['employee_number']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.employee_number} - {self.first_name} {self.last_name}"


class AttendanceStatus(models.TextChoices):
    PRESENT = 'PRESENT', 'Present'
    ABSENT = 'ABSENT', 'Absent'
    HALF_DAY = 'HALF_DAY', 'Half Day'
    ON_LEAVE = 'ON_LEAVE', 'On Leave'


class Attendance(TimeStampedModel):
    """Daily attendance record per employee."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(help_text='Attendance date')
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    working_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text='Calculated working hours')
    attendance_status = models.CharField(max_length=10, choices=AttendanceStatus.choices, default=AttendanceStatus.PRESENT)
    remarks = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'
        ordering = ['-date']
        indexes = [models.Index(fields=['date']), models.Index(fields=['employee', 'date'])]

    def __str__(self):
        return f"{self.employee.employee_number} - {self.date} - {self.attendance_status}"


class LeaveType(TimeStampedModel):
    """Defines leave categories and allowance."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120)
    days_allowed = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0)])
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Leave Type'
        verbose_name_plural = 'Leave Types'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.days_allowed})"


class LeaveStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    APPROVED = 'APPROVED', 'Approved'
    REJECTED = 'REJECTED', 'Rejected'
    CANCELLED = 'CANCELLED', 'Cancelled'


class LeaveRequest(TimeStampedModel):
    """Employee leave request record."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.PROTECT, related_name='leave_requests')
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=LeaveStatus.choices, default=LeaveStatus.PENDING)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')
    approval_date = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Leave Request'
        verbose_name_plural = 'Leave Requests'
        ordering = ['-start_date']
        indexes = [models.Index(fields=['employee', 'status'])]

    def __str__(self):
        return f"{self.employee.employee_number} - {self.leave_type.name} ({self.status})"


class PerformanceReview(TimeStampedModel):
    """Performance review scores and comments per employee for a review period."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='performance_reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews_given')
    review_period = models.CharField(max_length=50, help_text='E.g., 2025-Q4 or 2025-01')
    communication = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], default=0)
    teamwork = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], default=0)
    professionalism = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], default=0)
    attendance_score = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], default=0)
    initiative = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], default=0)
    leadership = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], default=0)
    overall_score = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(10)], null=True, blank=True)
    comments = models.TextField(blank=True)
    review_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Performance Review'
        verbose_name_plural = 'Performance Reviews'
        ordering = ['-review_date']
        indexes = [models.Index(fields=['review_period']), models.Index(fields=['employee'])]

    def save(self, *args, **kwargs):
        # compute overall_score if not provided
        if not self.overall_score:
            scores = [self.communication, self.teamwork, self.professionalism, self.attendance_score, self.initiative, self.leadership]
            try:
                self.overall_score = round(sum(scores) / len(scores), 2)
            except Exception:
                self.overall_score = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.employee_number} - {self.review_period} - {self.overall_score}"


class Announcement(TimeStampedModel):
    """Public announcements targeted to branches or global."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    message = models.TextField()
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='announcements_posted')
    target_branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='announcements')
    publish_date = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'
        ordering = ['-publish_date']

    def __str__(self):
        return f"{self.title} ({self.publish_date.date() if self.publish_date else 'unspecified'})"


class SurveyStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft'
    ACTIVE = 'ACTIVE', 'Active'
    CLOSED = 'CLOSED', 'Closed'


class Survey(TimeStampedModel):
    """Survey definition containing multiple questions."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='surveys_created')
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    anonymous = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=SurveyStatus.choices, default=SurveyStatus.DRAFT)

    class Meta:
        verbose_name = 'Survey'
        verbose_name_plural = 'Surveys'
        ordering = ['-created_at']
        indexes = [models.Index(fields=['created_at']), models.Index(fields=['status'])]

    def __str__(self):
        return self.title


class QuestionType(models.TextChoices):
    TEXT = 'TEXT', 'Text'
    SINGLE = 'SINGLE', 'Single Choice'
    MULTIPLE = 'MULTIPLE', 'Multiple Choice'
    RATING = 'RATING', 'Rating'


class SurveyQuestion(TimeStampedModel):
    """Individual question belonging to a survey."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    question_type = models.CharField(max_length=10, choices=QuestionType.choices, default=QuestionType.TEXT)
    required = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Survey Question'
        verbose_name_plural = 'Survey Questions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.survey.title}: {self.question[:60]}"


class SurveyResponse(models.Model):
    """Response given by an employee to a single survey question."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE, related_name='responses')
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='survey_responses')
    answer = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Survey Response'
        verbose_name_plural = 'Survey Responses'
        ordering = ['-submitted_at']

    def __str__(self):
        return f"Response {self.id} to {self.survey.title}"


class Recognition(TimeStampedModel):
    """Employee recognition / awards."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='recognitions')
    awarded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='recognitions_awarded')
    title = models.CharField(max_length=200)
    reason = models.TextField(blank=True)
    award_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Recognition'
        verbose_name_plural = 'Recognitions'
        ordering = ['-award_date']

    def __str__(self):
        return f"{self.title} - {self.employee.employee_number}"


class SuggestionStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    REVIEWED = 'REVIEWED', 'Reviewed'
    IMPLEMENTED = 'IMPLEMENTED', 'Implemented'
    REJECTED = 'REJECTED', 'Rejected'


class Suggestion(TimeStampedModel):
    """Employee suggestion or idea submission."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='suggestions')
    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=12, choices=SuggestionStatus.choices, default=SuggestionStatus.PENDING)
    hr_response = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Suggestion'
        verbose_name_plural = 'Suggestions'
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.subject} - {self.employee.employee_number}"


class ComplaintStatus(models.TextChoices):
    OPEN = 'OPEN', 'Open'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    RESOLVED = 'RESOLVED', 'Resolved'
    CLOSED = 'CLOSED', 'Closed'


class Complaint(TimeStampedModel):
    """Employee complaint or grievance."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='complaints')
    category = models.CharField(max_length=150)
    description = models.TextField()
    status = models.CharField(max_length=12, choices=ComplaintStatus.choices, default=ComplaintStatus.OPEN)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='complaints_assigned')
    resolution = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Complaint'
        verbose_name_plural = 'Complaints'
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.category} - {self.employee.employee_number} ({self.status})"


class EmployeeDocument(models.Model):
    """Employee document storage.

    Files are stored under `employees/documents/<year>/<month>/<day>/`.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=150)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='employees/documents/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Employee Document'
        verbose_name_plural = 'Employee Documents'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.title} - {self.employee.employee_number}"


class NotificationType(models.TextChoices):
    INFO = 'INFO', 'Information'
    ALERT = 'ALERT', 'Alert'
    REMINDER = 'REMINDER', 'Reminder'


class Notification(models.Model):
    """In-app / dashboard notification for users."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=10, choices=NotificationType.choices, default=NotificationType.INFO)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} -> {self.recipient.username}"


class AuditLog(models.Model):
    """Generic audit log for critical user actions.

    Stores the user, action, model name, record id and an optional description.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    action = models.CharField(max_length=200)
    model_name = models.CharField(max_length=200)
    record_id = models.CharField(max_length=100, help_text='Primary key of the affected record')
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.created_at.isoformat()} - {self.user or 'system'} - {self.action} on {self.model_name}({self.record_id})"

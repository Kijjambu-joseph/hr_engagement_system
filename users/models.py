# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class BankUser(AbstractUser):
	ROLE_CHOICES = [
		('branch_staff', 'Branch Staff (Initiator)'),
		('branch_manager', 'Branch Manager (Approver/Initiator)'),
		('hrbp', 'HR Business Partner (Handler/Resolver)'),
		('hr_specialist', 'Head Office HR Specialist (Escalation Resolver)'),
		('executive', 'Executive Management (Viewer/Auditor)'),
	]
    
	role = models.CharField(
		max_length=20, 
		choices=ROLE_CHOICES, 
		default='branch_staff'
	)

	def save(self, *args, **kwargs):
		# Ensure raw passwords entered via admin or data import are hashed.
		if self.password and not any(self.password.startswith(prefix) for prefix in (
			'pbkdf2_',
			'argon2$',
			'bcrypt$',
			'sha1$',
		)):
			self.set_password(self.password)
		super().save(*args, **kwargs)

	# Useful for HRBPs who manage multiple branches in a region
	region_cluster = models.CharField(
		max_length=100, 
		blank=True, 
		help_text="e.g., Central Cluster, Western Region, Head Office"
	)
	branch_name = models.CharField(max_length=100, blank=True)
	employee_id = models.CharField(max_length=15, unique=True, null=True, blank=True)

	def __str__(self):
		return f"{self.get_full_name() or self.username} - {self.get_role_display()}"


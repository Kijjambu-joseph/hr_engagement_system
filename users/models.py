# users/models.py
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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


class UserProfile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
	role = models.CharField(max_length=50, blank=True)
	branch = models.CharField(max_length=100, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"Profile for {self.user.username}"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(
			user=instance,
			role=getattr(instance, 'role', ''),
			branch=getattr(instance, 'branch_name', ''),
		)
	else:
		profile, _ = UserProfile.objects.get_or_create(user=instance)
		updated = False
		role_value = getattr(instance, 'role', '')
		branch_value = getattr(instance, 'branch_name', '')
		if role_value and profile.role != role_value:
			profile.role = role_value
			updated = True
		if branch_value and profile.branch != branch_value:
			profile.branch = branch_value
			updated = True
		if updated:
			profile.save()


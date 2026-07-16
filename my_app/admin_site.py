from django.contrib.admin import AdminSite
from django.core.exceptions import PermissionDenied
from django.urls import reverse

ALLOWED_ADMIN_ROLES = {"executive", "hrbp", "hr_specialist", "branch_manager"}
ALLOWED_ADMIN_GROUPS = {
    "General Managers",
    "General Manager",
    "HRBP",
    "HRBPs",
    "HR Specialists",
    "Executives",
    "System Administrators",
}


def can_access_admin(user):
    if not user.is_authenticated or not user.is_active:
        return False

    if user.is_superuser:
        return True

    if not user.is_staff:
        return False

    if getattr(user, "role", None) in ALLOWED_ADMIN_ROLES:
        return True

    if user.groups.filter(name__in=ALLOWED_ADMIN_GROUPS).exists():
        return True

    return False


class HRAdminSite(AdminSite):
    site_header = "HR Engagement System"
    site_title = "HR Engagement System"
    index_title = "Administrative Command Center"

    def has_permission(self, request):
        return can_access_admin(request.user)

    def login(self, request, extra_context=None):
        if request.user.is_authenticated and not can_access_admin(request.user):
            raise PermissionDenied("You do not have permission to access this admin interface.")
        return super().login(request, extra_context=extra_context)

    def each_context(self, request):
        context = super().each_context(request)
        context["admin_search_url"] = reverse("admin:index")
        return context


hr_admin_site = HRAdminSite(name="hr_admin")

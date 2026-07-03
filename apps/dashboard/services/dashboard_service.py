from apps.access.models import User, Role, Permission


class DashboardService:
    def get_stats(self) -> dict:
        return {
            'total_users': User.objects.count(),
            'total_roles': Role.objects.count(),
            'total_permissions': Permission.objects.count(),
            'active_users': User.objects.filter(status='Active', blocked=False).count(),
        }

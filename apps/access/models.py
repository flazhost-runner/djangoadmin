"""Access module models — User, Role, Permission with byte-identical schema to NodeAdmin."""
import uuid
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password


def _uuid4_str():
    return str(uuid.uuid4())


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email required')
        user = self.model(email=email.lower().strip(), **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    """Canonical users table — matches NodeAdmin's User entity exactly."""
    class Meta:
        db_table = 'users'

    id = models.CharField(max_length=36, primary_key=True, default=_uuid4_str, editable=False)
    code = models.CharField(max_length=20, unique=True, default='')
    name = models.CharField(max_length=50, default='')
    phone = models.CharField(max_length=15, default='')
    email = models.CharField(max_length=255, unique=True)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    password = models.CharField(max_length=255)
    password_otp = models.CharField(max_length=255, null=True, blank=True)
    password_otp_expires = models.BigIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, default='Active')
    picture = models.CharField(max_length=255, null=True, blank=True)
    blocked = models.BooleanField(default=False)
    blocked_reason = models.CharField(max_length=255, null=True, blank=True)
    timezone = models.CharField(max_length=255, default='UTC')
    created_by = models.CharField(max_length=36, default='')
    updated_by = models.CharField(max_length=36, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    last_login = None  # remove AbstractBaseUser.last_login

    roles = models.ManyToManyField(
        'Role',
        through='UsersRoles',
        through_fields=('user', 'role'),
        related_name='users',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    @property
    def is_active(self):
        return self.status == 'Active' and not self.blocked

    @property
    def is_staff(self):
        return self.is_administrator()

    @property
    def is_superuser(self):
        return self.is_administrator()

    def is_administrator(self):
        return self.roles.filter(name='Administrator').exists()

    def has_access(self, route_name: str, method: str = 'GET') -> bool:
        if self.is_administrator():
            return True
        return UsersRoles.objects.filter(
            user=self,
            role__roles_permissions__permission__name=route_name,
            role__roles_permissions__permission__method=method.upper(),
        ).exists()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.email


class Role(models.Model):
    """Canonical roles table."""
    class Meta:
        db_table = 'roles'

    id = models.CharField(max_length=36, primary_key=True, default=_uuid4_str, editable=False)
    name = models.CharField(max_length=255, unique=True)
    guard_name = models.CharField(max_length=20, default='web')
    status = models.CharField(max_length=20, default='Active')
    desc = models.CharField(max_length=255, null=True, blank=True, db_column='desc')
    created_by = models.CharField(max_length=36, default='')
    updated_by = models.CharField(max_length=36, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    permissions = models.ManyToManyField(
        'Permission',
        through='RolesPermissions',
        through_fields=('role', 'permission'),
        related_name='roles',
    )

    def __str__(self):
        return self.name


class Permission(models.Model):
    """Canonical permissions table — name is NON-unique (has index but no unique constraint)."""
    class Meta:
        db_table = 'permissions'
        indexes = [
            models.Index(fields=['name'], name='permissions__name'),
            models.Index(fields=['guard_name'], name='permissions__guard_name'),
        ]

    id = models.CharField(max_length=36, primary_key=True, default=_uuid4_str, editable=False)
    name = models.CharField(max_length=255)  # NON-unique — route name
    guard_name = models.CharField(max_length=20, default='web')
    method = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, default='Active')
    desc = models.CharField(max_length=255, null=True, blank=True, db_column='desc')
    created_by = models.CharField(max_length=36, default='')
    updated_by = models.CharField(max_length=36, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} [{self.method}]'


class UsersRoles(models.Model):
    """Join table users_roles — explicit through model with pinned column names."""
    class Meta:
        db_table = 'users_roles'
        unique_together = [('user', 'role')]

    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id', related_name='users_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_column='role_id', related_name='users_roles')

    def __str__(self):
        return f'{self.user_id} → {self.role_id}'


class RolesPermissions(models.Model):
    """Join table roles_permissions — explicit through model with pinned column names."""
    class Meta:
        db_table = 'roles_permissions'
        unique_together = [('role', 'permission')]

    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_column='role_id', related_name='roles_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, db_column='permission_id', related_name='roles_permissions')

    def __str__(self):
        return f'{self.role_id} → {self.permission_id}'

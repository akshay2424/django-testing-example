from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = None
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)  # a superuser

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.
    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin


class Roles(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)

    # relationship
    # _role = relationship("RoleUser", back_populates="role_user")
    # _role_perm = relationship("PermissionRole", back_populates="permission_role")

    def __repr__(self):
        return "<Roles(roles_name='%s')>" % (self.name)


class PermissionsS(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    group_key = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)

    # relationship
    # _permission = relationship("Role", back_populates="permission_role")

    def __repr__(self):
        return "<Permissions(:name='%s')>" % (self.name)


class RoleUser(models.Model):

    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    role_id = models.ForeignKey(Roles, on_delete=models.CASCADE)

    # relationship
    # _user = relationship("User", back_populates="user")
    # role = relationship("Roles", back_populates="roles")

    def __repr__(self):
        return "<RoleUser(roles='%s')>" % (self.user_id)


class PermissionRole(models.Model):

    id = models.AutoField(primary_key=True)
    permission_id = models.ForeignKey(PermissionsS, on_delete=models.CASCADE)
    role_id = models.ForeignKey(Roles, on_delete=models.CASCADE)

    def __repr__(self):
        return "<RoleUser(roles='%s')>" % (self.role_id)

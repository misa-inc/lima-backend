from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Create and save a user with the given email.
        """
        if not password:
            raise ValueError("Users must have a password")     

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(email, username, password)

        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

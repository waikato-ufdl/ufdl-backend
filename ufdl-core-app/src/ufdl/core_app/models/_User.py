from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    The base user model for all users of the UFDL system. Although this is currently
    identical to the Django User class, it is considered best practice to define
    your own user model, so it can be modified in future should the need arise.
    """
    pass

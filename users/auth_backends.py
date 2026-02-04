from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailOrPhoneBackend(ModelBackend):
    """
    Позволяет аутентифицироваться по email или по номеру телефона.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Берём login из username или kwargs
        login = username or kwargs.get("username") or kwargs.get("login")
        password = password or kwargs.get("password")
        if not login or not password:
            return None

        try:
            user = User.objects.get(Q(email__iexact=login) | Q(phone=login))
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

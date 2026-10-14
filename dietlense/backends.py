from django.contrib.auth.backends import BaseBackend
from dietlense.models import CustomUser

class EmailBackend(BaseBackend):
    def authenticate(self, request, username = ..., password = ..., **kwargs):
        try:
            user_object=CustomUser.objects.get(email=username)
            user_password=user_object.password

            if user_object.check_password(password):
                return user_object

            else:
                return None

        except:
            return None
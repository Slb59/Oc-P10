# from django.db import models
from django.db import models
from django.contrib.auth import models as auth_models


class User(auth_models.AbstractUser):
    post_description = models.CharField(max_length=128, default="")

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def is_admin(self):
        return self.is_admin

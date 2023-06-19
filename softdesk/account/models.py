# from django.db import models
from django.db import models
from django.contrib.auth import models as auth_models


class User(auth_models.AbstractUser):
    user_id = models.AutoField(primary_key=True)

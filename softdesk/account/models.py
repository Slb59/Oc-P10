from datetime import datetime
from django.db import models
# from django.db.models import CheckConstraint, Q, F
from django.contrib.auth import models as auth_models
# from django.utils.translation import gettext_lazy as _
# from django.core.exceptions import ValidationError


class User(auth_models.AbstractUser):
    post_description = models.CharField(max_length=128, default="")
    birth_date = models.DateField(blank=False, null=False)

    @property
    def age(self):
        return int((datetime.now().date() - self.birth_date).days / 365.25)

    # @property
    # def max_birth_date(self):
    #     return datetime.today() - timedelta(days=365*15)

    # class Meta:
    #     constraints = [
    #         # Ensures constraint on DB level, raises IntegrityError
    #         CheckConstraint(
    #             check=Q(birth_date__lte=(
    # datetime.today() - timedelta(days=365*15))),
    #             name='check_birth_date',
    #         ),
    #     ]

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def is_admin(self):
        return self.is_admin



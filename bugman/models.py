from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.db import models
# from unidecode import unidecode

#
# class AlligatorUser(AbstractBaseUser):
#     ROLES = (
#         ('AR', 'All-Round'),
#         ('BE', 'BackEnd'),
#         ('FE', 'FrontEnd'),
#         ('PM', 'Project Manager'),
#         ('UX', 'User eXperience'),
#         ('NA', 'Not Applicable'),
#     )
#     username = models.CharField(max_length=40, unique=True, primary_key=True)
#     name = models.CharField(max_length=200, unique=False)
#     email = models.CharField(max_length=100)
#     is_active = models.BooleanField(default=True)
#     photo_url = models.URLField(editable=False, null=True)
#     role = models.CharField(max_length=2, choices=ROLES, null=True)
#     location = models.CharField(max_length=100)
#     start_date = models.DateField(null=True, blank=True)
#
#     is_superuser = models.BooleanField()
#     is_staff = models.BooleanField()
#
#     objects = UserManager()
#
#     USERNAME_FIELD = 'username'
#
#     def info(self):
#         return vars(self)
#
#     def get_full_name(self):
#         return self.name
#
#     def get_short_name(self):
#         return self.username
#
#     def _photo_url(self, size, options):
#         if options:
#             options = "-" + "-".join(options)
#         else:
#             options = ""
#         try:
#             url = self.photo_url.replace('=h50', '')
#             url = "%s=s%d%s" % (url, size, options)
#         except AttributeError:
#             url = None
#         return url
#
#     @property
#     def tiny_photo_url(self):
#         return self._photo_url(50, ["pp"])
#
#     @property
#     def small_photo_url(self):
#         return self._photo_url(100, ["pp"])
#
#     @property
#     def weeks(self):
#         """here only to support V1 API data structure"""
#         return []
#
#     # @property
#     # def normalised_name(self):
#     #     return unidecode(self.name)
from django.contrib.admin import site
from .models import *

site.register(Candidate)
site.register(UserData)
site.register(Leader)

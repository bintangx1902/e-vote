from django.db import models
from django.contrib.auth.models import User


class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_data', related_query_name='user_data')
    no_phone = models.CharField(verbose_name='Nomor Telepon :', max_length=16)
    has_vote = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}"


class Candidate(models.Model):
    candidate = models.CharField(max_length=255)
    leader = models.CharField(max_length=255, default='')
    co_leader = models.CharField(max_length=255, default='')
    vote = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.candidate} - {self.vote} Suara"

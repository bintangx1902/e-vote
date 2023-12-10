from django.db import models
from django.contrib.auth.models import User


class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_data', related_query_name='user_data')
    no_phone = models.CharField(verbose_name='Nomor Telepon :', max_length=16)
    has_vote = models.BooleanField(default=False)
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.user}"


class Leader(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='images/', default='')
    desc = models.TextField()

    def __str__(self):
        return f"{self.name}"


class Candidate(models.Model):
    candidate = models.CharField(max_length=255)
    leader = models.ForeignKey(Leader, on_delete=models.CASCADE)
    co_leader = models.ForeignKey(Leader, on_delete=models.CASCADE, related_name='co_leader', related_query_name='co_leader')
    vote = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.candidate} - {self.vote} Suara"

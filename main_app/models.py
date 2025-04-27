import uuid
from django.db import models
from django.contrib.auth.models import User


GENDER_TYPE = (
    ('M', 'мужской'),
    ('W', 'женский')
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,)
    fullname = models.CharField(max_length=200)
    email = models.CharField(max_length=100, unique=True)
    mobile_phone = models.CharField(max_length=20, unique=True)
    gender = models.CharField(choices=GENDER_TYPE, default='M')
    age = models.IntegerField()
    category = models.CharField(max_length=100)
    rating = models.IntegerField(null=True)
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.fullname


TEAM_ROLE = (
    ('forward','нападающий'),
    ('defender', 'защитник'),
    ('goalkeeper','вратарь')
)

class TestBalancer(models.Model):
    name = models.CharField(max_length=50)
    rating = models.IntegerField()
    role = models.CharField(choices=TEAM_ROLE, default='forward')
    age = models.IntegerField()
    gender = models.CharField(choices=GENDER_TYPE, default='M')

    def __str__(self):
        return self.name
    

class Micromatch(models.Model):
    match_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    matchRating = models.IntegerField()
    team1_players = models.JSONField()
    team2_players = models.JSONField()
    team1_score = models.IntegerField(null=True)
    team2_score = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)




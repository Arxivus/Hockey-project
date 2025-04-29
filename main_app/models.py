import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


GENDER_TYPE = (
    ('M', 'мужской'),
    ('W', 'женский')
)

SITE_ROLE = (
    ('S', 'спортсмен'),
    ('C', 'тренер'),
    ('R', 'судья')
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,)
    fullname = models.CharField(max_length=200)
    email = models.CharField(max_length=100, unique=True)
    mobile_phone = models.CharField(max_length=20, unique=True)
    gender = models.CharField(choices=GENDER_TYPE, default='M')
    age = models.IntegerField(validators=[ MinValueValidator(6),  MaxValueValidator(90) ])
    category = models.CharField(max_length=100)
    rating = models.IntegerField(null=True)
    role = models.CharField(choices=SITE_ROLE, default='S')

    def __str__(self):
        return self.fullname


TEAM_ROLE = (
    ('forward','нападающий'),
    ('defender', 'защитник'),
    ('goalkeeper','вратарь')
)

class TestBalancer(models.Model):
    player_id = models.IntegerField(unique=True, editable=False, null=True)
    name = models.CharField(max_length=50)
    rating = models.IntegerField()
    role = models.CharField(choices=TEAM_ROLE, default='forward')
    age = models.IntegerField()
    gender = models.CharField(choices=GENDER_TYPE, default='M')
    matches_played = models.IntegerField(default=0)
    goals_scored = models.IntegerField(default=0)
    goals_taken = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.player_id:
            last_obj = TestBalancer.objects.order_by('-player_id').first()
            self.player_id = 1 if not last_obj else last_obj.player_id + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.player_id}: {self.name}"
    

class Micromatch(models.Model):
    match_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    matchRating = models.IntegerField()
    team1_players = models.JSONField()
    team2_players = models.JSONField()
    team1_score = models.IntegerField(null=True)
    team2_score = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)




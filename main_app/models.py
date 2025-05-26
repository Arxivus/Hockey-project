import uuid
import json
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


GENDER_TYPE = (
    ('M', 'мужской'),
    ('W', 'женский')
)

TEAM_ROLE = (
    ('forward','нападающий'),
    ('defender', 'защитник'),
    ('goalkeeper','вратарь')
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,)
    fullname = models.CharField(max_length=200)
    email = models.CharField(max_length=100, unique=True)
    mobile_phone = models.CharField(max_length=20, unique=True)
    gender = models.CharField(choices=GENDER_TYPE, default='M')
    age = models.IntegerField(validators=[ MinValueValidator(6),  MaxValueValidator(90) ])
    category = models.CharField(max_length=100, null=True, blank=True)
    rating = models.IntegerField(null=True, default=0)
    role = models.CharField(choices=TEAM_ROLE, default='forward', null=True, blank=True)

    class Meta:
        permissions = [
            ("cant_reg_in_tour", "Cannot register in tournament"),
        ]

    def __str__(self):
        return self.fullname


class Competitor(models.Model):
    player_id = models.IntegerField(primary_key=True, unique=True, editable=False) 
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    role = models.CharField(choices=TEAM_ROLE, default='forward')
    age = models.IntegerField()
    gender = models.CharField(choices=GENDER_TYPE, default='M')

    rating = models.IntegerField(null=True)
    start_rating = models.IntegerField(null=True)
    group_id = models.IntegerField(null=True)
    matches_played = models.IntegerField(default=0)
    goals_scored = models.IntegerField(default=0)
    goals_taken = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.player_id:
            last_obj = Competitor.objects.order_by('-player_id').first()
            self.player_id = 1 if not last_obj else last_obj.player_id + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"ID: {self.player_id}, {self.name}, {self.role}, {self.age}, matches: {self.matches_played}"
    

class Tournament(models.Model):
    tour_id = models.IntegerField(primary_key=True, unique=True, editable=False)
    date = models.DateField(auto_now_add=True)
    played_with_matrix = models.JSONField(default=list)

    class Meta:
        permissions = [
            ("can_start_tour", "Can start new tournament"),
        ]

    def save(self, *args, **kwargs):
        if not self.tour_id:
            last_obj = Tournament.objects.order_by('-tour_id').first()
            self.tour_id = 1 if not last_obj else last_obj.tour_id + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Турнир №{self.tour_id}"


class TournamentGroup(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='groups')
    group_id = models.IntegerField()
    group_age_pool = models.JSONField(default=tuple)
    age_spread = models.IntegerField(default=1)
    group_gender = models.CharField() 
    stopped_played = models.BooleanField(default=False)

    def __str__(self):
        return f"Группа №{self.group_id}, {self.group_age_pool[0]}-{self.group_age_pool[1]} лет, {self.group_gender}"
   

class Micromatch(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=True, related_name='matches')
    match_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    matchRating = models.IntegerField()
    team1_players = models.JSONField()
    team2_players = models.JSONField()
    team1_score = models.IntegerField(default=0)
    team2_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ("can_save_score", "Can save match score"),
            ("can_generate_match", "Can generate new match"),
        ]

    def __str__(self):
        return f"Микроматч {self.created_at}"
    
    


class Announsment(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField(max_length=500)

    def __str__(self):
        return self.title

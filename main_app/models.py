import uuid
from django.utils import timezone
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
    ('goalkeeper','вратарь'),
    ('referee','судья'),
    ('coach','тренер'),
)

CATEGORY_TYPE = (
    ('новичок','новичок'),
    ('любитель', 'любитель'),
    ('III юношеский','III юношеский'),
    ('II юношеский','II юношеский'),
    ('I юношеский','I юношеский'),
    ('III спортивный','III спортивный'),
    ('II спортивный','II спортивный'),
    ('I спортивный','I спортивный'),
    ('КМС','КМС'),
    ('ГР','ГР'),
    ('МСМК','МСМК')
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,)
    fullname = models.CharField('ФИО', max_length=200)
    email = models.CharField(max_length=100)
    mobile_phone = models.CharField('Телефон', max_length=20)
    gender = models.CharField('Пол', choices=GENDER_TYPE, max_length=20)
    age = models.IntegerField('Возраст', null=True) 
    category = models.CharField('Уровень подготовки', choices=CATEGORY_TYPE, null=True, blank=True, max_length=20)
    rating = models.IntegerField('Рейтинг', null=True, default=0)
    previous_ratings = models.JSONField('Прошлые рейтинги', default=list)
    role = models.CharField('Роль', choices=TEAM_ROLE, null=True, blank=True, max_length=20)
    tg_chat_id = models.BigIntegerField(null=True)
    

    class Meta:
        verbose_name = 'Профиль пользователя'        
        verbose_name_plural = 'Профили пользователей' 
        permissions = [
            ("cant_reg_in_tour", "Cannot register in tournament"),
        ]

    def __str__(self):
        return f'{self.fullname} / {self.role}' 


class Competitor(models.Model):
    player_id = models.IntegerField('ID игрока', primary_key=True, unique=True, editable=False) 
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField('Имя', max_length=50)
    role = models.CharField('Роль', choices=TEAM_ROLE, default='forward', max_length=20)
    age = models.IntegerField('Возраст', null=True)
    gender = models.CharField('Пол', choices=GENDER_TYPE, default='M', max_length=20)

    rating = models.IntegerField('Рейтинг', null=True)
    start_rating = models.IntegerField(null=True)
    group_id = models.IntegerField('ID группы', null=True, blank=True)
    matches_played = models.IntegerField('Матчей сыграно', default=0)
    goals_scored = models.IntegerField('Забитые', default=0)
    goals_taken = models.IntegerField('Пропущенные', default=0)
    banned = models.BooleanField('Исключен', default=False  )   

    def save(self, *args, **kwargs):
        if not self.player_id:
            last_obj = Competitor.objects.order_by('-player_id').first()
            self.player_id = 1 if not last_obj else last_obj.player_id + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"ID: {self.player_id}, {self.name}, {self.role}, {self.age}, сыграно: {self.matches_played} матчей, {self.rating}"
    
    class Meta:
        verbose_name = 'Участник'        
        verbose_name_plural = 'Участники' 
    

class Tournament(models.Model):
    tour_id = models.IntegerField('Номер турнира', primary_key=True, unique=True, editable=False)
    playing_groups_ids = models.JSONField('ID групп турнира', default=list)
    date = models.DateField('Дата', default=timezone.now)
    time_started = models.TimeField('Время начала', default=timezone.now)
    minutes_btwn_groups = models.IntegerField('Перерыв между группами (мин)', validators=[MinValueValidator(0)], default=10)
    minutes_btwn_matches = models.IntegerField('Перерыв между  матчами (мин)', validators=[MinValueValidator(0)], default=1)
    played_with_matrix = models.JSONField('Матрица встреч игроков', default=list)
    isEnded = models.BooleanField('Турнир закончен', default=False)

    class Meta:
        verbose_name = 'Турнир'        
        verbose_name_plural = 'Турниры' 
        permissions = [
            ("can_start_tour", "Can start new tournament"),
            ("can_shift_timetable", "Can shift timetable"),
        ]

    def save(self, *args, **kwargs):
        if not self.tour_id:
            last_obj = Tournament.objects.order_by('-tour_id').first()
            self.tour_id = 1 if not last_obj else last_obj.tour_id + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Турнир №{self.tour_id} / {self.date.strftime('%d-%m-%Y')}"


class TournamentGroup(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='groups')
    group_id = models.IntegerField('ID группы')
    group_age_pool = models.JSONField('Диапазон возраста', default=tuple)
    age_spread = models.IntegerField('Разброс по возрасту в матче', default=1)
    group_gender = models.CharField('Пол участников', max_length=20) 
    stopped_played = models.BooleanField('Закончила играть', default=False)

    def __str__(self):
        return f"Группа №{self.group_id}, {self.group_age_pool[0]}-{self.group_age_pool[1]} лет, {self.group_gender}"
    
    class Meta:
        verbose_name = 'Группа турнира'        
        verbose_name_plural = 'Группы турнира' 
   

class Micromatch(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=True, related_name='matches')
    group_id = models.IntegerField('ID группы', null=True)
    match_id = models.UUIDField('ID матча', primary_key=True, default=uuid.uuid4, editable=False)
    matchRating = models.IntegerField('Средний рейтинг')
    players_ids = models.JSONField('ID игроков', default=list)
    team1_players = models.JSONField('Команда 1')
    team2_players = models.JSONField('Команда 2')
    team1_score = models.IntegerField('Счет первой команды', default=0)
    team2_score = models.IntegerField('Счет второй команды', default=0)
    isPlayed = models.BooleanField('Матч сыгран', default=False)
    start_time = models.TimeField('Время начала', default=timezone.now)
    field_num = models.IntegerField('Номер поля', default=1)

    class Meta:
        verbose_name = 'Микроматч'        
        verbose_name_plural = 'Микроматчи' 
        permissions = [
            ("can_save_score", "Can save match score"),
            ("can_generate_match", "Can generate new match"),
        ]

    def __str__(self):
        return f"Микроматч / время: {self.start_time.strftime('%H:%M')}"
    
    


class Announsment(models.Model):
    title = models.CharField('Заголовок', max_length=150)
    text = models.TextField('Текст', max_length=500)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Объявление'        
        verbose_name_plural = 'Объявления'  

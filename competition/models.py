from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Team(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Round(models.Model):
    number = models.IntegerField(unique=True)
    deadline = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Round {self.number}"


class Match(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="home_team")
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="away_team")
    winner = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    eliminated = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Tip(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('player', 'round')

    def clean(self):
        if Tip.objects.filter(player=self.player, team=self.team).exclude(round=self.round).exists():
            raise ValidationError("You have already used this team.")
        
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)       
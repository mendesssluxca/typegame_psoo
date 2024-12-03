from django.db import models

class Player(models.Model):
    username = models.CharField(max_length=100, unique=True)
    high_score = models.IntegerField(default=0)

    def __str__(self):
        return self.username

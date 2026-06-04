from django.db import models


class VideoSubtitle(models.Model):
    video_id = models.CharField(max_length=32, unique=True)
    subtitle = models.TextField()

    def __str__(self):
        return self.video_id


class Users(models.Model):
    user_name = models.CharField(max_length=150, unique=True)
    mail_id = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    class Meta:
        db_table = "Users"

    def __str__(self):
        return self.user_name

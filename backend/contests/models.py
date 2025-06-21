from django.db import models
from django.contrib.auth.models import User

class Contest(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contests")
    image = models.ImageField(upload_to='contestimages')
    price = models.TextField()

class Participation(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='participations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contest_participations')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('contest', 'user')  # Ensures a user can only participate once in a contest
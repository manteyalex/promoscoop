from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from users.models import Profile
from django.utils import timezone
from datetime import date, datetime, time
import pytz

class Contest(models.Model):

    title = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    details = models.TextField()
    URL = models.CharField(max_length=2048) #commonly accepted max length for urls
    regions = ArrayField(models.CharField(max_length=100), default=list)
    frequency = models.CharField(max_length=50)
    date_posted = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()

    image = models.ImageField(default='default.jpg',upload_to='contest_pics')

    def __str__(self):
        return self.title

    @property
    def is_expired(self):
        tz = pytz.timezone('US/Eastern')
        today = datetime.now(tz).date()
        today = tz.localize(datetime.combine(today, time(0, 0)), is_dst=None)
        return today > self.end_date

class UserContest(models.Model):
    user = models.ForeignKey(User,related_name='user',on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest,related_name='contest',on_delete=models.CASCADE)
    entries = models.IntegerField(default=0)
    time_added = models.DateTimeField(default=timezone.now)
    last_entered = models.DateTimeField(default=None, blank=True, null=True)
    class Meta:
        unique_together = ["user", "contest"]
    def __str__(self):
        return f'{self.user.username} - {self.contest.title}'
    @property
    def enter_available(self):
        tz = pytz.timezone('US/Eastern')
        today = datetime.now(tz).date()
        midnight = tz.localize(datetime.combine(today, time(0, 0)), is_dst=None)
        print(midnight)
        if self.contest.frequency == 'daily':
            if self.last_entered:
                return self.last_entered < midnight
            else:
                return True
        else:
            return True